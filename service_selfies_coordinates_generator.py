import os
from api import req
import time
import sys
from tempfile import TemporaryDirectory
import urllib

from time import sleep

SLASH = str( '\\' if os.name == 'nt' else '/' )

# Load darknet 

sys.path.insert(0, '/var/AI/darknet/')
import darknet

darknet.performDetect()

exit()
while 1:
    
    data = req('get_service_selfies_coordinates_generator')
    if data:    
        with TemporaryDirectory() as tmpdir:
            for selfie in data:
                # Download selfie
                download_url = "https://cdn.appealbot.net/"+selfie['filename']
                tmpdirStr = str(tmpdir)
                save_location = tmpdirStr+SLASH+selfie['filename']
                urllib.request.urlretrieve(
                    download_url,
                    save_location
                )
                # Load detector (kewl)
                

    