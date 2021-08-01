# -*- coding: utf-8 -*-
from pathlib import Path

class LCache
    def __init__(self, opt):
        self.__base=Path(cache)
        if not self.__base.exists():
            #создаем папку
            self.__base.mkdir(parents=True, exist_ok=True)
        elif pth.is_file(self.__base):
            raise Exception("Невозможно использовать локальный кэш файлов - указанный путь %s является файлом, а не папкой" % self.__base)
        #все нормально - папка существует

    def GetPlatformFilePath(version):
        """ Получение пути, для размещения файлов платформы в локальном кэше """
        res = self.__base / "ent" / version
        res.mkdir(parents=True, exist_ok=True)
        return res

