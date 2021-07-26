# -*- coding: utf-8 -*-
import pprint

class VerInfoEnterprise:
    """ инструменты для работы с версией платформы """
    @staticmethod
    def calc_num(version):
        """ расчет номера версии, который используется в сравнениях """
        if isinstance(version, VerInfoEnterprise):
            res=(version.main*100+version.release)*10000+version.patch
        else:
            v=version.split('.')
            res=((int(v[0])*10+int(v[1]))*100+int(v[2]))*10000+int(v[3])
        return res

    #номер версии, начиная с которой ее вставляют в имя файла
    __num_version_in_file=0
    #номер версии, начиная с которой появился 64-битный тонкий клиент для linux
    _num_version_start_64thin_linux=0
    #номер версии, начиная с которой появился 64-битный тонкий клиент для windows
    _num_version_start_64thin_win=0
    #номер версии, начиная с которой появился тонкий клиент для mac
    _num_version_start_thin_mac=0

    def __init__(self, version):
        ver=version.strip()
        self.d_version=ver
        self.v_list=ver.split('.')
        if self.v_list[0] != '8':
            raise "Unknown platform - must be 8.x (%s)" % ver
        vs=self.v_list[1]
        if vs=='3':
            self.main=83
        elif vs=='2':
            self.main=82
        elif vs=='1':
            self.main=81
        elif vs=='0':
            self.main=80
        else:
            raise "Unknown main version %s " % version
        self.u_version=ver.replace('.','_')
        self.release=int(self.v_list[2])
        self.patch=int(self.v_list[3])
        self.__num=0

    def GetNum(self):
        if self.__num == 0:
            self.__num=VerInfoEnterprise.calc_num(self)
        return self.__num

    def NeedVersionInFile(self):
        """ проверка, что при скачивании версию следует добавлять в имя файла (это пошло с версии 8.3.12.1469)"""
        if self.__num_version_in_file == 0:
            self.__num_version_in_file = self.calc_num("8.3.12.1469")
        return self.GetNum() >= self.__num_version_in_file

    def ExistsThin64Linux(self):
        """ проверка, что существуют версии 64-битного тонкого клиента для linux"""
        if self._num_version_start_64thin_linux == 0:
            self._num_version_start_64thin_linux = self.calc_num("8.3.3.658")
        return self.GetNum() >= self._num_version_start_64thin_linux

    def ExistsThin64Win(self):
        """ проверка, что существуют версии 64-битного тонкого клиента для windows"""
        if self._num_version_start_64thin_win == 0:
            self._num_version_start_64thin_win = self.calc_num("8.3.9.1818")
        return self.GetNum() >= self._num_version_start_64thin_win

    def ExistsThinMac(self):
        """ проверка, что существуют версии тонкого клиента для mac"""
        if self._num_version_start_thin_mac == 0:
            self._num_version_start_thin_mac = self.calc_num("8.3.13.1690")
        if self.d_version in ["8.3.12.1855", "8.3.12.1924"]:
            return True
        return self.GetNum() >= self._num_version_start_thin_mac


