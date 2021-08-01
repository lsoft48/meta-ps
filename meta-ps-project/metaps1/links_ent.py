# -*- coding: utf-8 -*-
import requests
import re
import pprint
from enum import Enum

import metaps1.info as inf
from metaps1.version_1c import VerInfoEnterprise

#__releases_site="https://releases.1c.ru"

# - ссылки на 23.07.2021
def get_link_enterprise_v1(version, what, bit, platform, add):
    v=VerInfoEnterprise(version)
    path="version_file"
    if add == inf.AWhat.Teach:
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
    elif platform == inf.Platform.Win or platform == inf.Platform.Mac:
        fl_bit=''
    else:
        fl_bit='32'

    if what == inf.What.Doc:
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.19.1229&path=Platform\8_3_19_1229\1cv8upd_8_3_19_1229.htm
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.3.641  &path=Platform\8_3_3_641  \1cv8upd.htm
        fl="".join(("1cv8upd", fl_ver, ".htm"))
        file_name="1cv8up.htm"
    elif what == inf.What.ErrOsDB:
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.19.1229&path=Platform\8_3_19_1229\Err_Other.htm
        fl="Err_Other.htm"
        file_name=fl
    elif what == inf.What.Thin:
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.12.1469&path=Platform\8_3_12_1469\setuptc_8_3_12_1469.rar
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.3.641  &path=Platform\8_3_3_641  \setuptc.rar
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.12.1469&path=Platform\8_3_12_1469\setuptc64_8_3_12_1469.rar
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.12.1469&path=Platform\8_3_12_1469\thin.client_8_3_12_1469.rpm32.tar.gz
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.12.1469&path=Platform\8_3_12_1469\thin.client_8_3_12_1469.deb64.tar.gz
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.19.1229&path=Platform\8_3_19_1229\thin.osx_8_3_19_1229.dmg
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.3.641  &path=Platform\8_3_3_641  \thin.client.deb32.tar.gz
        if platform == inf.Platform.Win:
            if bit==64 and not v.ExistsThinFull64Win():
                raise Exception("No 64-bit windows thin client of this version %s" % v.d_version)
            fl="".join(("setuptc", fl_bit, fl_ver, ".rar"))
            file_name="".join(("setuptc-", str(bit), ".rar"))
        elif platform in inf.list_linux:
            #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.20.1363&path=Platform\8_3_20_1363\thin.client32_8_3_20_1363.tar.gz
            #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.20.1363&path=Platform\8_3_20_1363\thin.client64_8_3_20_1363.tar.gz
            if v.BinFormat4Linux():
                fl="".join(("thin.client", fl_bit, fl_ver, ".tar.gz"))
                file_name="".join(("thin.client-", str(bit), ".tar.gz"))
            else:
                if platform == inf.Platform.LinuxDEB:
                    if bit==64 and not v.ExistsThin64Linux():
                        raise Exception("No 64-bit linux thin client of this version %s" % v.d_version)
                    fl="".join(("thin.client", fl_ver, ".deb", fl_bit, ".tar.gz"))
                    file_name="".join(("thin.client-", str(bit), ".deb.tar.gz"))
                elif platform == inf.Platform.LinuxRPM:
                    if bit==64 and not v.ExistsThin64Linux():
                        raise Exception("No 64-bit linux thin client of this version %s" % v.d_version)
                    fl="".join(("thin.client", fl_ver, ".rpm", fl_bit, ".tar.gz"))
                    file_name="".join(("thin.client-", str(bit), ".rpm.tar.gz"))
                else:
                    raise Exception("No thin client for common Linux platform for version %s Use LinuxDEB or LinuxRPM" % v.d_version)
        elif platform == inf.Platform.Mac:
            if not v.ExistsMac():
                raise Exception("No mac/os-x thin client of this version %s" % v.d_version)
            fl="".join(("thin.osx", fl_ver, ".dmg"))
            fl="".join(("thin.osx.dmg"))
        else:
            raise Exception("Unknown platform/os (%s)" % platform)
    elif what == inf.What.Client:
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.12.1469&path=Platform\8_3_12_1469\client_8_3_12_1469.deb32.tar.gz
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.12.1469&path=Platform\8_3_12_1469\client_8_3_12_1469.rpm64.tar.gz
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.12.1469&path=Platform\8_3_12_1469\clientosx_8_3_12_1469.dmg
        if platform in inf.list_linux:
            if v.BinFormat4Linux():
                raise Exception("No client for any Linux platform for version %s Use full platform instead" % v.d_version)
            else:
                if platform == inf.Platform.LinuxDEB:
                    fl="".join(("client",fl_ver,".deb", fl_bit, ".tar.gz"))
                    file_name="".join(("client-", str(bit),".deb.tar.gz"))
                elif platform == inf.Platform.LinuxRPM:
                    fl="".join(("client",fl_ver,".rpm", fl_bit, ".tar.gz"))
                    file_name="".join(("client-", str(bit),".rpm.tar.gz"))
                else:
                    raise Exception("No client for common Linux platform for version %s Use LinuxDEB or LinuxRPM" % v.d_version)
        elif platform == inf.Platform.Mac:
            if not v.ExistsMac():
                raise Exception("No mac/os-x client of this version %s" % v.d_version)
            fl="".join(("clientosx",fl_ver, ".dmg"))
            file_name="clientosx.dmg"
        elif platform == inf.Platform.Win:
            raise Exception("No client files for windows - use full platform")
        else:
            raise Exception("Unknown platform/os (%s)" % platform)
    elif what == inf.What.Full:
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.13.1690&path=Platform\8_3_13_1690\windows_8_3_13_1690.rar
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.13.1690&path=Platform\8_3_13_1690\windows64full_8_3_13_1690.rar
        if platform == inf.Platform.Win:
            fl_full=''
            if bit==64:
                if not v.ExistsThinFull64Win():
                    raise Exception("No 64-bit windows full platform of this version %s" % v.d_version)
                else:
                    fl_full="full"
            fl="".join(("windows", fl_bit, fl_full, fl_ver, ".rar"))
            file_name="".join(("windows-", str(bit), "-full.rar"))
        elif platform in inf.list_linux:
            if v.BinFormat4Linux():
                #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.20.1363&path=Platform\8_3_20_1363\server32_8_3_20_1363.tar.gz
                #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.20.1363&path=Platform\8_3_20_1363\server64_8_3_20_1363.tar.gz
                fl="".join(("server", fl_bit, fl_ver, ".tar.gz"))
                file_name="".join(("server-", str(bit), ".tar.gz"))
            else:
                raise Exception("No full platform for any Linux till 8.3.20 Use client+server")
        else:
            raise Exception("No full platform for this version %s for platform/os %s" % (v.d_version, platform))
    elif what == inf.What.Server:
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.3.641&path=Platform\8_3_3_641\windows64.rar
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.3.641&path=Platform\8_3_3_641\deb64.tar.gz
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.3.641&path=Platform\8_3_3_641\rpm.tar.gz
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.17.1989&path=Platform\8_3_17_1989\deb_8_3_17_1989.tar.gz
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.17.1989&path=Platform\8_3_17_1989\windows64_8_3_17_1989.rar
        if platform == inf.Platform.Win:
            if bit == 32:
                raise Exception("No server files for windows 32 bit, use full 32 platform")
            fl="".join(("windows64", fl_ver, ".rar"))
            file_name="".join(("windows-64-server.rar"))
        elif platform in inf.list_linux:
            if v.BinFormat4Linux():
                raise Exception("No server for Linux platform since version 8.3.20 Use full platform")
            elif platform == inf.Platform.LinuxDEB:
                fl="".join(("deb", fl_bit, fl_ver, ".tar.gz"))
                file_name="".join(("server-", str(bit), ".deb.tar.gz"))
            elif platform == inf.Platform.LinuxRPM:
                fl="".join(("rpm", fl_bit, fl_ver, ".tar.gz"))
                file_name="".join(("server-", str(bit), ".rpm.tar.gz"))
            else:
                raise Exception("No server for common Linux platform for version %s Use LinuxDEB or LinuxRPM" % v.d_version)
        else:
            raise Exception("No server files for platform %s" % platform)
    elif what == inf.What.Ext:
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.17.1989&path=Platform\8_3_17_1989\addin_8_3_17_1989.zip
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.3.641&path=Platform\8_3_3_641\addin.zip
        fl="".join(("addin", fl_ver, ".zip"))
        file_name="addin.zip"
    elif what == inf.What.Demo:
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.3.641&path=Platform\8_3_3_641\demo.zip
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.19.1150&path=Platform\8_3_19_1150\demo.zip
        fl="demo.zip"
        file_name=fl
    elif what == inf.What.DemoDT:
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.19.1150&path=Platform\8_3_19_1150\demodt_8_3_19_1150.zip
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.8.1747&path=Platform\8_3_8_1747\demodt.zip
        if not v.ExistsDemoDT():
            raise Exception("No demo dt information base for this version %s" % v.d_version)
        fl="".join(("demodt", fl_ver, ".zip"))
        file_name="demodt.zip"
    elif what == inf.What.OrSort:
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.7.1845&path=Platform\8_3_7_1845\Collations.rar
        #https://releases.1c.ru/version_file?nick=Platform83&ver=8.3.19.1229&path=Platform\8_3_19_1229\Collations.rar
        fl="Collations.rar"
        file_name=fl
    else:
        raise Exception("Unknown what (%s)" % what)
    return ("".join((inf.releases_site, '/', path, '?', nick, '&ver=', ver, '&', "path=", dir_1, '\\', dir_2, '\\', fl)), file_name)


