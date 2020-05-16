import os
from api import req
import time
import sys
from tempfile import TemporaryDirectory
import urllib
from time import sleep
#sys.path.insert(0, 'C:\\Users\\Teo\\Documents\\GitHub\\AppealBot-Service\\papersheet-detection')
sys.path.insert(0, '/var/appealbot/papersheet-detection/')
from post_detection import getAccurateBox

SLASH = str( '\\' if os.name == 'nt' else '/' )

# Load darknet 

sys.path.insert(0, '/var/AI/darknet/')
import darknet
darknet.performDetect(initOnly=True)
with TemporaryDirectory() as tmpdir:
    while 1:
        selfie = req('get_service_selfies_coordinates_generator')
        if selfie:    
            # Download selfie
            download_url = "https://cdn.appealbot.net/"+selfie['filename']
            tmpdirStr = str(tmpdir.name)
            save_location = tmpdirStr+SLASH+selfie['filename']
            urllib.request.urlretrieve(
                download_url,
                save_location
            )
            print ('[DETECTOR] Performing for '+selfie['filename'])
            detections = darknet.performDetect(save_location)
            #detections = [('papersheet', 0.9260228872299194, (586.1337890625, 1471.395751953125, 992.4650268554688, 593.9584350585938))]
            if len(detections) < 1:
                print ("Not found")
                req('set_service_selfies_coordinates_generator',{
                    'selfie_id': selfie['id'],
                    'coordinates': None
                });
            else:
                # Get detection with highest confidence ( bruh )
                
                detection = sorted(detections,key= lambda x: x[1], reverse = True)[0]
                print(detection)
                confidence = str(int(detection[1]*100)) + "%"
                
                c = getAccurateBox(save_location,{
                    "center_x":detection[2][0],
                    "center_y":detection[2][1],
                    "width":detection[2][2],
                    "height":detection[2][3]
                })
                
                
                x1 = c['p1'][0]
                y1 = c['p1'][1]
                x2 = c['p2'][0]
                y2 = c['p2'][1]
                x3 = c['p3'][0]
                y3 = c['p3'][1]
                x4 = c['p4'][0]
                y4 = c['p4'][1]
                
                coordStr = f"{x1}-{y1}-{x2}-{y2}-{x3}-{y3}-{x4}-{y4}"
                print (f"Found with confidence: {confidence}; Coords: {coordStr}")
                req('set_service_selfies_coordinates_generator',{
                    'selfie_id': selfie['id'],
                    'coordinates': coordStr
                })
        
                    
        sleep(10)
                    

