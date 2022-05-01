# -*- coding: utf-8 -*-
import sys
from enum import Enum

version='0.0.1'

platform=sys.platform
platform_linux=platform.startswith('linux')

class SiteParts():
    pass

class SiteParts_RU():
    releases  = "releases.1c.ru"
    downloads = "downloads.1c.ru"
    login     = "login.1c.ru"
    portal    = "portal.1c.ru"

class SiteParts_EU():
    releases  = "releases.1c.eu"
    downloads = "downloads.1c.eu"
    login     = "login.1c.eu"
    portal    = "portal.1c.eu"

