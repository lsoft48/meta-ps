# -*- coding: utf-8 -*-
import requests
import http.cookiejar as cjar
import pickle
import re
import pprint
from enum import Enum

import logging
logger = logging.getLogger(__name__)

class AuthBase():
    """ авторизация на сервере 1С """
    class Error(Exception):
        pass

    # - вызов текущего актуального метода авторизации
    @staticmethod
    def Auth(user, password, debug=False):
        auth=Auth_v1(user, password, debug)
        return auth.Connect()

    def __init__(self, user, password, debug=False):
        self.user     = user
        self.password = password
        self.debug    = debug
        self.sess     = None
        if self.user==None or self.user=="":
            raise AuthBase.Error("No user selected for 1C portal")
        if self.password==None or self.password=="":
            raise AuthBase.Error("No password for user %s at 1C portal" % self.user)

    def save_cookie(self, name):
        fname="cookie-%s" % name
        if isinstance(self.sess.cookies, cjar.FileCookieJar):
            self.sess.cookies.save(fname, True, True)
        else:
            with open(fname, 'wb') as f:
                pickle.dump(self.sess.cookies, f)

    def MakeSession(self):
        self.sess = requests.session()
        self.sess.cookies = cjar.LWPCookieJar('tmp')

    def InitSessionRead(self):
        r_init = self.sess.get('https://releases.1c.ru')
        if not r_init.ok:
            raise AuthBase.Error("Site access error (%s) " % r_init.reason)
        if self.debug:
            save_cookie(self.sess, 'init')
        return r_init

class Auth_v1(AuthBase):
    """ авторизация на 23.07.2021 """
    def Connect(self):
        self.MakeSession()
        r_init=self.InitSessionRead()

        match=re.search('(?<=form method="post" id="loginForm" action=")[^"]+(?=")', r_init.text)
        if not match:
            raise AuthBase.Error("Site parse error: no action")
        action=match.group(0)
        match=re.search('(?<=input type="hidden" name="execution" value=")[^"]+(?=")', r_init.text)
        if not match:
            raise AuthBase.Error("Site parse error: no execution")
        ex=match.group(0)
        data={'inviteCode':'', 'execution':ex, '_eventId':'submit', 'username':self.user, 'password':self.password}
        r_post = self.sess.post('https://login.1c.ru'+action, data=data)
        if self.debug:
            self.save_cookie('post')
        if not r_post.ok:
            raise AuthBase.Error("Site login error (%s)" % r_post.reason)
        found=False
        for cc in sess.cookies:
            if cc.name == 'TGC' and cc.domain == 'login.1c.ru':
                found=True;
                break;
        if not found:
            raise AuthBase.Error("Site login error - incorrect login/password")
        return self.sess

def DownloadFile(sess, link, file_to):
    """ Загрузка файла с портала 1С """
    for cnt in range(1, 5):
        try:
            if cnt > 1:
                time.sleep(10)  # 10 seconds wait time between downloads
            with sess.get(link, stream=True) as resp:
                resp.raise_for_status()
                with open(file_to, 'wb') as of:
                    for ch in resp.iter_content(chunk_size=1024*1024):
                        of.write(ch)
                        print(".", end="", flush=True)
                    print("\nFinished")
                #logger.info('Download finished successfully')
                return file_to
        except Exception as ex:
            #logger.error(f'Attempt #{attempt} failed with error: {ex}')
            raise Exception(f'Attempt #{cnt} failed with error: {ex}')

