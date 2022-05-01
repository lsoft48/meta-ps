# -*- coding: utf-8 -*-
import sys

class SiteParts():
    def __init__(self, ru=True, ru2=True):
        self.set_lang(ru, ru2)

    def set_lang(self, ru=True, ru2=True):
        if ru==None:
            self.ru=True
        else:
            self.ru=ru
        if ru2==None:
            self.ru2=True
        else:
            self.ru2=ru2

    def is_ru(self, ru):
        if ru==None:
           return self.ru
        return ru

    def get_login(self, ru=None):
        if self.is_ru(ru):
           return SiteParts_RU.login
        else:
           return SiteParts_EU.login

    def get_releases(self, ru=None):
        if self.is_ru(ru):
           return SiteParts_RU.releases
        else:
           return SiteParts_EU.releases

    def get_login_auth(self, ru=None):
        return "https://"+self.get_login(ru)+"/rest/public/user/auth"

    def get_login_releases(self, ru=None, ru2=None):
        if ru2==None:
           ru2=self.ru2
        return 'https://'+self.get_login()+'/login?service=https%3A%2F%2F'+self.get_releases(ru2)+'%2Fpublic%2Fsecurity_check'


class SiteParts_RU(SiteParts):
    releases  = "releases.1c.ru"
    downloads = "downloads.1c.ru"
    login     = "login.1c.ru"
    portal    = "portal.1c.ru"

class SiteParts_EU(SiteParts):
    releases  = "releases.1c.eu"
    downloads = "downloads.1c.eu"
    login     = "login.1c.eu"
    portal    = "portal.1c.eu"

