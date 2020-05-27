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
		'cookie':'rur=FRC; mid=Xs3vrwALAAFEXqm8CoSf1t6btTnT; ig_did=C0945479-28C7-45E4-A25F-4E6BCC255ECE; urlgen="{\"2604:180:3:376:5639:7bcc:ec03:6abd\": 3842}:1jdnv8:w1O7HNI0-HNpMSlQKhFqlPZR05A"; ds_user_id=31874002324; sessionid=31874002324%3AmzcUxKyrSdXbJu%3A17',
		'proxy_ip_port':'168.235.95.186:46650',
		'proxy_user_pass':'MngbJ3:6PL9EF'
	},
	{
		'cookie':'ig_did=A56068B1-24A3-4F27-BD32-144E52F2CD1F; csrftoken=jWSmxNZQ0slNflXBYII50EDRs5ASRvBn; mid=Xp8JxAALAAFSbjpiQFEY4tlaHmjq; ds_user_id=32069056468; sessionid=32069056468%3A3F4Yb2S17Gpkuy%3A4; urlgen="{\"196.19.178.42\": 19969}:1jdnVs:dTmEOrxb5mVDbtv8IIZG33Fr96o"',
		'proxy_ip_port':'196.19.178.42:8000',
		'proxy_user_pass':'9WTX7a:eGuqLS'
	},
	{
		'cookie':'csrftoken=CpKAkAms5zTWZwUGlnyuOpSVSCKGvsdG; mid=Xs3qQgALAAF-QZ0okkNYmuDS_yhV; ig_did=32ED9DEC-7E2B-4880-A209-08147BE9C340; ds_user_id=31872466402; sessionid=31872466402%3ABUx5oVuOqa2Ie4%3A5; rur=FRC; urlgen="{\"196.19.177.247\": 19969}:1jdnXU:DkH2MKkrw_644yjUNSE2b2OCu-M"',
		'proxy_ip_port':'196.19.177.247:8000',
		'proxy_user_pass':'9WTX7a:eGuqLS'
	},
	{
		'cookie':'csrftoken=TiPm4NstNhVllOWV3x2h1JSPV076u8kE; rur=FRC; mid=Xs3q_wALAAH8oJbWQw7zWP7vvb8c; ig_did=89EE6022-ADAD-4D20-A5B1-91C79F603E4E; ds_user_id=31862268157; sessionid=31862268157%3A4tvYuFe9Bs28NR%3A17; urlgen="{\"196.19.179.157\": 19969}:1jdnaV:RT-rfot3N3aB6h2Nybp2OsDH9rs"',
		'proxy_ip_port':'196.19.179.157:8000',
		'proxy_user_pass':'9WTX7a:eGuqLS'
	},
 	{
		'cookie':'csrftoken=1jfM909jyOrTrmEEoexPKAlLlgL8GAr1; mid=Xs3rVwALAAHtMoTr92ygutZ4-lmw; ig_did=9B9BED04-A3E6-466A-8DD6-8636306E594B; ds_user_id=32224035567; sessionid=32224035567%3AZ2UbbA479tXM3B%3A15; urlgen="{\"196.19.179.154\": 19969}:1jdnbw:6i9cjx-A-oSzXUBLHvPNz3OK42g"',
		'proxy_ip_port':'196.19.179.154:8000',
		'proxy_user_pass':'9WTX7a:eGuqLS'
	}
]
total_proxies = len(proxy_cookie_pairs)
cur_proxy_index = 0

while True:
	cur_proxy_index +=1;
	
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
			url=f'https://www.instagram.com/{username}/',
			headers={
				'cookie': cur_proxy['cookie'],
				'host': 'www.instagram.com',
				'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',

			}
		)
		if 'not-logged-in' in response.text:
			print('Not logged in!! Bad cookies. Status code :'+str(response.status_code))
		
		if response.status_code == 200 and 'window._sharedData = {"' in response.text:
			print(f'[{username}] Is active, confirming unban')
			req(
				'register_unban_confirmation',
				{
					'ig_account_id': afs['id']
				}
			)
		sleep(30)
	else:
		print('Found no accounts..')
		sleep(30)

	
