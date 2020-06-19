from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options
from proxy_handler import ProxyHandler, Proxy

import time
from time import sleep
import random
from selenium.webdriver.common.proxy import Proxy, ProxyType
from proxy_chrome import proxy_chrome
from xvfbwrapper import Xvfb
from helpers import prttime
import os

def submit_form_one(username, fullname, email, proxy):
    options = Options()
    options.headless = False
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ['enable-automation','enable-logging',"ignore-certificate-errors"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = None
    with Xvfb() as xvfb:
        if proxy:
            driver = proxy_chrome(proxy.ip, proxy.port,
                                    proxy.user, proxy.password)
        else:
            driver = webdriver.Chrome(options=options)

        driver.set_page_load_timeout(30)

        driver.get('https://help.instagram.com/contact/1652567838289083')
        driver.implicitly_wait(15)
        driver.find_elements(
            By.XPATH, "//form[@action='/ajax/help/contact/submit/page']//label")[4].click()

        e_fullname = driver.find_elements(
            By.XPATH, "//form[@action='/ajax/help/contact/submit/page']//input")[4]

        e_username = driver.find_elements(
            By.XPATH, "//form[@action='/ajax/help/contact/submit/page']//input")[5]

        e_email = driver.find_elements(
            By.XPATH, "//form[@action='/ajax/help/contact/submit/page']//input")[6]

        e_country = driver.find_elements(
            By.XPATH, "//form[@action='/ajax/help/contact/submit/page']//input")[8]

        e_button = driver.find_elements(
            By.XPATH, "//form[@action='/ajax/help/contact/submit/page']//button")

        e_fullname.send_keys(str(fullname))
        time.sleep(1)
        e_username.send_keys(str(username))
        time.sleep(1)
        e_email.send_keys(str(email))
        time.sleep(1)
        e_country.send_keys('United States')
        time.sleep(1)
        e_country.send_keys(Keys.ENTER)

        time.sleep(1)
        driver.find_element_by_css_selector(
            'form button[type="submit"]').click()

        time.sleep(1)


        result = False
        if len( driver.find_elements( By.XPATH, 
                            "//*[contains(text(),'currently have any known issues to report.')]") ) > 0:
            result = True
        elif len( driver.find_elements( By.XPATH, 
                            "//*[contains(text(),'username or short-link you provided does not belong to an inactive')]") ) > 0:
                result = "is_active"
        elif len( driver.find_elements( By.XPATH, 
                            "//*[contains(text(),'you provided is not a User')]") ) > 0:
                result = "is_inexistent"
        elif len( driver.find_elements( By.XPATH, 
                            "//*[contains(text(),'s you before requesting a review')]") ) > 0:
                result = "confirm_its_you"
        else:
            result = False


        driver.close()
        driver.quit()
        return result



