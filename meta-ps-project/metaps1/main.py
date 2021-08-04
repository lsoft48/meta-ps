# -*- coding: utf-8 -*-
import sys
import os
import pprint
import argparse
import metaps1.info as inf
import metaps1.opt  as options
import metaps1.links_ent as links
import metaps1.site_1c as site
from metaps1.cache import LCache

__arh=['linux', 'linux_deb', 'linux_rpm', 'win', 'mac']
__what=['thin', 'full', 'client', 'server', 'ext', 'demo', 'demo_dt', 'or_sort', 'doc', 'err_os_db']
__arh_help="""
- win - Microsoft Windows 32/64 разрядная
- linux - система Linux, без уточнения используемой системы пакетов, следует использовать для версий платформы начиная с 8.3.20
- linux_deb - система Linux, с форматом пакетов deb - Debian, Ubuntu и т.п.
- linux_rpm - система Linux, с форматом пакетов rpm - CentOs, Red Hat, и т.п.
- mac - компьютеры Apple с операционной системой OSX"""

__what_help="""
- thin - тонкий клиент
- full - платформа целиком
- client - клиент платформы (платформа без сервера)
- server - сервер 1С предприятия
- ext - технология внешних компонент
- demo - демонстрационная база
- demo_dt - демонстрационная база в виде dt файла
- or_sort - порядок сортировки для баз данных Oracle
- doc - инструкция по установке и обновлению
- err_os_db - ошибки проблемы при работе с БД"""

def create_parser():
    parser = argparse.ArgumentParser(add_help = False,
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     #conflict_handler='resolve',
                                     prog="meta-ps",
                                     epilog = """(c) 2021. Л-Софт""",
                                     description="""Утилита автоматизации работы с платформой 1С Предприятие - автоматическое скачивание/установка/удаление"""
    )
    cmd_parsers = parser.add_subparsers(dest='command',
                                        title = 'Доступные команды',
                                        description = 'Одна из перечисленных команд, должна быть указана в командной строке %(prog)s'
    )

    down_parser   = cmd_parsers.add_parser('download',
                                           formatter_class=argparse.RawTextHelpFormatter,
                                           add_help = False,
                                           help = 'Загрузка файлов платформы',
                                           description = "Загрузка файлов платформы с сайта 1С и сохранение в папке загрузки (в кэше загрузки)"
    )
    down_group = down_parser.add_argument_group(title='Параметры')
    down_group.add_argument('-h', '--help', action='help', help='Справка')
    #варианты last|неполная версия 8.3.11 - загружаем последнюю платформу 11-го релиза
    down_group.add_argument('-v', '--version', help='Версия платформы для скачивания (пример: 8.3.16.1148)', metavar="8.X.XX.XXXX")
    down_group.add_argument('-b', '--bit',     help='Разрядность скачиваемых файлов 32/64', type=int, choices=[32, 64], metavar='BIT')
    down_group.add_argument('-a', '--arh',     help="ОС/Архитектура: %s" % __arh_help, type=str, choices=__arh, metavar='ARCH')
    down_group.add_argument('-w', '--what',    help='Что именно скачиваем: %s' % __what_help, type=str, choices=__what, metavar='WHAT')
    down_group.add_argument('-o', '--out',     help='Размещение загруженного файла по указанному пути/в указанном файле', metavar='out-file or out-path')
    down_group.add_argument('-f', '--force',   help='Скачивать принудительно, даже если файл уже имеется', action='store_true')
    down_group.add_argument('-s', '--show',    help='Не скачивать - только показать ссылку(и) для скачивания', action='store_true')

    inst_parser   = cmd_parsers.add_parser('install',
                                           formatter_class=argparse.RawTextHelpFormatter,
                                           add_help = False,
                                           help = 'Установка компонентов платформы',
                                           description = "Установка компонентов платформы (с загрузкой при необходимости с портала 1С)"
    )
    inst_group = inst_parser.add_argument_group(title='Параметры')
    inst_group.add_argument('-h', '--help', action='help', help='Справка')
    inst_group.add_argument('-v', '--version', help='Версия платформы для установки (пример: 8.3.16.1148)')
    inst_group.add_argument('-b', '--bit',     help='Разрядность устанавливаемых файлов 32/64', type=int, choices=[32, 64], metavar='BIT')
    inst_group.add_argument('-a', '--arh',     help="ОС/Архитектура: %s" % __arh_help, type=str, choices=__arh, metavar='ARCH')
    inst_group.add_argument('-w', '--what',    help='Что именно скачиваем: %s' % __what_help, type=str, choices=__what, metavar='WHAT')
    inst_group.add_argument('-n', '--no-load', help='Не обращаться к порталу 1С, установка только с диска', action='store_true', dest="no_load")
    inst_group.add_argument('-i', '--in',      help='Установка из указанной папки/файла', metavar='in-file or in-path')
    inst_group.add_argument('-d', '--no-del',  help='Не удалять распакованные файлы из временной папки', action='store_true', dest="no_del_tmp")

    list_parser   = cmd_parsers.add_parser('list', 
                                           add_help = False,
                                           formatter_class=argparse.RawTextHelpFormatter,
                                           help = 'Получение списков версий платформ',
                                           description = """Получение списков версий платформ:
    - доступных для скачивания/установки с сайта 1С
    - установленных на компьютере"""
    )
    list_group = list_parser.add_argument_group(title='Параметры')
    list_group.add_argument('-h', '--help', action='help', help='Справка')
    list_group.add_argument('-v', '--version', help='Фильтр версий платформ (пример: 8.3)')
    list_group.add_argument('-с', '--count',   help='Выводить последние COUNT версий')

    clear_parser  = cmd_parsers.add_parser('clear',
                                           add_help = False,
                                           help = 'Очистка папки загруженных файлов',
                                           description = "Удаление загруженных ранее файлов платформы (очистка кеша загрузки)"
    )
    clear_group = clear_parser.add_argument_group(title='Параметры')
    clear_group.add_argument('-h', '--help', action='help', help='Справка')


    remove_parser = cmd_parsers.add_parser('remove',
                                           add_help = False,
                                           help = 'Деинсталяция платформы',
                                           description = "Удаление ранее установленной платформы"
    )
    remove_group = remove_parser.add_argument_group(title='Параметры')
    remove_group.add_argument('-h', '--help', action='help', help='Справка')
    remove_group.add_argument('-v', '--version', help='Версия платформы для установки (пример: 8.3.16.1148)')


    pg = parser.add_argument_group(title='Параметры')
    pg.add_argument('-h', '--help',    help = 'Справка', action='help')
    pg.add_argument('-c', '--cache',   help = 'Путь к папке для хранения загруженных файлов (кэш загрузки)', metavar='путь')
    pg.add_argument('-u', '--user',    help = 'Имя пользователя на портале 1С')
    pg.add_argument('-p', '--pass',    help = 'Пароль пользователя на портале 1С', dest='PASS')
    pg.add_argument('-o', '--options', help = 'Файл с настройками имени/пароля/путей', metavar="opt-file", type=argparse.FileType())
    pg.add_argument('-v', '--version',
                    action='version',
                    help = 'Вывести номер версии',
                    version='%(prog)s {}'.format(inf.version))
    return parser

