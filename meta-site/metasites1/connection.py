# -*- coding: utf-8 -*-
import requests
import json
import http.cookiejar as cjar
import re
from pathlib import Path
from metasites1.sites import SiteParts

import logging
logger = logging.getLogger(__name__)

class Connection():
    """ используется для подключения и работы с сайтами 1С """

    class Error(Exception):
        pass

    def __init__(self, user=None, password=None):
        logger.debug("Connection.__init__ user=%s" % user)
        self.debug=False
        self.debug_body=False
        self.user=user
        self.password=password
        self.sess=None
        self._sp=SiteParts(True)
        self._up_set=(user != None and len(user)>0) and (password!=None and len(password)>0)
        self._up_tested=False
        self._up_correct=None
        self._releases_entered=False
        self._session_path=Path("sessions")

    def _get_cookie_file(self):
        if self._up_set:
            return self._session_path / self.user
        return "cookie.tmp"

    def VerifyAuth(self):
        logger.debug("VerifyAuth")
        res=self.LoginREST()
        self._up_tested=True
        self._up_correct=res.ok
        return res.ok

    def MakeSession(self, force=False):
        logger.debug("MakeSession")
        if self.sess == None or force:
            self.sess = requests.session()
            self.sess.cookies = cjar.LWPCookieJar(self._get_cookie_file())
            self._session_path.mkdir(parents=True, exist_ok=True)
        return self.sess

    def SaveCookie(self, fn=None):
        logger.debug("SaveCookie fn=%s" % fn)
        if self.sess==None:
            return
        if fn==None:
            self.sess.cookies.save(ignore_discard=self.debug, ignore_expires=self.debug)
        else:
            self.sess.cookies.save(ignore_discard=self.debug, ignore_expires=self.debug, filename="cookie-"+fn+".txt")
    
    def LoadCookie(self, fn=None):
        logger.debug("LoadCookie fn=%s" % fn)
        if fn==None:
            self.sess.cookies.load(ignore_discard=self.debug, ignore_expires=self.debug)
        else:
            self.sess.cookies.load(ignore_discard=self.debug, ignore_expires=self.debug, filename="cookie-"+fn+".txt")

    def LoginREST(self):
        """ Проверка логина/пароля партала 1С """
        logger.debug("LoginREST")
        headers = {"Content-Type": "application/json",
        #           "User-Agent": "1C+Enterprise/8.3",}
        #           "Accept-Encoding": "",
                   "Connection": "keep-alive"}
        data={"login":self.user, "password":self.password}
        data=json.dumps(data)

        if self.debug:
            from http.client import HTTPConnection
            HTTPConnection.debuglevel = 2

        location=self._sp.get_login_auth()
        #location="https://login.1c.ru/rest/public/user/auth"
        req=requests.Request(method="POST", url=location, data=data, headers=headers)
        self.MakeSession()
        preq=self.sess.prepare_request(req)
        r_init = self.sess.send(preq)
        if self.debug:
            if self.debug_body:
                logger.debug(r_init.text)
            self.SaveCookie("login-rest")
        return r_init

    def LoginHTTPS_Read(self):
        """ Чтение главной страницы login """
        logger.debug("LoginHTTPS_Read")
        self.MakeSession()
        r_init = self.sess.get(self._sp.get_login_releases(ru2=False))
        if self.debug:
            if self.debug_body:
                logger.debug(r_init.text)
            self.SaveCookie("https-read")
        return r_init

    def LoginHTTPS_SendfUserPassword(self, main_page):
        logger.debug("LoginHTTPS_SendfUserPassword")
        match=re.search('(?<=form method="post" id="loginForm" action=")[^"]+(?=")', main_page.text)
        if not match:
            raise Connection.Error("Site parse error: no action")
        action=match.group(0)
        match=re.search('(?<=input type="hidden" name="execution" value=")[^"]+(?=")', main_page.text)
        if not match:
            raise Connection.Error("Site parse error: no execution")
        ex=match.group(0)
        data={'inviteCode':'', 'execution':ex, '_eventId':'submit', 'username':self.user, 'password':self.password}
        r_post = self.sess.post("https://"+self._sp.get_login()+action, data=data)
        if self.debug:
            if self.debug_body:
                logger.debug(r_post.text)
            self.SaveCookie("https-sup")
        return r_post

    def Releases_Read(self):
        """ загрузка releases """
        logger.debug("Releases_Read")
        page=self.sess.get("https://"+self._sp.get_releases())
        if self.debug:
            if self.debug_body:
                logger.debug(page.text)
            self.SaveCookie("https-vr")
        return page

    def VerifyReleases(self):
        """ проверка что вход на релизы произведен """
        logger.debug("VerifyReleases")
        page=self.Releases_Read()
        return page.ok

    def ConnectReleases(self):
        """ Подклюяение к сайту releases """
        logger.debug("ConnectReleases")
        if not self._up_set:
            raise Connection.Error("No user/password for releases site")
        if not self._up_tested:
            self.VerifyAuth()
        if not self._up_correct:
            raise Connection.Error("Incorrect user/password for releases site")
        if self._releases_entered:
            return
        if (self._session_path / self.user).is_file():
            #возможно есть уже готовая сессия
            self.LoadCookies()
        r_init=self.LoginHTTPS_Read()
        if not r_init.ok:
            raise Connection.Error("Can't read login page")
        r_post=LoginHTTPS_SendfUserPassword(r_init)
        if not r_init.ok:
            raise Connection.Error("Can't enter login/passoword")
        self.SaveCookie() 
        self._releases_entered=True
        return True
