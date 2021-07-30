# -*- coding: utf-8 -*-
import sys
import os
import pprint
import argparse
import metaps1.info as inf

class Options():
    def __init__(self):
        """ Начальная инициализация всех опций и получений свойств машины
        на которой запущена утилита """
        #параметры подключения к серверу
        self.username = None
        self.password = None

        #кэш
        self.cache    = None

        #параметры "требуемой" платформы
        self.need_version = None
        self.need_bit     = None
        self.need_arh     = None
        self.need_what    = None
        self.need_add     = None

        #текущая ОС
        self.__is_lin=False
        self.__is_win=False
        self.__is_mac=False
        if sys.platform.startswith('linux'):
            # linux
            self.__is_lin=True
        elif platform == "darwin":
            # OS X
            self.__is_mac=True
        elif platform == "win32" or platform == "cygwin":
            # Windows
            self.__is_win=True

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

    def load_file(self, fh):
        """ часть настроек может быть указана в отдельном файле - прочитаем его
        (заполняем только незаполненные)"""
        lines = fh.readlines()
        for ln in lines:
            if ln.startswith('#'):
                #это комментарий
                continue
            if len(ln.strip())==0:
                #пустая строка
                continue
            (name,_,data)=ln.partition('=')
            if len(data)>0:
                data=data.strip()
                if name=="USER":
                    self.username=data
                elif name=="PASS":
                    self.password=data
                elif name=="CACHE":
                    self.cache=data

    def load_params(self, ns):
        """ прочитаем настройки, указанные непосредственно в параметрах """
        if ns.user != None:
            self.username=ns.user
        if ns.PASS != None:
            self.password=ns.PASS
        if ns.cache != None:
            self.cache=ns.cache
        #если команда требует параметров платформы 1С
        if ns.command in ['download', 'install']:
            # - версия
            if ns.version == 'last':
                raise Exception("Автозаполнение последней версии не реализовано")
            elif ns.version !=None:
                if ns.version.find('?') != -1 or ns.version.find('*') != -1:
                    raise Exception("Шаблоны версий не реализованы")
                else:
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
            if ns.what!=None:
                self.need_what=inf.What.GetFromUser(ns.what)
            else:
                self.need_what=inf.What.Full

    def load_env(self):
        """ прочитаем настройки, указанные в переменных окружения
        (заполняем только незаполненные)"""
        pass
    def fill_defaults(self):
        """ Заполнение значениями по умолчанию незаполненных параметров """
        if self.cache==None:
            if self.__is_lin:
                self.cache="%s/meta-1c" % self.__home
            elif self.__is_win:
                self.cache="%s/meta-1c" % self.__home

