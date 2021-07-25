# -*- coding: utf-8 -*-
import pprint
from enum import Enum

from version_1c import VerInfoEnterprise

#получение ссылок
#варианты
#bit - разрядность
#       - 32
#       - 64

class Platform(Enum):
    """ Варианты платформы/ОС """
    Win      = 1
    LinuxRpm = 2
    LinuxDeb = 3
    Mac      = 4

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
    #файл настроки сортировки для Oracle
    OrSort      = 9

class AWhat(Enum):
    """ Дополнительные вариныт загрузки """
    #обычная платформа
    Std         = 1
    #учебная версия
    Teach       = 2

# - ссылки на 23.07.2021
def get_link_enterprise_v1(version, what, bit, platform, add):
    v=VerInfoEnterprise(version)
    site="https://releases.1c.ru"
    path="version_file"
    if add=="teach":
        #учебная версия платформы
        nick="nick=PlTr83"
        dir_1="PlTr"
    else:
        nick="nick=Platform83"
        dir_1="Platform"
    ver=v.d_version
    dir_2=v.u_version

    fl_ver=''
    if v.NeedVersionInFile(self):
        fl_ver="_"+v.u_version

    fl_bit=''
    if bit==64:
        fl_bit='64'

    if what="doc":
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.19.1229&path=Platform\8_3_19_1229\1cv8upd_8_3_19_1229.htm
        fl="1cv8upd"
        ext="htm"
        fl_bit=''
    elif what="err_osdb":
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.19.1229&path=Platform\8_3_19_1229\Err_Other.htm
        fl="Err_Other"
        ext="htm"
        #версия в файл не добавляется никогда
        fl_ver=''
        fl_bit=''
    elif what="thin":
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.12.1469&path=Platform\8_3_12_1469\setuptc_8_3_12_1469.rar
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.12.1469&path=Platform\8_3_12_1469\setuptc64_8_3_12_1469.rar
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.12.1469&path=Platform\8_3_12_1469\thin.client_8_3_12_1469.rpm32.tar.gz
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.12.1469&path=Platform\8_3_12_1469\thin.client_8_3_12_1469.deb64.tar.gz
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.19.1229&path=Platform\8_3_19_1229\thin.osx_8_3_19_1229.dmg
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.3.641  &path=Platform\8_3_3_641  \thin.client.deb32.tar.gz
        fl="setuptc"
    elif what="client":
        
    else
        raise "Unknown what (%s)" % what

    return "".join((site, '/', path, '?', nick, '&', ver, '&', "path=", dir_1, '\\', dir_2, '\\', fl, fl_bit, fl_ver, '.', ext))




8.3.12.1469 

https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.19.1229&path=Platform\8_3_19_1229\deb64_8_3_19_1229.tar.gz
https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.3.641  &path=Platform\8_3_3_641\deb64.tar.gz
https://releases.1c.ru/version_file?nick=PlTr83    &ver=8.3.19.1229&path=PlTr\8_3_19_1229\training.deb64.tar.gz



# - получение ссылки на платформу 1С
def GetLinkEnterprise(version, what, bit, platform, add=None):
    return get_link_enterprise_v1(version, what, bit, platform, add)

