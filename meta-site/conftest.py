# -*- coding: utf-8 -*-
import pytest
import logging
logging.basicConfig(filename='pytest.log', filemode='w', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_opt(name):
    """ часть настроек может быть указана в отдельном файле - прочитаем его
        (заполняем только незаполненные)"""    
    logger.debug("load_opt %s" % name)
    with open(name, "r") as fh:
        lines = fh.readlines()
    res={}
    for ln in lines:
        if ln.startswith('#'):
            #это комментарий
            continue
        if len(ln.strip())==0:
            #пустая строка
            continue
        (name,_,data)=ln.partition('=')
        name=name.upper()
        if len(data)>0:
            data=data.strip()
        res[name]=data
    return res

@pytest.fixture
def opts():
    logger.debug("opts() fixture")
    return load_opt("opt.txt")

def pytest_addoption(parser):
    """ добавление опции для запуска сетевых тестов"""
    logger.debug("pytest_addoption(parser)")
    parser.addoption("--run-net",
                     action="store_true",
                     dest="run_net",
                     default=False,
                     help="run platform tests with network operations")

    parser.addoption("--run-auth",
                     action="store_true",
                     dest="run_auth",
                     default=False,
                     help="run platform tests with 1c site auth")



def pytest_collection_modifyitems(config, items):
    logger.debug("pytest_collection_modifyitems(config, items)")
    if not config.getoption("--run-net"):
        skip_net = pytest.mark.skip(reason="need --run-net option to run")
        for item in items:
            if "net" in item.keywords:
                item.add_marker(skip_net)
    if not config.getoption("--run-auth"):
        skip_auth = pytest.mark.skip(reason="need --run-auth option to run")
        for item in items:
            if "auth" in item.keywords:
                item.add_marker(skip_auth)



