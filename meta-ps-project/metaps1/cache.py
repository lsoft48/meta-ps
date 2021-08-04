# -*- coding: utf-8 -*-
from pathlib import Path
import tempfile
import os
import shutil
import zipfile
import patoolib

class LCache:
    def __init__(self, opt):
        self.__options=opt
        self.__downloads={}
        self.__installs={}
        self.__base=Path(opt.cache)
        if not self.__base.exists():
            #создаем папку
            self.__base.mkdir(parents=True, exist_ok=True)
        elif self.__base.is_file():
            raise Exception("Невозможно использовать локальный кэш файлов - указанный путь %s является файлом, а не папкой" % self.__base)
        #все нормально - папка существует

    def GetVersionPath(self, version):
        """ получение пути к папке версии в кэше """
        return self.__base / "ent" / version

    def GetPlatformFilePath(self, version):
        """ Получение пути, для размещения файлов платформы в локальном кэше """
        res = GetVersionPath(version)
        res.mkdir(parents=True, exist_ok=True)
        return res

    def StartDownload(self, version, file_name):
        """ Вызывается при начале загрузки файла - выделяется временный файл, запоминается 
        расположение результьтата"""
        path=self.GetPlatformFilePath(version)
        tt=tempfile.NamedTemporaryFile(suffix=".part",delete=False)
        self.__downloads[tt.name]=(path / file_name, tt)
        tt.close()
        return tt.name
        
    def FinishDownload(self, tmp_file):
        """ Вызывается при завершении загрузки, с указанием ранее выделенного временного файла. Файл
        перемещается на свое результирующее положение, временные файлы удаляются (если остались).
        Если целевой файл уже был - перед перемещением он перименуется и потом тоже удаляется"""
        (to, tt)=self.__downloads[tmp_file]
        try:
            delete_old=False
            if Path(to).is_file():
                to_old=str(to)+".old"
                for i in range(0, 1000):
                    to_old_temp=to_old+str(i).strip()
                    if not Path(to_old_temp).exists():
                        delete_old=True
                        to_old=to_old_temp
                        break
                if delete_old:
                    shutil.move(to, to_old)
                else:
                    raise Exception("Can't select old file name for %s" % to)
            shutil.move(tt.name, str(to))
            if delete_old:
                os.remove(to_old)
        finally:
            if Path(tt.name).is_file():
                os.remove(tt.name)

    def StartInstall(self, version, file_name):
        """ Вызывается при начале установки - выполняет распаковку платформы во временную папку """
        tt=tempfile.TemporaryDirectory()
        self.__installs[tt.name]=(version, file_name, tt)
        ff=GetVersionPath(self, version) / file_name
        if not ff.is_file():
            raise Exception("Файл платформы %s не существует или не является файлом" % str(ff))
        #в зависимости от вида архива выполняем распаковку
        extracted=True
        if file_name.endswith(".zip"):
            #zip архив
            patoolib.extract_archive(self.__base , outdir=tt.name)
        elif file_name.endswith(".rar"):
            #rar архив
            patoolib.extract_archive(self.__base , outdir=tt.name)
        elif file_name.endswith(".tar.gz"):
            #rtar+gzip архив
            patoolib.extract_archive(self.__base , outdir=tt.name)
        else:
            #файл не требует распаковки - возможно это установщик Linux
            extracted=False
        return (extracted, tt.name)

    def FinishInstall(self, tmp_dir):
        """ Вызывается при завершении устновки - удаляет временную папку с платформой """
        (version, file_name, tt)=self.__installs[tmp_dir]
        try:
            tt.cleanup()
        finally:
            if Path(tt.name).is_dir():
                os.rmdir(tt.name)


