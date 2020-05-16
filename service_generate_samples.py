import cv2
from api import req
from image_generator import generate
from tempfile import TemporaryDirectory
import time
import os
SLASH = str( '\\' if os.name == 'nt' else '/' )
import urllib





while True:    
    selfie = req('get_generate_sample')
    if selfie:
        print('Generating sample for selfie ID '+str(selfie['id']))
        with TemporaryDirectory() as tmpdir:
            download_url = "https://cdn.appealbot.net/"+selfie['filename']
            tmpdirStr = str(tmpdir)
            save_location = tmpdirStr+SLASH+selfie['filename']
            urllib.request.urlretrieve(
                download_url,
                save_location
            )
            selfie = req('get_generate_sample')
            base64 = generate('1337','@appealbot','Appeal Bot',selfie['coordinates'],save_location)
            req('set_generate_sample',{
                "selfie_id":selfie['id'],
                "base_64":base64,
                "user_id":selfie['user_id']
            })
    else:
        print('Found no selfies to generate samples for. Sleeping 30 seconds.')
        time.sleep(30)