# -*- coding: utf-8 -*-
import re
import pprint
from pathlib import Path
from locale import getpreferredencoding 
import metaps1.info as inf
from metaps1.install import InstallerBase

import logging
logger = logging.getLogger(__name__)
#alogger = logging.getLogger("apt")

if inf.platform_linux:
  import sh
else:
  #windows
  pass


class InstallerLinuxDeb(InstallerBase):
    class DebInf:
        def __init__(self, name):
            self.name = name
            self.is_nls = "-nls_" in name.name
            self.installed=False

    def __init__(self, opt, file_name):
        logger.info("InstallerLinuxDeb::__init__()")
        super().__init__(opt, file_name)
        self.alogger = logging.getLogger("apt")
        self.alogger.setLevel(opt.log_level)
        handler=logging.FileHandler("/var/log/meta-ps-apt.log", mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.alogger.addHandler(handler)
        self.alogger.propagate=False

    def _log_sh_res(self, e):
        logger.info("InstallerLinuxDeb::_log_sh_res()")
        self.alogger.error("CMD[%s]: %s" % (e.exit_code, e.full_cmd))
        self.alogger.debug("OUT: %s", e.stdout.decode(self.def_enc, "replace"))
        self.alogger.error("ERR: %s", e.stderr.decode(self.def_enc, "replace"))

    def _apt_update(self):
        """ запуск команды apt update для обновления списков пакетов из репозиториев """
        logger.info("InstallerLinuxDeb::_apt_update()")
        try:
            sh.apt("update", _ok_code=[])
        except sh.ErrorReturnCode_0 as e:
            self._log_sh_res(e)
        except sh.ErrorReturnCode as e:
            logger.error("error updating packet cache (%s)", e)
            self._log_sh_res(e)

    def _apt_install_dep(self):
        """ Запуск команды apt install -f для установки зависимостей """
        logger.info("InstallerLinuxDeb::_apt_install_dep()")
        try:
            sh.apt("install", "-f", "-y", _ok_code=[])
        except sh.ErrorReturnCode_0 as e:
            self._log_sh_res(e)
        except sh.ErrorReturnCode as e:
            logger.error("error installing dependances (%s)", e)
            self._log_sh_res(e)

    def _apt_install_debs(self, debs, flt, find_dep=False):
        """ Установка deb пакетов по списку с фильтром """
        logger.info("InstallerLinuxDeb::_apt_install_debs()")
        deps={}
        for pack in debs:
            if flt(pack):
                try:
                    sh.dpkg("-i", pack.name, _ok_code=[])
                    pack.installed=True
                except sh.ErrorReturnCode_0 as e:
                    pack.installed=True
                    self._log_sh_res(e)
                except sh.ErrorReturnCode as e:
                    if not find_dep:
                        logger.error("error installing %s (%s)", pack.name, e)
                    else:
                        dep_list=self._find_dep_list(pack, e.stderr.decode(self.def_enc, "replace"))
                        deps[str(pack.name)]=dep_list
                        pprint.pprint(dep_list)
                        raise self.InstallException("Need install dependances by hand")
                    self._log_sh_res(e)
        return deps

    def _find_dep_list(self, pack, log):
        """ Выделение из лога списка пакетов, от которых зависит данный """
        logger.info("InstallerLinuxDeb::_find_dep_list(%s)" % pack.name)
        lst=re.findall(" ([^ ]+) depends on ([^ ]+) ", log)
        res=[]
        for fnd in lst:
            logger.debug("%s depends on %s" % fnd)
            if fnd[0]==pack.name:
                res.append(fnd[1])
        return res

    def _install(self, ext, tmp_dir):
        """ установка из deb пакетов на линуксе """
        logger.info("InstallerLinuxDeb::_install()")
        frm=Path(tmp_dir)
        debs=[]
        for pack in frm.glob("*.deb"):
            debs.append(self.DebInf(pack))

        #выполняем обновление локального списка пакетов
        self._apt_update()

        #libwebkitgtk-3.0-0
        #сначала ставим обычные пакеты
        self._apt_install_debs(debs, lambda pack: (not pack.is_nls))

        #добавляем зависимости
        self._apt_install_dep()

        #устанавливаем неустановленные
        self._apt_install_debs(debs, lambda pack: (not pack.is_nls and not pack.installed), True)

        #теперь языковые
        self._apt_install_debs(debs, lambda pack: (pack.is_nls and not pack.installed))

        pprint.pprint(debs)

        res=[]
        for pack in debs:
            if not pack.installed:
                res.append(str(pack.name))
        if len(res)>0:
            raise self.InstallException("Error installing packages: %s" % ", ".join(res))


