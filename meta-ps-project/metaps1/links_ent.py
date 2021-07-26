# -*- coding: utf-8 -*-
import requests
import re
import pprint
from enum import Enum

from metaps1.version_1c import VerInfoEnterprise

__releases_site="https://releases.1c.ru"

#получение ссылок
#варианты
#bit - разрядность
#       - 32
#       - 64

class Platform(Enum):
    """ Варианты платформы/ОС """
    Win      = 1
    LinuxRPM = 2
    LinuxDEB = 3
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
    path="version_file"
    if add == AWhat.Teach:
        #учебная версия платформы
        nick="nick=PlTr83"
        dir_1="PlTr"
    else:
        nick="nick=Platform83"
        dir_1="Platform"
    ver=v.d_version
    dir_2=v.u_version

    fl_ver=''
    if v.NeedVersionInFile():
        fl_ver="_"+v.u_version

    if bit==64:
        fl_bit='64'
    elif platform == Platform.Win or platform == Platform.Mac:
        fl_bit=''
    else:
        fl_bit='32'

    if what == What.Doc:
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.19.1229&path=Platform\8_3_19_1229\1cv8upd_8_3_19_1229.htm
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.3.641  &path=Platform\8_3_3_641  \1cv8upd.htm
        fl="1cv8upd".join((fl_ver, ".htm"))
    elif what == What.ErrOsDB:
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.19.1229&path=Platform\8_3_19_1229\Err_Other.htm
        fl="Err_Other.htm"
    elif what == What.Thin:
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.12.1469&path=Platform\8_3_12_1469\setuptc_8_3_12_1469.rar
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.3.641  &path=Platform\8_3_3_641  \setuptc.rar
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.12.1469&path=Platform\8_3_12_1469\setuptc64_8_3_12_1469.rar
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.12.1469&path=Platform\8_3_12_1469\thin.client_8_3_12_1469.rpm32.tar.gz
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.12.1469&path=Platform\8_3_12_1469\thin.client_8_3_12_1469.deb64.tar.gz
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.19.1229&path=Platform\8_3_19_1229\thin.osx_8_3_19_1229.dmg
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.3.641  &path=Platform\8_3_3_641  \thin.client.deb32.tar.gz

        if platform == Platform.Win:
            if bit==64 and not v.ExistsThin64Win():
                raise "No 64-bit windows thin client of this version %s" % v.d_version
            fl="".join(("setuptc", fl_bit, fl_ver, ".rar"))
        elif platform == Platform.LinuxDEB:
            if bit==64 and not v.ExistsThin64Linux():
                raise "No 64-bit linux thin client of this version %s" % v.d_version
            fl="".join(("thin.client", fl_ver, "deb", fl_bit, ".tar.gz"))
        elif platform == Platform.LinuxRPM:
            if bit==64 and not v.ExistsThin64Linux():
                raise "No 64-bit linux thin client of this version %s" % v.d_version
            fl="".join(("thin.client", fl_ver, "rpm", fl_bit, ".tar.gz"))
        elif platform == Platform.Mac:
            if not v.ExistsThinMac():
                raise "No mac/os-x thin client of this version %s" % v.d_version
            fl="".join(("thin.osx", fl_ver, ".dmg"))
        else:
            raise "Unknown platform/os (%s)" % platform
    elif what == What.Client:
        pass
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.12.1469&path=Platform\8_3_12_1469\client_8_3_12_1469.deb32.tar.gz
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.12.1469&path=Platform\8_3_12_1469\client_8_3_12_1469.rpm64.tar.gz
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.12.1469&path=Platform\8_3_12_1469\clientosx_8_3_12_1469.dmg
    else:
        raise "Unknown what (%s)" % what
    return "".join((__releases_site, '/', path, '?', nick, '&ver=', ver, '&', "path=", dir_1, '\\', dir_2, '\\', fl))


def GetLinkEnterprise(version, what, bit, platform, add=None):
    """ Получение ссылки на страницу скачивания платформы/ее части """
    return get_link_enterprise_v1(version, what, bit, platform, add)


def GetPlatformListPage(sess, version_main):
    """ Загрузка страницы полного списка платформ указанной версии 83/82... """
    if version_main==83:
        v="83"
    elif version_main==82:
        v="82"
    elif version_main==81:
        v="81"
    elif version_main==80:
        v="80"
    else:
        raise "Unknown main plaform version, must be 83, 82, 81, 80 (%s)" % version_main
    res=sess.get(__releases_site+"/project/Platform%s" % v)
    if not res.ok:
        raise "Error reciving platforms list (%s)" % res.reason
    return res.text

def GetLinksEnterpriseAll(sess, version_main):
    """ Получение версий и ссылок на все имеющиеся платформы """
    txt=GetPlatformListPage(sess, version_main)
    lst=re.findall('(?<=<a href=")(/version_files\?nick=Platform8[0-3]&ver=([^"]+))(?=")', txt) 
    res_list=[]
    for (link,ver) in lst:
        res_list.append((__releases_site+link, ver))
    return res_list
