from operator import mul
from collections import namedtuple
import time
import numpy as np
import argparse
import cv2
import imutils
import sys
import os
import re
import json
from os import path
from coordinator import generateCoordinates


OUTPUT_FOLDER = r"C:\\Users\\Teo\\Documents\\GitHub\\AppealBot-Service\\papersheet-detection\\images_cropped\\"
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False,help="For single")
ap.add_argument("-j", "--json", required=False,help="Load from json")
args = vars(ap.parse_args())


if not args['image'] and not args['json']:
    exit('No parameters supplied')
    

props = []

if args['json']:
    if path.exists(args['json']):
        raw_json = "";
        with open(args['json']) as f:
            raw_json = f.read()
        # Escape " \ " with " \\ " for windows compatibility
        props = json.loads(
            re.sub(
                r'(?<!\\)\\(?!\\)',
                r'\\\\',
                raw_json
            )
        )
    else:
        exit('JSON file is inexistent')

for prop in props:
    if len(prop['objects']) >= 1:
        # Get the detection with maximum confidence
        detection = sorted(
            prop['objects'],
            key = lambda x: x['confidence'],
            reverse = True
        )[0]
        img = cv2.imread(prop["filename"])
        height,width,_ = img.shape
        
        detection_width = int( width * detection['relative_coordinates']['width'] )
        detection_height = int( height * detection['relative_coordinates']['height'] )
        detection_x1 =   int( np.abs((detection['relative_coordinates']['center_x'] * width) - (detection_width/2)))
        detection_y1 =   int( np.abs( (detection['relative_coordinates']['center_y'] * height) - (detection_height/2)))
        
        cropped =  img[detection_y1:detection_y1+detection_height,detection_x1:detection_x1+detection_width]
        
        coords = generateCoordinates(cropped)
        exit(coords)
        # cv2.imwrite(
        #     OUTPUT_FOLDER+str(time.time())+".jpg",
        #     cropped
        # )
        #exit()
        ##exit([detection_x1,detection_y1,detection_width,detection_height])
        
        
    # Otherwise it has no detection