def GetLinkEnterprise(version, what, bit, platform, add=None):
    """ Получение ссылки на страницу скачивания платформы/ее части + имени скачиваемого файла"""
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
        raise Exception("Unknown main plaform version, must be 83, 82, 81, 80 (%s)" % version_main)
    res=sess.get(inf.releases_site+"/project/Platform%s" % v)
    if not res.ok:
        raise Exception("Error reciving platforms list (%s)" % res.reason)
    return res.text

def GetLinksEnterpriseAll(sess, version_main):
    """ Получение версий и ссылок на все имеющиеся платформы """
    txt=GetPlatformListPage(sess, version_main)
    lst=re.findall('(?<=<a href=")(/version_files\?nick=Platform8[0-3]&ver=([^"]+))(?=")', txt) 
    res_list=[]
    for (link,ver) in lst:
        res_list.append((inf.releases_site+link, ver))
    return res_list

def GetDownloadLinks(sess, page_link):
    """ Получение списка ссылок на загрузки файлов c выбранной страницы"""
    page=sess.get(page_link)
    if not page.ok:
        raise Exception("Can't load page %s" % page_link)
    #https://dl03.1c.ru/public/file/get/49ea130c-35fc-4de8-9e9d-41c343134acc
    #https://dl04.1c.ru/public/file/get/49ea130c-35fc-4de8-9e9d-41c343134acc
    lst=re.findall('<a\s+href="(https://[^/]+/public/file/get/[^"]+)"', page.text) 
    return lst

