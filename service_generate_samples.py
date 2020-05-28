import cv2
from api import req
from image_generator import generate
from tempfile import TemporaryDirectory
import time
import os
SLASH = str( '\\' if os.name == 'nt' else '/' )
import urllib
from helpers import adjustJPEGRotation




while True:
    try:    
        selfie = req('get_generate_sample')
        if selfie:
            print('Generating sample for selfie ID '+str(selfie['id']))
            import requests
            from io import BytesIO
            download_url = "https://cdn.appealbot.net/"+selfie['filename']
            response = requests.get(
                download_url
            )
            
            vanilla_selfie_buffer = BytesIO(response.content)
            
            #vanilla_selfie_base64 = base64.b64encode(vanilla_selfie_buffer.getvalue())
            from PIL import Image, ExifTags
            img =  adjustJPEGRotation( Image.open(vanilla_selfie_buffer) )
            
            base64 = generate('1337','@appealbot','Appeal Bot',selfie['coordinates'],img)
            
            
            print('Sample generated, sending feedback to backend api')
            req('set_generate_sample',{
                "selfie_id":selfie['id'],
                "base_64":base64,
                "user_id":selfie['user_id']
            })
        else:
            print('Found no selfies to generate samples for. Sleeping 30 seconds.')
            time.sleep(30) 
    except Exception as ex:
        print (ex)
    