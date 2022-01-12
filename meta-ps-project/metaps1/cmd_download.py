# -*- coding: utf-8 -*-
import sys
import metaps1.links_ent as links
import metaps1.site_1c as site
from metaps1.cache import LCache

import logging
logger = logging.getLogger(__name__)

def ExecuteDownload(opt, nn):
    """ Команда скачивания файлов платформы """
    logger.info("executing download command")
    try:
        (platform_link, file_name)=links.GetLinkEnterprise(opt.need_version, opt.need_what, opt.need_bit, opt.need_arh)
        logger.debug("platform link = %s" % platform_link)
        logger.debug("downloading element file name = %s" % file_name)
        if opt.no_load_show:
            print("Найденные ссылка на платформу:")
            print("  %s" % platform_link)
        sess=site.Auth(opt.username, opt.password)
        down_links=links.GetDownloadLinks(sess, platform_link)
        if len(down_links)==0:
            print("На странице загрузки отсутствуют ссылки для скачивания файла")
            sys.exit(1)
        if opt.no_load_show:
            print("Найденные ссылки для скачивания:")
            for ln in down_links:
                print("  %s" % ln)
        else:
            print("Выполняем загрузку с портала 1С")
            cc=LCache(opt)
            tmp_file=cc.StartDownload(opt.need_version, file_name)
            site.DownloadFile(sess, down_links[0], tmp_file)
            cc.FinishDownload(tmp_file)
    except site.Auth1CException as e:
        print("Ошибка авторизации/доступа на сервер (%s)" % e)
        logger.exception("Auth error: %s" % e)
    except links.LinksException as e:
        print("Ошибка указанаия версий, платформ или архитектур для загрузки: %s" % e)
        logger.exception("Links error")
    except:
        logger.exception("Unexpected error in download command")
        raise
