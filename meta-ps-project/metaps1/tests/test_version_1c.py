# -*- coding: utf-8 -*-
from unittest import TestCase

import metaps1
import metaps1.version_1c as tst

class Test_version(TestCase):
    def setUp(self):
        self.v1=tst.VerInfoEnterprise("8.3.13.1690")
        self.v2=tst.VerInfoEnterprise("8.2.8.1121")
        self.v3=tst.VerInfoEnterprise("8.3.10.2561")
        self.v4=tst.VerInfoEnterprise("8.3.3.641")
        self.v5=tst.VerInfoEnterprise("8.3.20.1789")

    def test_create_version_1(self):
        ver=self.v1
        self.assertEqual(ver.main, 83)
        self.assertEqual(ver.release, 13)
        self.assertEqual(ver.patch, 1690)
        self.assertEqual(ver.u_version, "8_3_13_1690")

    def test_create_version_2(self):
        ver=self.v2
        self.assertEqual(ver.main, 82)
        self.assertEqual(ver.release, 8)
        self.assertEqual(ver.patch, 1121)
        self.assertEqual(ver.u_version, "8_2_8_1121")

    def test_calc(self):
        c1=self.v1.GetNum()
        c2=self.v2.GetNum()
        self.assertGreater(c1, c2)

    def test_NeedVersionInFile(self):
        self.assertTrue(self.v1.NeedVersionInFile())
        self.assertFalse(self.v3.NeedVersionInFile())

    def test_ExistsThin64Linux(self):
        self.assertTrue(self.v1.ExistsThin64Linux())
        self.assertFalse(self.v4.ExistsThin64Linux())

    def test_ExistsThinFull64Win(self):
        self.assertTrue(self.v1.ExistsThinFull64Win())
        self.assertTrue(self.v3.ExistsThinFull64Win())
        self.assertFalse(self.v4.ExistsThinFull64Win())

    def test_ExistsMac(self):
        self.assertTrue(self.v1.ExistsMac())
        self.assertFalse(self.v3.ExistsMac())

    def test_ExistsDemoDT(self):
        self.assertTrue(self.v3.ExistsDemoDT())
        self.assertFalse(self.v4.ExistsDemoDT())

    def test_BinFormat4Linux(self):
        self.assertTrue(self.v5.BinFormat4Linux())
        self.assertFalse(self.v1.BinFormat4Linux())
