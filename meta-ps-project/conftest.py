import pytest


def pytest_addoption(parser):
    # добавление опции для запуска сетевых тестов
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

