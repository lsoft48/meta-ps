# -*- coding: utf-8 -*-
import pytest
import unittest.mock as mock
import metasites1
import metasites1.connection as s1s

import logging
logger = logging.getLogger(__name__)

@pytest.fixture
def opt_auth(opts):
    return {"user":opts["USER"], "password":opts["PASS"]}

@pytest.fixture
def auth():
    return s1s.AuthBase("test-user", "test-pass")

@pytest.fixture
def mauth(auth):
    #with mock.patch("auth.sess") as sess:
    #    yield auth
    auth.sess=mock.Mock()
    return auth


class Test_ConnectionNet():
    def test_Session(self, opt_auth):
        conn=s1s.Connection(opt_auth["user"], opt_auth["password"])
        assert conn._up_set
        assert not conn._up_tested
        assert not conn._releases_entered

    def test_SessionNoUP(self, opt_auth):
        conn=s1s.Connection()
        assert not conn._up_set
        assert not conn._up_tested
        assert not conn._releases_entered

    def test_MakeSession(self, opt_auth):
        conn=s1s.Connection()
        conn.MakeSession()
        assert conn.sess != None

    @pytest.mark.net
    def test_LoginPassword(self, opt_auth):
        logger.debug("test_LoginPassword")
        conn=s1s.Connection(opt_auth["user"], opt_auth["password"])
        conn.debug=True
        res=conn.LoginREST()
        assert res.ok
        assert res.status_code == 200

    @pytest.mark.net
    def test_LoginHTTPS(self, opt_auth):
        logger.debug("test_Releases")
        conn=s1s.Connection(opt_auth["user"], opt_auth["password"])
        conn.debug=True
        conn.debug_body=True
        res=conn.LoginREST()
        assert res.ok
        res=conn.LoginHTTPS_Read()
        assert res.ok
        res_2=conn.LoginHTTPS_SendfUserPassword(res)
        assert res_2.ok
        res_3=conn.Releases_Read()
        assert res_3.ok
