import sys
# Load darknet 
sys.path.append('/var/AI/darknet/')
import darknet
darknet.performDetect(initOnly=True)

print('Loaded darknet')
import os
from api import req
import time
print('Loading tempfile')
from tempfile import TemporaryDirectory
import urllib
from time import sleep
from helpers import adjustJPEGRotation
print('Importing CV2 papersheet-detection library')

from papersheet_detection import post_detection

SLASH = str( '\\' if os.name == 'nt' else '/' )

print('Beginning API query loop')
while True:
    print('Requesting selfie..')
    selfie = req('get_service_selfies_coordinates_generator')
    if selfie:    
        # Download selfie
        coordStr = ""
        try:
            with TemporaryDirectory() as tmpdir:
                download_url = "https://cdn.appealbot.net/"+selfie['filename']
                tmpdirStr = str(tmpdir.name) if os.name == 'nt' else str(tmpdir)
                save_location = tmpdirStr+SLASH+selfie['filename']
                urllib.request.urlretrieve(
                    download_url,
                    save_location
                )
                
                from PIL import Image
                
                img = adjustJPEGRotation( Image.open(save_location) )
                img.save(save_location,format ="JPEG")
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
                    
                    c = post_detection.getAccurateBox(save_location,{
                        "center_x":detection[2][0],
                        "center_y":detection[2][1],
                        "width":detection[2][2],
                        "height":detection[2][3]
                    })
                    
                    
                    x1 = str(int(c['p1'][0]))
                    y1 = str(int(c['p1'][1]))
                    x2 = str(int(c['p2'][0]))
                    y2 = str(int(c['p2'][1]))
                    x3 = str(int(c['p3'][0]))
                    y3 = str(int(c['p3'][1]))
                    x4 = str(int(c['p4'][0]))
                    y4 = str(int(c['p4'][1]))
                    
                    coordStr = '-'.join([x1,y1,x2,y2,x3,y3,x4,y4])
                    print (f"Found with confidence: {confidence}; Coords: {coordStr}")
        except Exception as ex:
            print (ex)
        req('set_service_selfies_coordinates_generator',{
            'selfie_id': selfie['id'],
            'coordinates': coordStr
        })
    else:
        print ('Server returned no selfie. Sleeping 30 seconds.')              
        sleep(30)
                    

