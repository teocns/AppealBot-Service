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


class FormTwo:
    @staticmethod
    def submit(username, fullname, email, phone_number, appeal_reason, proxy):

        options = Options()
        options.headless = True
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = None
        with Xvfb() as xvfb:
            if proxy:
                driver = proxy_chrome(proxy.ip, proxy.port,
                                        proxy.user, proxy.password)
            else:
                driver = webdriver.Chrome(options=options)

            driver.set_page_load_timeout(30)

            driver.get('https://help.instagram.com/contact/606967319425038?ref=cr')
            driver.implicitly_wait(5)

            # driver.find_elements(
            # 	By.XPATH, "//form[@action='/ajax/help/contact/submit/page']//label")[4].click()

            e_fullname = driver.find_element_by_css_selector('form input[name="name"]')

            e_username = driver.find_element_by_css_selector('form input[name="instagram_username"]')

            e_email = driver.find_element_by_css_selector('form input[name="email"]')
                
            e_mobile_number = driver.find_element_by_css_selector('form input[name="mobile_number"]')

            e_appeal_reason  = driver.find_element_by_css_selector('form textarea[name="appeal_reason"]')


            e_button = driver.find_element_by_css_selector('form button[type="submit"]')

            e_fullname.send_keys(str(fullname))
            time.sleep(1)
            
            e_username.send_keys(str(username))
            time.sleep(1)
            
            e_email.send_keys(str(email))
            time.sleep(1)

            
            e_mobile_number.send_keys(str(phone_number))
            time.sleep(1)
            
            e_appeal_reason.send_keys(str(appeal_reason))
            time.sleep(1)
            
            
            
            driver.find_element_by_css_selector(
                'form button[type="submit"]').click()
            time.sleep(1)

            time.sleep(2)
            result = False
            try:
                driver.find_element(
                    By.XPATH, "//*[contains(text(),'Your report has been submitted. Thanks for contacting Instagram.')]")
                time.sleep(2)
                result = True
            except:
                try:
                    driver.find_element(
                        By.XPATH, "//*[contains(text(),'username or short-link you provided does not belong to an inactive')]")
                    result = "is_active"
                except:
                    try:
                        driver.find_element(
                            By.XPATH, "//*[contains(text(),'you provided is not a User. Please provide a valid User')]")
                        result = "is_inexistent"
                    except:
                        result = False

            driver.close()
            driver.quit()
            return result

