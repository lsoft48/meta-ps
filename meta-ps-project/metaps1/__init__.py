# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)
handeler=logging.FileHandler("/var/log/meta-ps.log", mode='w')
handeler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handeler)

def SetLogLevel(level):
    logger.setLevel(level)

import metaps1.info as inf

__version__ = inf.version

