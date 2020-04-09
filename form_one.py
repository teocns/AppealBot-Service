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



class FormOne:
	@staticmethod
	def submit(username, fullname, email, proxy):

		options = Options()
		options.headless = True
		driver = None
		
		if False:
			driver = proxy_chrome(proxy.ip, proxy.port,
								  proxy.user, proxy.password)
		else:
			driver = webdriver.Chrome(options=options)
		
		driver.set_page_load_timeout(30)

		driver.get('https://help.instagram.com/contact/1652567838289083')
		driver.implicitly_wait(5)
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

		e_fullname.send_keys(fullname)
		time.sleep(1)
		e_username.send_keys(username)
		time.sleep(1)
		e_email.send_keys(email)
		time.sleep(1)
		e_country.send_keys('United States')
		time.sleep(1)
		e_country.send_keys(Keys.ENTER)

		time.sleep(1)
		driver.find_element_by_css_selector(
			'form button[type="submit"]').click()

		time.sleep(5)
		result = False
		try:
			driver.find_element(
				By.XPATH, "//p[contains(text(),'currently have any known issues to report.')]")
			time.sleep(2)
			result = True
		except:
			try:
				driver.find_element(
					By.XPATH, "//div[contains(text(),'Instagram Account is active')]")
				result = "is_active"
			except:
				try:
					driver.find_element(
						By.XPATH, "//div[contains(text(),'Incorrect Instagram input')]")
					result = "is_inexistent"
				except:
					result = False

		driver.close()
		driver.quit()
		return result
