import time
import base64
import os

from time import sleep
from time import gmtime, strftime

# LOCAL LIBS


from constants import Constants

from email_handler import EmailHandler
from helpers import prttime
import requests

from api import req

proxy_cookie_pairs = [
	{
		'cookie':'ig_did=FDAA567D-385E-4592-A4E6-5FC6025EDDFB; csrftoken=TaTxj65HDmuByy5ofPAI47vA25y4OJ5o; mid=XpD2WAALAAGk8UmgWqdNxytO5aBs; rur=ATN; ds_user_id=32069056468; sessionid=32069056468%3AyEpQTB7TG5a68z%3A1; urlgen="{\"196.19.178.42\": 19969}:1jN2ND:evVAvAvFVxzfYat9OhMQ8tG2eKU"',
		'proxy_ip_port':'196.19.178.42:8000',
		'proxy_user_pass':'9WTX7a:eGuqLS'
	},
	{
		'cookie':'ig_did=0006B4A0-1276-4A0C-8AB4-A8B9772B222B; csrftoken=Px3j1oDa8EgbK1B4J2JLa6cxkDOoCeXU; rur=FRC; mid=XpD3ZgALAAHKArWb4Eg9iV3Iu7ux; ds_user_id=31872466402; sessionid=31872466402%3AJNh3UnfSAqbp9R%3A1; urlgen="{\"196.19.177.247\": 19969}:1jN2Qv:GX2x-x7diCAe4t8K0NwnhNYrw-U"',
		'proxy_ip_port':'196.19.177.247:8000',
		'proxy_user_pass':'9WTX7a:eGuqLS'
	},
	{
		'cookie':'ig_did=60082014-1E55-4558-A68A-E7BE517D06E6; csrftoken=epbY6w0ccG7fQLkRTCkc0Yd2MhuY6mvv; rur=FRC; mid=XpD37QALAAEKR8m5X9bmRzgUjGK2; ds_user_id=31862268157; sessionid=31862268157%3AgbeuVY3CXvXHQU%3A29; urlgen="{\"196.19.179.157\": 19969}:1jN2Sx:z6UPcbjN8R2yFGDOTkzLHJKpRmw"',
		'proxy_ip_port':'196.19.179.157:8000',
		'proxy_user_pass':'9WTX7a:eGuqLS'
	},
 	{
		'cookie':'ig_did=BC07902C-A6F5-423E-8EE3-3B24EB1379A5; csrftoken=2BOaFjBeiuNBS0KQFPU27Df8ov04D9ct; rur=VLL; mid=XpD4pAALAAFY7yyn2qdEeyzoJfnx; ds_user_id=32224035567; sessionid=32224035567%3AuStXkxqKo9oGsD%3A12; urlgen="{\"196.19.179.154\": 19969}:1jN2WE:NMc9s7Ubtw6VWE2ReaEdzTFZYfs"',
		'proxy_ip_port':'196.19.179.154:8000',
		'proxy_user_pass':'9WTX7a:eGuqLS'
	}
]
total_proxies = len(proxy_cookie_pairs)
cur_proxy_index = 0

while True:
	cur_proxy_index = cur_proxy_index +1;
	
	if cur_proxy_index > total_proxies -1:
		cur_proxy_index = 0
	cur_proxy = proxy_cookie_pairs[cur_proxy_index]
	afs = req('get_for_unban_checker_service')
	if (afs):
		print(f"Checking {afs['username']} with proxy {cur_proxy['proxy_ip_port']}..")
		username = afs['username']

		proxies = {
	  		'https' : f"https://{cur_proxy['proxy_user_pass']}@{cur_proxy['proxy_ip_port']}",
			'http' : f"https://{cur_proxy['proxy_user_pass']}@{cur_proxy['proxy_ip_port']}",
   		} 
		response = requests.get(
			url=f'https://www.instagram.com/{username}/?__a=1',
			headers={
				'cookie': proxy_cookie_pairs[cur_proxy_index]['cookie'],
				'host': 'www.instagram.com',
						'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'
			}
		)
		if response.status_code == 200 and response.text != "{}":
			print(f'[{username}] Is active, confirming unban')
			req(
				'register_unban_confirmation',
				{
					'ig_account_id': afs['id']
				}
			)
		sleep(1)
	else:
		print('Found no accounts..')
		sleep(30)
	
