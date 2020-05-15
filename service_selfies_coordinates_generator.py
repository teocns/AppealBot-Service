import os
from api import req
import time
import sys
from tempfile import TemporaryDirectory
import urllib
from time import sleep
sys.path.insert(0, '/var/appealbot/papersheet-detection/')
from post_detection import getAccurateBox

SLASH = str( '\\' if os.name == 'nt' else '/' )

# Load darknet 

sys.path.insert(0, '/var/AI/darknet/')
import darknet
darknet.performDetect(initOnly=True)

while 1:
    
    selfie = req('get_service_selfies_coordinates_generator')
    if selfie:    
        with TemporaryDirectory() as tmpdir:
            # Download selfie
            download_url = "https://cdn.appealbot.net/"+selfie['filename']
            tmpdirStr = str(tmpdir)
            save_location = tmpdirStr+SLASH+selfie['filename']
            urllib.request.urlretrieve(
                download_url,
                save_location
            )
            print ('[DETECTOR] Performing for '+selfie['filename'])
            detections = darknet.performDetect(save_location)
            if len(detections) < 1:
                print ("Not found")
                req('set_service_selfies_coordinates_generator',{
                    'selfie_id': selfie['id'],
                    'coordinates': None
                });
            else:
                # Get detection with highest confidence ( bruh )
                detection = sorted(detections,key= lambda x: x[1], reverse = True)[0]
                confidence = str(int(detection[1]*100)) + "%"
                print (f"Found with confidence: {confidence}")
                realBoxCoordinates = getAccurateBox(save_location,{
                    "center_x":detection[2][0],
                    "center_y":detection[2][1],
                    "width":detection[2][2],
                    "height":detection[2][3]
                })
                coordStr = ""
                for c in realBoxCoordinates:
                    coordStr = coordStr + str(c[0]) + "-" + str(c[1])
                coordStr = coordStr[0:-(len(coordStr)-1)]
                req('set_service_selfies_coordinates_generator',{
                    'selfie_id': selfie['id'],
                    'coordinates': coordStr
                });
                
                
    sleep(10)
                

    