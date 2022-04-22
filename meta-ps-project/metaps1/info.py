# -*- coding: utf-8 -*-
import sys
from enum import Enum

version='0.6.1'

platform=sys.platform
platform_linux=platform.startswith('linux')

releases_site="https://releases.1c.ru"

class Platform(Enum):
    """ Варианты платформы/ОС """
    Win      = 1
    LinuxRPM = 2
    LinuxDEB = 3
    Mac      = 4
    Linux    = 5
    @staticmethod
    def GetFromUser(arh):
        arh=arh.lower()
        if arh=="win":
            return Platform.Win
        elif arh=="linux_rpm":
            return Platform.LinuxRPM
        elif arh=="linux_deb":
            return Platform.LinuxDEB
        elif arh=="mac":
            return Platform.Mac
        elif arh=="linux":
            return Platform.Linux
        else:
            raise Exception("Указана неизвестная архитектура платформы %s" % arh)

#список платформ, относящихся к линуксу
list_linux=[Platform.Linux, Platform.LinuxDEB, Platform.LinuxRPM]

class What(Enum):
    """ Варианты что именно скачиваем """
    #список изменений и порядок установки платформы
    Doc         = 1
    #решение текущих проблем с различным СУБД и ОС
    ErrOsDB     = 2
    #тонкий клиент
    Thin        = 3
    #платформа целиком
    Full        = 4
    #клиент платформы
    Client      = 5
    #сервер платформы
    Server      = 6
    #технология внешних компонент
    Ext         = 7
    #демонстрационная база
    Demo        = 8
    #демонстрационная база DT
    DemoDT      = 9
    #файл настроки сортировки для Oracle
    OrSort      = 10
    @staticmethod
    def GetFromUser(what):
        if what=="doc":
            return What.Doc
        elif what=="err_os_db":
            return What.ErrOsDB
        elif what=="thin":
            return What.Thin
        elif what=="full":
            return What.Full
        elif what=="client":
            return What.Client
        elif what=="server":
            return What.Server
        elif what=="ext":
            return What.Ext
        elif what=="demo":
            return What.Demo
        elif what=="demo_dt":
            return What.DemoDT
        else:
            raise Exception("Неизвестный пакет из состава платформы %s" % what)

""" 
	Части платформы, которые требуют установки 
"""
list_4install=[What.Thin, 
               What.Full, 
               What.Client, 
               What.Server]

class WhatInst(Enum):
    """ Варианты что именно устанавливаем """
    #тонкий клиент обычный
    Thin        = 1
    #тонкий клиент фаловый
    ThinFile    = 2
    #толстый клиент
    Thick       = 4
    #сервер
    Server      = 8
    #сервер администрирования
    ServerAdmin = 16
    #расширение веб-сервера
    WS          = 32
    #хранилище
    Storage     = 64
    #админка
    Admin       = 128
    #проверка целостности
    Integrity   = 256
    #JRE
    JRE         = 512


class AWhat(Enum):
    """ Дополнительные варинты загрузки """
    #обычная платформа
    Std         = 1
    #учебная версия
    Teach       = 2
    @staticmethod
    def GetFromUser(what):
        pass


