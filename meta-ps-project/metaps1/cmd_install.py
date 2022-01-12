# -*- coding: utf-8 -*-
import sys
import metaps1.links_ent as links
#import metaps1.site_1c as site
from metaps1.cache import LCache

import logging
logger = logging.getLogger(__name__)

def ExecuteInstall(opt, nn):
    """ команда установки платформы """
    logger.info("executing install command")
    try:
        cc=LCache(opt)
        (platform_link, file_name)=links.GetLinkEnterprise(opt.need_version, opt.need_what, opt.need_bit, opt.need_arh)
        if cc.NeedDownload(opt.need_version, file_name):
            #запускаем загрузку только если файл отсутвует в кэше
            ExecuteDownload(opt, nn)
        if cc.NeedDownload(opt.need_version, file_name):
            #файла по прежнему нет в кэше - загрузка не удалась
            raise Exception("Не удалось выполнить загрузку %s" % platform_link)
        #выполняем инсталляцию
        InstallerBase.DoInstall(cc, opt, nn, file_name)
    except InstallerBase.InstallException as e:
        print("Ошибка при выполнении установки: %s" % e)
        logger.exception("Install error")
    except links.LinksException as e:
        print("Ошибка указания версий, платформ или архитектур для установки: %s" % e)
        logger.exception("Links error")
    except:
        logger.exception("Unexpected error in install command")
        raise
