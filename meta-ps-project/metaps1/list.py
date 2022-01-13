# -*- coding: utf-8 -*-
#import re
import pprint
from pathlib import Path
#from locale import getpreferredencoding 
import metaps1.info as inf

import logging
logger = logging.getLogger(__name__)


class ListBase():
    """ Базовый класс для полуения информации об установленных в 
        системе компонентах 
    """
    class ListException(Exception):
        pass

    def __init__(self, opt):
        logger.info("ListBase::__init__()")
        self._opt=opt
        #self.def_enc=getpreferredencoding() or "UTF-8"
        logger.debug("file_name=%s" % self._file_name)
        #logger.debug("def_encoding=%s" % self.def_enc)

    @staticmethod
    def GetLister():
        """ Создани соответсвующего текущей платформе класса,
        выполняющего получение информации о локальнйо системе
        """
        if opt.need_arh==inf.Platform.LinuxDEB:
            from metaps1.list_linux import ListLinuxDeb
            lst=ListLinuxDeb(opt)
        elif opt.need_arh==inf.Platform.Win:
            from metaps1.list_win import ListWindows
            lst=ListWindows(opt)
        else:
            raise ListException("Получение списков для платформы %s не реализована" % opt.need_arh)
        return lst


