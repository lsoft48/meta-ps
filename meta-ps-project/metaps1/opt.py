# -*- coding: utf-8 -*-
import sys
import os
import pprint
import argparse
import metaps1.info as inf

import logging
logger = logging.getLogger(__name__)

class Options():
    def __init__(self):
        """ Начальная инициализация всех опций и получений свойств машины
        на которой запущена утилита """
        #уровень лога
        self.log_level = None

        #параметры подключения к серверу
        self.username = None
        self.password = None

        #кэш
        self.cache    = None
        self.no_del_tmp = False

        #параметры "требуемой" платформы
        self.need_version = None
        self.need_bit     = None
        self.need_arh     = None
        self.need_what    = None
        self.need_add     = None

        #не скачивать - просто показать ссылки
        self.no_load_show = False

        #текущая ОС
        self.__is_lin = False
        self.__is_win = False
        self.__is_mac = False
        self.__is_xp  = False
        import platform
        if inf.platform_linux:
            # linux
            self.__is_lin=True
        elif inf.platform == "darwin":
            # OS X
            self.__is_mac=True
        elif inf.platform == "win32" or inf.platform == "cygwin":
            # Windows
            self.__is_win=True
            self.__is_xp=(platform.release() == "XP")

        #настройки установки инсталляторами
        self.__inst_DESIGNERALLCLIENTS=1 
        self.__inst_THICKCLIENT=1 
        self.__inst_THINCLIENTFILE=1 
        self.__inst_THINCLIENT=1 
        self.__inst_WEBSERVEREXT=1 
        self.__inst_SERVER=0 
        self.__inst_CONFREPOSSERVER=0 
        self.__inst_CONVERTER77=0 
        self.__inst_SERVERCLIENT=1 
        self.__inst_LANGUAGES="RU"
        #по умолчанию установка инсталятором не предпологаетвмешательства пользователя
        #но можно отключить и тогда пользователь сможет выбрать что и куда
        self.inst_user_select=False
        #демонстрация интерфейса пользователя при инсталяции:
        # 0 - не показывать
        # 1 - прогресс
        # 2 - полный интерфейс
        self.inst_ui_show=0
        #предварительно выполнить деинсталяцию
        self.inst_unintall=False
        #выполнять запуск скрипта установки - можно оставить только формирование его
        self.inst_exec=True
        #выполнить установку vc redist - можно пропустить установку
        self.inst_vcredist=True

        #разрядность ОС
        self.__is_64=False
        self.__is_32=False
        import platform
        arx=platform.architecture()
        if arx[0]=="64bit":
            self.__is_64=True
        if arx[0]=="32bit":
            self.__is_32=True
        if self.__is_win:
            self.__home=os.environ['USERPROFILE']
        elif self.__is_lin:
            self.__home=os.environ['HOME']

    def __repr__(self):
        return "<Options "+pprint.pformat(vars(self))+" >"

    def getWinInstallOptions(self):
        """ строка настроек установки для инсталлятора Windows"""
        return "DESIGNERALLCLIENTS=%s THICKCLIENT=%s THINCLIENTFILE=%s THINCLIENT=%s WEBSERVEREXT=%s SERVER=%s CONFREPOSSERVER=%s CONVERTER77=%s SERVERCLIENT=%s LANGUAGES=%s" % (
                  self.__inst_DESIGNERALLCLIENTS,
                  self.__inst_THICKCLIENT,
                  self.__inst_THINCLIENTFILE,
                  self.__inst_THINCLIENT,
                  self.__inst_WEBSERVEREXT,
                  self.__inst_SERVER,
                  self.__inst_CONFREPOSSERVER,
                  self.__inst_CONVERTER77,
                  self.__inst_SERVERCLIENT,
                  self.__inst_LANGUAGES,
                 )


    def getIsXP(self):
        """ Возвращает true если запущено под XP"""
        return self.__is_xp

    def load_file(self, fh):
        """ часть настроек может быть указана в отдельном файле - прочитаем его
        (заполняем только незаполненные)"""
        logger.info("loading option file")
        lines = fh.readlines()
        for ln in lines:
            if ln.startswith('#'):
                #это комментарий
                continue
            if len(ln.strip())==0:
                #пустая строка
                continue
            (name,_,data)=ln.partition('=')
            name=name.upper()
            if len(data)>0:
                data=data.strip()
                if name=="USER":
                    self.username=data
                elif name=="PASS":
                    self.password=data
                    data="********"
                elif name=="CACHE":
                    self.cache=data
                elif name=="LOGLEVEL":
                    self.log_level=data.upper()
                    from metaps1 import SetLogLevel
                    SetLogLevel(self.log_level)
                logger.debug("%s=%s" % (name, data))

    def load_params(self, ns):
        """ прочитаем настройки, указанные непосредственно в параметрах """
        logger.info("loading command line params")
        if ns.user != None:
            self.username=ns.user
        if ns.PASS != None:
            self.password=ns.PASS
        if ns.cache != None:
            self.cache=ns.cache
        if ns.LogLevel != 'def':
            self.log_level=str(ns.LogLevel).upper()

        if ns.command in ['install', 'remove']:
            self.no_del_tmp = ns.no_del_tmp
        if ns.command=='download':
            self.no_load_show = ns.show

        #если команда требует параметров платформы 1С
        if ns.command in ['download', 'install', 'remove']:
            # - версия
            if ns.version == 'last':
                raise Exception("Автозаполнение последней версии не реализовано")
            elif ns.version !=None:
                if ns.version.find('?') != -1 or ns.version.find('*') != -1:
                    raise Exception("Шаблоны версий не реализованы")
                else:
                    logger.debug("ns.version=%s" % ns.version)
                    self.need_version=ns.version.strip()
            else:
                raise Exception("Требуется обязательное указание версии платформы 1С")
            # - разрядность
            if ns.bit != None:
                self.need_bit=ns.bit
            else:
                if self.__is_32:
                    self.need_bit=32
                else:
                    self.need_bit=64
            # - архитектура
            if ns.arh!=None:
                self.need_arh=inf.Platform.GetFromUser(ns.arh)
            else:
                if self.__is_win:
                    self.need_arh=inf.Platform.Win
                elif self.__is_mac:
                    self.need_arh=inf.Platform.Mac
                elif self.__is_lin:
                    #TODO: select deb/rpm
                    self.need_arh=inf.Platform.Linux
                else:
                    raise Exception("Не удалось определить архитектуру требуемой платформы")
            #what
            what=getattr(ns, "what", None)
            if what!=None:
                self.need_what=inf.What.GetFromUser(what)
            else:
                self.need_what=inf.What.Full

    def load_env(self):
        """ прочитаем настройки, указанные в переменных окружения
        (заполняем только незаполненные)"""
        logger.info("loading env var params")
        pass
    def fill_defaults(self):
        """ Заполнение значениями по умолчанию незаполненных параметров """
        logger.info("filling params default values")
        if self.cache==None:
            if self.__is_lin:
                self.cache="%s/meta-1c" % self.__home
            elif self.__is_win:
                self.cache="%s/meta-1c" % self.__home
        if self.log_level==None:
            self.log_level="ERROR"


