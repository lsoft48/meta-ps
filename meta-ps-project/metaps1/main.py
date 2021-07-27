# -*- coding: utf-8 -*-
import sys
import argparse
import metaps1.info as inf

def create_parser():
    parser = argparse.ArgumentParser(add_help = False,
                                     prog="meta-ps",
                                     epilog = """(c) 2021. Л-Софт""",
                                     description="""Утилита автоматизации работы с платформой 1С Предприятие - автоматическое скачивание/установка/удаление"""
    )
    cmd_parsers = parser.add_subparsers(dest='command',
                                        title = 'Доступные команды',
                                        description = 'Одна из перечисленных команд, должна быть указана в командной строке %(prog)s'
    )

    list_parser   = cmd_parsers.add_parser('list', 
                                           add_help = False,
                                           help = 'Получение списков версий плаформ',
                                           description = "Получение списков версий платформ:\r\n"
                                                         "- доступных для скачивания/установки с сайта 1С\r\n"
                                                         "- установленных на компьютере"
    )
    list_group = list_parser.add_argument_group(title='Параметры')
    list_group.add_argument('--help', '-h', action='help', help='Справка')

    clear_parser  = cmd_parsers.add_parser('clear')
    down_parser   = cmd_parsers.add_parser('download')
    inst_parser   = cmd_parsers.add_parser('install')
    remove_parser = cmd_parsers.add_parser('remove')

    pg = parser.add_argument_group(title='Параметры')
    pg.add_argument ('--help', '-h', action='help', help='Справка')
    pg.add_argument('-c', '--cache')
    pg.add_argument('-u', '--user')
    pg.add_argument('-p', '--pass')
    pg.add_argument('--version', 
                    action='version',
                    help = 'Вывести номер версии',
                    version='%(prog)s {}'.format(inf.version))
    return parser

def ExecuteCommand():
    parser = create_parser()
    namespace = parser.parse_args()
    #print (namespace)

    if namespace.command == 'list':
        print("LIST")
    elif namespace.command == 'download':
        print("DOWNLOAD")
    elif namespace.command == 'install':
        print("INSTALL")
    elif namespace.command == 'remove':
        print("REMOVE")
    elif namespace.command == 'clear':
        print("CLEAR")
    else:
         parser.print_help()


#    print("(c) 2021 LSoft 1C Enterprise Platform Installer")


