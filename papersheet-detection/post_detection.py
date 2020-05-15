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
    
    old_box = {
        "p1":[detection_x1,detection_y1],
        "p2":[detection_x1+width,detection_y1],
        "p3":[detection_x1+width,detection_y1+height],
        "p4":[detection_x1,detection_y1+height]
    }
    cropped =  img[detection_y1:detection_y1+detection_height,detection_x1:detection_x1+detection_width]
    
    box =  generateCoordinates(cropped)
    old_box["p1"][0] +=  box[0][2][0]
    old_box["p1"][1] +=  box[0][2][1]
    old_box["p2"][0] -=  box[0][3][0]
    old_box["p2"][1] +=  box[0][3][1]
    old_box["p3"][0] -=  box[0][0][0]
    old_box["p3"][1] -=  box[0][0][1]
    old_box["p4"][0] +=  box[0][1][0]
    old_box["p4"][1] -=  box[0][1][1]
    return old_box