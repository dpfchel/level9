# -*- coding: utf-8 -*-
from selenium import webdriver
from fixture.session import SessionHelper
#from fixture.group import GroupHelper
#from fixture.contact import ContactHelper
from selenium.webdriver.support.ui import Select


import random
import string


class Application:
    def __init__(self, browser, base_url):
        if browser == 'chrome':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
            self.wd = webdriver.Chrome(executable_path=r'c:/Python39/chromedriver.exe')
        elif browser == 'firefox':
            self.wd = webdriver.Firefox(executable_path=r'geckodriver.exe')
        elif browser == 'edge':
            self.wd = webdriver.Edge(executable_path=r'msedgedriver.exe')
        else:
            raise ValueError("Unrecognazed browser %s" % browser)
        #self.wd.implicitly_wait(5)
        self.session = SessionHelper(self)
        #self.group = GroupHelper(self)
        #self.contact = ContactHelper(self)
        self.base_url=base_url

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False


    def count(self, key):  # key = contact - подсчет контактов, key = group - подсчет групп
        wd = self.wd
        if key == 'group':
            self.group.open_groups_page()
        elif key == 'contact':
            self.contact.open_home_page()
        else:
            print('Неверный параметр! key = contact - подсчет контактов, key = group - подсчет групп')
        return len(wd.find_elements_by_name("selected[]"))

    def change_field_value(self, field_name, text):
        wd = self.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def change_field_value_select(self, field_name, text):
        wd = self.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            Select(wd.find_element_by_name(field_name)).select_by_visible_text(text)

    def random_string(prefix, maxlen):
        symbols = string.ascii_letters + string.digits + string.punctuation + " " * 10
        return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

    def random_number(prefix, maxlen):
        symbols = string.digits
        return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

    def open_home_page(self):
        wd = self.wd
        # Если страница не открыта, то откроем страницу
        # menu "home"
        #if not (wd.current_url.endswith("/index.php") and len(wd.find_elements_by_css_selector("[value='Send e-Mail']")) > 0):
        wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()

