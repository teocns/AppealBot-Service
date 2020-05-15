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




# OUTPUT_FOLDER = r"C:\\Users\\Teo\\Documents\\GitHub\\AppealBot-Service\\papersheet-detection\\images_cropped\\"
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=False,help="For single")
# ap.add_argument("-j", "--json", required=False,help="Load from json")
# args = vars(ap.parse_args())


# if not args['image'] and not args['json']:
#     exit('No parameters supplied')
    

# props = []

# if args['json']:
#     if path.exists(args['json']):
#         raw_json = "";
#         with open(args['json']) as f:
#             raw_json = f.read()
#         # Escape " \ " with " \\ " for windows compatibility
#         props = json.loads(
#             re.sub(
#                 r'(?<!\\)\\(?!\\)',
#                 r'\\\\',
#                 raw_json
#             )
#         )
#     else:
#         exit('JSON file is inexistent')
        
        
    
        
        
# Otherwise it has no detection
    
def getAccurateBox(imagePath,detection):
    img = cv2.imread(imagePath)
    height,width,_ = img.shape
    
    detection_width = int( detection['width'] )
    detection_height = int( detection['height'] )
    detection_x1 =   int( detection['center_x'] ) - int(detection_width/2)
    detection_y1 =   int( detection['center_y'] ) - int(detection_height/2)
    
    cropped =  img[detection_y1:detection_y1+detection_height,detection_x1:detection_x1+detection_width]
    
    return generateCoordinates(cropped)