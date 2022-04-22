# -*- coding: utf-8 -*-
import pytest
import unittest.mock as mock
import metaps1
import metaps1.site_1c as s1s

@pytest.fixture
def auth():
    return s1s.AuthBase("test-user", "test-pass")

@pytest.fixture
def mauth(auth):
    #with mock.patch("auth.sess") as sess:
    #    yield auth
    auth.sess=mock.Mock()
    return auth


class Test_AuthLocal():
    def test_init(self, auth):
        assert auth != None
        assert auth.user == "test-user"
        assert auth.password == "test-pass"
        assert auth.sess == None

    def test_init_nouser_nopass(self):
        with pytest.raises(s1s.AuthBase.Error) as e_info:
            auth=s1s.AuthBase(None, "test-pass")
        with pytest.raises(s1s.AuthBase.Error) as e_info:
            auth=s1s.AuthBase("test-user", None)
        with pytest.raises(s1s.AuthBase.Error) as e_info:
            auth=s1s.AuthBase("", "test-pass")
        with pytest.raises(s1s.AuthBase.Error) as e_info:
            auth=s1s.AuthBase("test-user", "")

    def test_make_session(self,auth):
        auth.MakeSession()
        assert auth.sess !=None
        assert auth.sess.cookies !=None

    def test_InitSession(self, mauth):
        mauth.InitSessionRead()