def ExecuteCommand():
    parser = create_parser()
    namespace = parser.parse_args()
    #print (namespace)

    #общие настройки
    opt=options.Options()
    opt.load_params(namespace)
    if namespace.options != None:
        opt.load_file(namespace.options)
    opt.load_env()
    opt.fill_defaults()

    #выполняем команду
    if namespace.command == 'list':
        print("LIST")
    elif namespace.command == 'download':
        #print("DOWNLOAD")
        ExecuteDownload(opt, namespace)
    elif namespace.command == 'install':
        ExecuteInstall(opt, namespace)
    elif namespace.command == 'remove':
        print("REMOVE")
    elif namespace.command == 'clear':
        print("CLEAR")
    else:
         parser.print_help()

def ExecuteDownload(opt, nn):
    #pprint.pprint(nn)
    #pprint.pprint(opt)

    try:
        (platform_link, file_name)=links.GetLinkEnterprise(opt.need_version, opt.need_what, opt.need_bit, opt.need_arh)
        if nn.show:
            print("Найденные ссылка на платформу:")
            print("  %s" % platform_link)
        #pprint.pprint(platform_link)
        sess=site.Auth(opt.username, opt.password)
        down_links=links.GetDownloadLinks(sess, platform_link)
        if len(down_links)==0:
            print("На странице загрузки отсутствуют ссылки для скачивания файла")
            sys.exit(1)
        if nn.show:
            print("Найденные ссылки для скачивания:")
            for ln in down_links:
                print("  %s" % ln)
        #pprint.pprint(down_links)
        cc=LCache(opt)
        tmp_file=cc.StartDownload(opt.need_version, file_name)
        site.DownloadFile(sess, down_links[0], tmp_file)
        cc.FinishDownload(tmp_file)
    except site.Auth1CException as e:
        print("Ошибка авторизации/доступа на сервер (%s)" % e)


def ExecuteInstall(opt, nn):
    try:
        cc=LCache(opt)
        (platform_link, file_name)=links.GetLinkEnterprise(opt.need_version, opt.need_what, opt.need_bit, opt.need_arh)
        if cc.NeedDownload(opt.need_version, file_name):
            ExecuteDownload(opt, nn)
        if cc.NeedDownload(opt.need_version, file_name):
            raise Exception("Не удалось выполнить загрузку %s" % platform_link)
        #выполняем инсталляцию
        import metaps1.install as inst
        inst.DoInstall(cc, opt, nn, file_name)
    except:
        pass
