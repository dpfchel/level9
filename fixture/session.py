
import time

class SessionHelper:

    def __init__(self, app):
        self.app = app

    def login(self, username, password):
        wd = self.app.wd
        self.app.open_home_page()
        time.sleep(1)
        wd.find_element_by_xpath("//input[@name='username']").click()
        wd.find_element_by_xpath("//input[@name='username']").clear()
        wd.find_element_by_xpath("//input[@name='username']").send_keys(username)
        #wd.find_element_by_name("username").click()
        #wd.find_element_by_name("username").clear()
        #wd.find_element_by_name("username").send_keys(username)
        wd.find_element_by_name("password").clear()
        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_xpath("//input[@value='Login']").click()

    def logout(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Logout").click()

    def ensure_logout(self):
        wd = self.app.wd
        if self.is_logged_in():
            self.logout()

    def is_logged_in(self):
        wd = self.app.wd
        return len(wd.find_elements_by_link_text("Logout")) > 0

    def is_logged_in_as(self, username):
        wd = self.app.wd
        return self.get_logged_user() == username

    def get_logged_user(self):
        wd = self.app.wd
        return wd.find_element_by_css_selector("td.login-info-left span").text

    def ensure_login(self, username, password):
        wd = self.app.wd
        if self.is_logged_in():
            if self.is_logged_in_as(username):
                return    # выход из метода, если залогинен именно username
            else:
                self.logout() # если залогин, но не username - выйдем
        self.login(username, password)  # 1) если пользователь не залогинен, то логинемся, 2) или через if-else