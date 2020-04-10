from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask, ImageToTextTask
from api import req
import base64
import requests
import time
import os
import warnings
import requests
import json
import re
import sys
from webdrivermanager import ChromeDriverManager
from bs4 import BeautifulSoup
from bs4.element import Comment
from time import sleep

from html.parser import HTMLParser
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import string
import random
import json
from xvfbwrapper import Xvfb
CHANGE_PASS_LLINK = 'https://mail.ru/'


class Browser:
	
	driver = None
	def __init__(self):

		options = Options()
		options.headless = True
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-dev-shm-usage')
		self.driver = webdriver.Chrome(
			options=options
		)
		

	def __enter__(self):
		return self.driver

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.driver.quit()


email = None


def solveCaptcha():

	# anti-captcha.com processing
	api_key = 'f6845a2b33eda8b32448cdce089c5c51'
	captcha_fp = open('captcha.jpg', 'rb')
	client = AnticaptchaClient(api_key)
	task = ImageToTextTask(captcha_fp)
	job = client.createTask(task)
	job.join()
	return job.get_captcha_text()


while True:
	email = req('reset_email_passwords')
	if not email:
		print('No accounts found')
		sleep(30)
		continue

	new_pwd = email['password_to_assign']

	print(f"Assigning {new_pwd} for {email['email']}")
	if (email):
		with Xvfb() as xvfb:
			with Browser() as browser:
				try:
					browser.get('https://mail.ru/')
					element = browser.find_element_by_id('mailbox:login')
					sleep(5)
					element.send_keys(email['email'])
					browser.find_element_by_id(
						'mailbox:submit').click()
					sleep(1)
					browser.find_element_by_id(
						'mailbox:password').send_keys(email['old_email_password'])
					sleep(1)
					browser.find_element_by_id(
						'mailbox:submit').click()
					sleep(5)

					# Check to see if there's any captcha
					ele_captcha = browser.find_elements_by_css_selector(
						".b-captcha img")
					if len(ele_captcha) > 0:
						print('solving captcha')

						pic_url = browser.execute_script("""
						var ele = document.querySelector('.b-captcha img');
						return ele.getAttribute('src')
						""", ele_captcha[0])
						# open tab
						browser.execute_script(
							f"window.open('https:{pic_url}');")
						browser.switch_to.window(
							browser.window_handles[1])
						base64img = browser.execute_script("""
							var c = document.createElement('canvas');
							var ctx = c.getContext('2d');
							var img = document.querySelector('img');
							c.height=img.naturalHeight;
							c.width=img.naturalWidth;
							ctx.drawImage(img, 0, 0,img.naturalWidth, img.naturalHeight);
							var base64String = c.toDataURL().substring(22);
							return base64String;
						""")
						browser.close()
						browser.switch_to.window(
							browser.window_handles[0])
						imgdata = base64.b64decode(base64img)
						filename = 'captcha.jpg'  # I assume you have a way of picking unique filenames
						with open(filename, 'wb') as f:
							f.write(imgdata)
						text = solveCaptcha()
						print(f'Captcha text: {text}')
						# Find captcha input button
						browser.find_element_by_css_selector(
							'input.b-input.b-input_captcha').send_keys(text)
						sleep(1)
						browser.find_element_by_css_selector(
							'form.js-form button[type="submit"]').click()
						sleep(5)

						browser.get(
							'https://e.mail.ru/settings/security?changepass&afterReload=1')
						sleep(5)

						browser.find_element_by_css_selector(
							'[data-test-id="old-password-input"]').send_keys(email['old_email_password'])
						sleep(1)
						browser.find_element_by_css_selector(
							'[data-test-id="new-password-input"]').send_keys(new_pwd)
						sleep(1)
						browser.find_element_by_css_selector(
							'[data-test-id="repeat-password-input"]').send_keys(new_pwd)
						sleep(1)
						browser.find_element_by_css_selector(
							'[data-test-id="password-change-submit"]').click()
						sleep(3)
						req("confirm_reset_email_password",
							{
								'email': email['id'],
								'password': new_pwd
							}
							)
						browser.quit()
				except:
					print ('Failed changing password. Skipping')
	else:
		print('Finished!!')
		break
