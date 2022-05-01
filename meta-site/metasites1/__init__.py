# -*- coding: utf-8 -*-
import logging
import metasites1.info as inf

logger = logging.getLogger(__name__)
if inf.platform_linux:
    handeler=logging.FileHandler("/var/log/meta-site.log", mode='w')
else:
    handeler=logging.FileHandler("meta-site.log", mode='w')
handeler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handeler)

def SetLogLevel(level):
    logger.setLevel(level)

__version__ = inf.version

