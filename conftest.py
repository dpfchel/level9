# -*- coding: utf-8 -*-
import pytest
import json
from fixture.application import Application
import os.path
import ftputil
fixture = None
target = None

# Функци загрузки конфига
# __file__ = C:\Users\dpf\PycharmProjects\python_training\conftest.py
# os.path.abspath(__file__) = C:\Users\dpf\PycharmProjects\python_training\conftest.py
# os.path.dirname(os.path.abspath(__file__)) = C:\Users\dpf\PycharmProjects\python_training
# os.path.join(os.path.dirname(os.path.abspath(__file__)), request.config.getoption(--target)) = C:\Users\dpf\PycharmProjects\python_training\target.json
def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file, encoding='cp1251') as f:
            target = json.load(f)
    return target

@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))

@pytest.fixture
def app(request, config):
    global fixture
    browser = request.config.getoption('--browser')
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=config['web']['baseUrl'])
    #fixture.session.ensure_login(username=config['web']['username'], password=config['web']['password'])
    return fixture

@pytest.fixture(scope="session", autouse=True) # сработает автоматом, даже если ни в каком тесте не указана
def stop(request):
    def fin():
        #fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='chrome')
    parser.addoption('--target', action='store', default='target.json') #'target.json'
    #parser.addoption('--check_ui', action='store_true') #store_true - автоматом True если опция есть, False если отсутствует


@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config["ftp"]["host"], config["ftp"]["username"], config["ftp"]["password"])
    def fin():
        restore_server_configuration(config["ftp"]["host"], config["ftp"]["username"], config["ftp"]["password"])
    request.addfinalizer(fin)

def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            remote.remove("config_inc.php.bak")
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.bak")
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"), "config_inc.php")


def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.bak", "config_inc.php")

"""@pytest.fixture(scope='session')
def orm(request):
    db_config = load_config(request.config.getoption("--target"))['db']
    ormfixture = ORMFixture(host=db_config['host'], name=db_config['name'], user=db_config['user'],
                          password=db_config['password'])

    #def fin():
    #    ormfixture.destroy()
    #request.addfinalizer(fin)
    return ormfixture
"""

"""@pytest.fixture(scope='session')
def db(request):
    db_config = load_config(request.config.getoption("--target"))['db']
    dbfixture = DbFixture(host=db_config['host'], name=db_config['name'], user=db_config['user'], password=db_config['password'])
    def fin():
        dbfixture.destroy()
    request.addfinalizer(fin)
    return dbfixture"""

"""def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:]) # отбросить 5 символов 'data_'
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
        elif fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:]) # отбросить 5 символов 'data_'
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])

def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata

def load_from_json(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
        return jsonpickle.decode(f.read())"""

"""@pytest.fixture
def check_ui(request):
    return request.config.getoption("--check_ui")"""