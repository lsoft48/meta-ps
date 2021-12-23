# -*- coding: utf-8 -*-
import requests
import http.cookiejar as cjar
import pickle
import re
import pprint
from enum import Enum

import logging
logger = logging.getLogger(__name__)

class Auth1CException(Exception):
    pass

#авторизация на сервере 1С
# - авторизация на 23.07.2021
def auth_v1(user, password, debug):
    sess = requests.session()
    sess.cookies = cjar.LWPCookieJar('tmp')
    r_init = sess.get('https://releases.1c.ru')
    if not r_init.ok:
        raise Auth1CException("Site access error (%s) " % r_init.reason)
    if debug:
        save_cookie(sess, 'init')
    match=re.search('(?<=form method="post" id="loginForm" action=")[^"]+(?=")', r_init.text)
    if not match:
        raise Auth1CException("Site parse error: no action")
    action=match.group(0)
    match=re.search('(?<=input type="hidden" name="execution" value=")[^"]+(?=")', r_init.text)
    if not match:
        raise Auth1CException("Site parse error: no execution")
    ex=match.group(0)
    if user==None or user=="":
        raise Auth1CException("No user selected for 1C portal")
    if password==None or password=="":
        raise Auth1CException("No password for user %s at 1C portal" % user)
    data={'inviteCode':'', 'execution':ex, '_eventId':'submit', 'username':user, 'password':password}
    r_post = sess.post('https://login.1c.ru'+action, data=data)
    if debug:
        save_cookie(sess, 'post')
    if not r_post.ok:
        raise Auth1CException("Site login error (%s)" % r_post.reason)
    found=False
    for cc in sess.cookies:
        if cc.name == 'TGC' and cc.domain == 'login.1c.ru':
            found=True;
            break;
    if not found:
        raise Auth1CException("Site login error - incorrect login/password")
    return sess

# - вызов текущего актуального метода авторизации
def Auth(user, password, debug=False):
    return auth_v1(user, password, debug)

def save_cookie(sess, name):
    fname="cookie-%s" % name
    if isinstance(sess.cookies, cjar.FileCookieJar):
        sess.cookies.save(fname, True, True)
    else:
        with open(fname, 'wb') as f:
            pickle.dump(sess.cookies, f)


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
    
