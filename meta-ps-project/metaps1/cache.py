# -*- coding: utf-8 -*-
from pathlib import Path
import tempfile
import os
import shutil
import zipfile
import patoolib

import logging
logger = logging.getLogger(__name__)

class LCache:
    class ExtractError(Exception):
        pass

    class CacheUseError(Exception):
        pass

    def __init__(self, opt):
        logger.info("LCache.__init__()")
        self.__options=opt
        self.__downloads={}
        self.__installs={}
        self.__removes={}
        self.__base=Path(opt.cache)
        if not self.__base.exists():
            #создаем папку
            logger.debug("creating base dir %s " % self.__base)
            self.__base.mkdir(parents=True, exist_ok=True)
        elif self.__base.is_file():
            raise self.CacheUseError("Невозможно использовать локальный кэш файлов - указанный путь %s является файлом, а не папкой" % self.__base)
        #все нормально - папка существует

    def GetVersionPath(self, version):
        """ получение пути к папке версии в кэше """
        return self.__base / "ent" / version

    def GetPlatformFilePath(self, version):
        """ Получение пути, для размещения файлов платформы в локальном кэше """
        res = self.GetVersionPath(version)
        res.mkdir(parents=True, exist_ok=True)
        return res

    def StartDownload(self, version, file_name):
        """ Вызывается при начале загрузки файла - выделяется временный файл, запоминается 
        расположение результьтата"""
        logger.info("StartDownload()")
        logger.debug("version=%s" % version)
        logger.debug("file_name=%s" % file_name)
        path=self.GetPlatformFilePath(version)
        logger.debug("path=%s" % path)
        tt=tempfile.NamedTemporaryFile(suffix=".part",delete=False)
        logger.debug("temp file_name=%s" % tt.name)
        self.__downloads[tt.name]=(path / file_name, tt)
        tt.close()
        return tt.name

    def NeedDownload(self, need_version, file_name):
        """ Проверка наличия файла в кэше """
        logger.info("NeedDownload()")
        logger.debug("need_version=%s" % need_version)
        logger.debug("file_name=%s" % file_name)
        path=self.GetPlatformFilePath(need_version) / file_name
        if path.is_dir():
            raise Exception("Файл элемента плафтформы является папкой %s" % path)
        return not path.is_file()

    def FinishDownload(self, tmp_file):
        """ Вызывается при завершении загрузки, с указанием ранее выделенного временного файла. Файл
        перемещается на свое результирующее положение, временные файлы удаляются (если остались).
        Если целевой файл уже был - перед перемещением он переименуется и потом тоже удаляется"""
        logger.info("FinishDownload()")
        logger.debug("tmp_file=%s" % tmp_file)
        (to, tt)=self.__downloads[tmp_file]
        try:
            delete_old=False
            if Path(to).is_file():
                logger.debug("file already exists %s" % to)
                to_old=str(to)+".old"
                for i in range(0, 1000):
                    to_old_temp=to_old+str(i).strip()
                    if not Path(to_old_temp).exists():
                        delete_old=True
                        to_old=to_old_temp
                        logger.debug("old file name selected %s" % to_old)
                        break
                if delete_old:
                    shutil.move(to, to_old)
                    logger.debug("moved file (%s) to (%s)" % (to,to_old))
                else:
                    raise Exception("Can't select old file name for %s" % to)
            shutil.move(tt.name, str(to))
            logger.debug("moved file (%s) to (%s)" % (tt.name, to))
            if delete_old:
                logger.debug("delete_old=True - removing file (%s)" % to_old)
                os.remove(to_old)
        finally:
            if Path(tt.name).is_file():
                os.remove(tt.name)
                logger.debug("file (%s) still exists (exception?) - removing it" % tt.name)
            logger.info("FinishDownload  - end")

    def StartInstall(self, version, file_name):
        """ Вызывается при начале установки - выполняет распаковку платформы во временную папку """
        logger.info("StartInstall()")
        tt=tempfile.TemporaryDirectory()
        self.__installs[tt.name]=(version, file_name, tt)
        ff=self.GetVersionPath(version) / file_name
        #распакуем архив
        extracted=self.__extract(ff, tt)
        return (extracted, tt.name)

    def FinishInstall(self, tmp_dir):
        """ Вызывается при завершении установки - удаляет временную папку с платформой """
        logger.info("FinishInstall()")
        logger.debug("tmp_dir=%s" % tmp_dir)
        (version, file_name, tt)=self.__installs[tmp_dir]
        try:
            if not self.__options.no_del_tmp:
                logger.debug("cleanup %s" % tt.name)
                tt.cleanup()
        finally:
            if Path(tt.name).is_dir() and (self.__options.no_del_tmp):
                logger.debug("stop removing %s" % tt.name)
                #помечаем финализатор временного объекта как "мертвый", что предотвращает
                #вызов cleanup функции для объекта tt (TemporaryDirectory)
                tt._finalizer.detach()

    def StartRemove(self, version, file_name):
        """ Вызывается при начале удаления - выполняет распаковку платформы во временную папку """
        logger.info("StartRemove()")
        tt=tempfile.TemporaryDirectory()
        self.__removes[tt.name]=(version, file_name, tt)
        ff=self.GetVersionPath(version) / file_name
        #распакуем архив
        extracted=self.__extract(ff, tt)
        return (extracted, tt.name)

    def FinishRemove(self, tmp_dir):
        """ Вызывается при завершении удаления - удаляет временную папку с платформой """
        logger.info("FinishRemove()")
        logger.debug("tmp_dir=%s" % tmp_dir)
        (version, file_name, tt)=self.__removes[tmp_dir]
        try:
            if not self.__options.no_del_tmp:
                logger.debug("cleanup %s" % tt.name)
                tt.cleanup()
        finally:
            if Path(tt.name).is_dir() and (self.__options.no_del_tmp):
                logger.debug("stop removing %s" % tt.name)
                #помечаем финализатор временного объекта как "мертвый", что предотвращает
                #вызов cleanup функции для объекта tt (TemporaryDirectory)
                tt._finalizer.detach()

    def __extract(self, ff, tt):
        """ Распаковка архива в папку """
        if not ff.is_file():
            raise self.ExtractError("Файл архива %s не существует или не является файлом" % str(ff))
        extracted=True
        logger.debug("trying to unpack %s arhive to %s" % (ff, tt.name))
        sff=str(ff)
        fin=sff[-8:]
        if fin.endswith(".zip"):
            #zip архив
            patoolib.extract_archive(sff , outdir=tt.name)
        elif fin.endswith(".rar"):
            #rar архив
            patoolib.extract_archive(sff , outdir=tt.name)
        elif fin.endswith(".tar.gz"):
            #tar+gzip архив
            patoolib.extract_archive(sff , outdir=tt.name)
        else:
            #файл не требует распаковки - возможно это установщик Linux
            extracted=False
        return extracted
