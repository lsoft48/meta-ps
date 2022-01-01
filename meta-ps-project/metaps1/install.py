# -*- coding: utf-8 -*-
import re
import pprint
from pathlib import Path
from locale import getpreferredencoding 
import metaps1.info as inf

import logging
logger = logging.getLogger(__name__)
#alogger = logging.getLogger("apt")

#if inf.platform_linux:
#  import sh
#else:
#  #windows
#  pass


def std_conv(txt):
    return 


class InstallerBase():
    """ Базовый класс инсталлятора - от него создаются установщики
    для linux deb/rpm и для windows native/wine
    """
    class InstallException(Exception):
        pass

    @staticmethod
    def DoInstall(cc, opt, nn, file_name):
        """ Установка элемента платформы """
        logger.info("DoInstall()")
        logger.debug("file_name=%s" % file_name)
        if not opt.need_what in inf.list_4install:
            raise self.InstallException("Элемент платформы %s не требует установки" % opt.need_what)
        #в зависимости от целевой архитектуры создадим инсталлятор
        if opt.need_arh==inf.Platform.LinuxDEB:
            from metaps1.install_linux import InstallerLinuxDeb
            installer=InstallerLinuxDeb(opt, file_name)
        elif opt.need_arh==inf.Platform.Win:
            from metaps1.install_win import InstallerWindows
            installer=InstallerWindows(opt, file_name)
        else:
            raise self.InstallException("Установка для платформы %s не реализована" % opt.need_arh)
        try:
            #получим временную папку и распакуем в нее архив
            #выполним установку
            installer(cc)
        finally:
            #удалим распакованные данные платформы
            pass

    @staticmethod
    def DoRemove(cc, opt, nn, file_name):
        """ Удаление платформы """
        logger.info("DoRemove()")
        logger.debug("file_name=%s" % file_name)
        if not opt.need_what in inf.list_4install:
            raise self.InstallException("Элемент платформы %s не требует удаления" % opt.need_what)
        #в зависимости от целевой архитектуры создадим инсталлятор
        if opt.need_arh==inf.Platform.LinuxDEB:
            from metaps1.install_linux import InstallerLinuxDeb
            installer=InstallerLinuxDeb(opt, file_name)
        elif opt.need_arh==inf.Platform.Win:
            from metaps1.install_win import InstallerWindows
            installer=InstallerWindows(opt, file_name)
        else:
            raise self.InstallException("Удаление для платформы %s не реализована" % opt.need_arh)
        try:
            #получим временную папку и распакуем в нее архив
            #выполним установку
            installer.Remove(cc)
        finally:
            #удалим распакованные данные платформы
            pass

    def __init__(self, opt, file_name):
        logger.info("InstallerBase::__init__()")
        self._opt=opt
        self._file_name=file_name
        self.def_enc=getpreferredencoding() or "UTF-8"
        logger.debug("file_name=%s" % self._file_name)
        logger.debug("def_encoding=%s" % self.def_enc)

    def _install(self, ext, tmp_dir):
        logger.info("InstallerBase::_install()")
        raise Exception("Base installer _install")

    def _remove(self, ext, tmp_dir):
        logger.info("InstallerBase::_remove()")
        raise Exception("Base installer _remove")

    def __call__(self, cc):
        """ установка из архива  """
        logger.info("Installerbase::__call__()s")
        (ext, tmp_dir)=cc.StartInstall(self._opt.need_version, self._file_name)
        try:
            self._install(ext, tmp_dir)
        finally:
            cc.FinishInstall(tmp_dir)

    def Remove(self, cc):
        """ Удаление платформы """
        logger.info("Installerbase::Remove()")
        (ext, tmp_dir)=cc.StartRemove(self._opt.need_version, self._file_name)
        try:
            self._remove(ext, tmp_dir)
        finally:
            cc.FinishRemove(tmp_dir)




