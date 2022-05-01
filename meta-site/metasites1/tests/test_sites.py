# -*- coding: utf-8 -*-
import pytest
import metasites1
import metasites1.sites as st

import logging
logger = logging.getLogger(__name__)

@pytest.fixture(params=[None, True, False])
def ru(request):
    return request.param


class Test_Sites():
    def test_set_lang(self, ru):
        logger.debug("test_set_lang %s" % ru)
        tst=st.SiteParts()
        tst.set_lang(ru)
        if ru==False:
            assert tst.ru==False
        else:
            assert tst.ru==True
        
    def test_get_login(self, ru):
        logger.debug("test_get_login %s" % ru)
        tst=st.SiteParts(ru)
        if ru==False:
           assert tst.get_login()=="login.1c.eu"
        else:
           assert tst.get_login()=="login.1c.ru"

    def test_get_releases(self, ru):
        logger.debug("test_get_releases %s" % ru)
        tst=st.SiteParts(ru)
        if ru==False:
            assert tst.get_releases()=="releases.1c.eu"
        else:
            assert tst.get_releases()=="releases.1c.ru"

    def test_get_login_auth(self):
        logger.debug("test_get_login_auth")
        tst=st.SiteParts()
        link=str(tst.get_login_auth())
        assert link.startswith("https://")
        assert tst.get_login() in link
        assert tst.get_login_auth()=="https://login.1c.ru/rest/public/user/auth"

