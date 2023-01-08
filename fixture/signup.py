

import re
import time


class SignupHelper:

    def __init__(self, app):
        self.app = app

    def new_user(self, username, email, password):
        wd = self.app.wd
        wd.get(self.app.base_url + "/signup_page.php")
        wd.find_element_by_name("username").send_keys(username)
        wd.find_element_by_name("email").send_keys(email)
        wd.find_element_by_css_selector('input[type="submit"]').click()
        mail = self.app.mail.get_mail(username, password, "[MantisBT] Account registration")
        url = self.extract_confirmation_url(mail)
        wd.get(url)
        time.sleep(2)
        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_name("password_confirm").send_keys(password)
        wd.find_element_by_css_selector('input[value="Update User"]').click()


    def extract_confirmation_url(self, text):
        with open("c:/temp/extract_confirmation_url.txt", 'w') as d:
            d.write(str(re.search("http://.*$", text, re.MULTILINE).group(0)))
        return re.search("http://.*$", text, re.MULTILINE).group(0)