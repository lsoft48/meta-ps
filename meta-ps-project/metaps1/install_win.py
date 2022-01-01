# -*- coding: utf-8 -*-
import re
import pprint
import sys
import ctypes
from pathlib import Path
import subprocess
#from locale import getpreferredencoding 
import metaps1.info as inf
from metaps1.install import InstallerBase, InstallException

import logging
logger = logging.getLogger(__name__)
#alogger = logging.getLogger("apt")

if inf.platform_linux:
    import sh
else:
    #windows
    pass

import ctypes, sys


class InstallerWindows(InstallerBase):
    @staticmethod
    def getIsAadmin():
        """ Проверка является ли текущий пользователь админом, используется для проверки
        можно ли запустить установку без elevation черезх UAC прав текущего пользователя """
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def _execute_win_cmd(self, script):
        """ Запуск скрипта cmd с админскими правами """
        if not self._opt.inst_exec:
            return
        if self.getIsAadmin():
            #есть админские права - можно запустить установку
            subprocess.call(script)
        else:
            #выполняем rights elevation
            ctypes.windll.shell32.ShellExecuteW(None, "runas", str(script), "", None, 1)

    def __get_msi_name(self):
        """ Получение имени пакета msi используемого для установки"""
        msi="1CEnterprise 8";
        if self._opt.getIsXP():
            msi=msi+"_xp"
        if self._opt.need_bit == 64:
            msi=msi+" (x86-64)";
        msi=msi+".msi"
        return msi

    def __get_vc_redist(self):
        """ Получение имени пакета VC redist """
        res="vc_redist"
        if self._opt.need_bit == 64:
            res=res+".x64";
        res=res+".exe"
        return res

    def __get_transforms(self):
        """ получение списка пакетов транформации"""
        res="adminstallrelogon.mst"
        if self._opt.getIsXP():
            res=res+";1049_xp.mst"
        else:
            res=res+";1049.mst"
        return res

    def __get_user_itf(self):
        """ Получение ключа показа пользовательского интерфейса """
        if self._opt.inst_ui_show==0:
           ui="/qn"
        elif self._opt.inst_ui_show==1:
           ui="/qr"
        else:
           ui=""
        return ui

    def __get_interact(self):
        """ Получение ключа взаимодействия с пользователем """
        if self._opt.inst_user_select:
           interact=""
        else:
           interact="/passive"
        return interact

    def _install(self, ext, tmp_dir):
        """ установка из архива на виндоус или на линукс в wine """
        logger.info("InstallerWindows::_install")
        frm=Path(tmp_dir)
        #соберем специальный установочный скрипт
        #имя msi пакета
        msi=self.__get_msi_name()
        #пакеты трансформации
        mst=self.__get_transforms()
        #опции установки
        inst_opt=self._opt.getWinInstallOptions()

        #взаимодействие с пользователем
        interact=self.__get_interact()

        #показ интерфейса
        ui=self.__get_user_itf()

        #имя redist пакета
        vcredist=self.__get_vc_redist()

        #запись скрипта
        with open(frm / "ls_install.cmd", 'w') as out:
            #переходим в папку с дистрибутивом
            out.write('cd /D "%s"\n' % frm)
            if self._opt.inst_vcredist:
                #устанавливаем vc_redist
                out.write('%s /install /quiet /norestart\n' % (vcredist))
            if self._opt.inst_unintall:
                #сначала команда удаления текущей версии - необходима в случае если до этого начинали установку
                #и уже выполнили трансформацию - повторная транформация произойдет с ошибкой
                out.write('msiexec /x "%s" /norestart %s /Lv ls-uninstall.log %s\n' % (msi, interact, ui))
            #трансформация установки
            out.write('msiexec /jm "%s" /t "%s" /norestart %s /Lv ls-trans.log %s\n' % (msi, mst, interact, ui))
            #выполнение установки
            out.write('msiexec /package "%s" %s /norestart /Lv ls-inst.log %s %s\n' % (msi, interact, ui, inst_opt))
        #запуск скрипта
        self._execute_win_cmd(frm / "ls_install.cmd")

    def _remove(self, ext, tmp_dir):
        """ деинсталляция платформы """
        logger.info("InstallerWindows::_remove")
        frm=Path(tmp_dir)
        #соберем специальный удаляющий скрипт
        #имя msi пакета
        msi=self.__get_msi_name()

        #взаимодействие с пользователем
        interact=self.__get_interact()

        #показ интерфейса
        ui=self.__get_user_itf()

        #запись скрипта
        with open(frm / "ls_remove.cmd", 'w') as out:
            #переходим в папку с дистрибутивом
            out.write('cd /D "%s"\n' % frm)
            #команда удаления текущей версии
            out.write('msiexec /x "%s" /norestart %s /Lv ls-uninstall.log %s\n' % (msi, interact, ui))
        #запуск скрипта
        self._execute_win_cmd(frm / "ls_remove.cmd")

