from operator import mul
from scipy.spatial import distance as dist
from collections import namedtuple
import time
import distutils
import numpy as np
import argparse
import cv2
import imutils
import sys
import os
import re
import json
from os import path

def generateCoordinates(image,draw = False):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # ----------------------------------
    # Calculate average and median color
    # ----------------------------------
    median = int(np.median(gray))
    average_color = int(np.mean(gray))
    

    ret,  gray= cv2.threshold(
        gray,
        median * 0.95,
        255,
        cv2.THRESH_BINARY,
    )

    cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)


    # Get with the largest area

    c = cnts[0]
    
    
    
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    rect = cv2.minAreaRect(approx)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    # cv2.drawContours(asd, [box], 0, (0, 128, 0), 2)
    # cv2.imwrite('test\\detection.jpg',asd)
    if draw:
        cv2.drawContours(image, [box], 0, (0, 128, 0), 2)
    return box


def applyReduction(image,color_threshold):
    image_height,image_width,hierarchy = image.shape
    print(f"Width: {image_width}px\nHeight: {image_height}px")
    print(f"Average: {average_color}px\nMedian: {median}px")

    # ------------------------------------
    # Apply cropping based on median color
    # ------------------------------------

    lookup_x_axis = [
        int(image_width*0.5), # Start from the middle (the most effective)
        int(image_width*0.25),
        int(image_width*0.75),
    ]

    lookup_y_axis = [
        int(image_height*0.5), # Start from the middle (the most effective)
        int(image_height*0.25),
        int(image_height*0.75),
    ]

    crop_threshold = color_threshold

    # Crop from top
    crop_top = 0
    for x in lookup_x_axis:    
        #print (f"Looking up for x:{x}/{image_width}")
        for y in range(0,image_height):
            color = np.mean(image[y][x])
            if color >= crop_threshold and y > crop_top:
                crop_top = y
                break
            
    # Crop from bottom
    crop_bottom = image_height-1
    for x in lookup_x_axis:    
        for y in range(image_height-1,0,-1):
            color = np.mean(image[y][x])
            if color >= crop_threshold and y < crop_bottom:
                crop_bottom = y
                break


    # Crop from left
    crop_left = 0
    for y in lookup_y_axis:    
        for x in range(0,image_width):
            color = np.mean(image[y][x])
            if color >= crop_threshold and x>crop_left:
                crop_left = x
                break
            
    # Crop from right
    crop_right = image_width-1
    for y in lookup_y_axis:    
        for x in range(image_width-1,0,-1):
            color = np.mean(image[y][x])
            if color >= crop_threshold and x<crop_right:
                crop_right = x
                break
            

    print(f"Cropping\\\nTOP={crop_top}\nBOTTOM={crop_bottom}\nLEFT={crop_left}\nRIGHT={crop_right}")

    original_cropped = image[crop_top:crop_bottom, crop_left:crop_right]
    crop_img = gray[crop_top:crop_bottom, crop_left:crop_right]
    return crop_img


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
        
        
    
def order_points(pts):
    # sort the points based on their x-coordinates
    xSorted = pts[np.argsort(pts[:, 0]), :]

    # grab the left-most and right-most points from the sorted
    # x-roodinate points
    leftMost = xSorted[:2, :]
    rightMost = xSorted[2:, :]

    # now, sort the left-most coordinates according to their
    # y-coordinates so we can grab the top-left and bottom-left
    # points, respectively
    leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
    (tl, bl) = leftMost

    # now that we have the top-left coordinate, use it as an
    # anchor to calculate the Euclidean distance between the
    # top-left and right-most points; by the Pythagorean
    # theorem, the point with the largest distance will be
    # our bottom-right point
    D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
    (br, tr) = rightMost[np.argsort(D)[::-1], :]

    # return the coordinates in top-left, top-right,
    # bottom-right, and bottom-left order
    return np.array([tl, tr, br, bl], dtype="float32")
        
# Otherwise it has no detection
    
def getAccurateBox(imagePath,detection):
    img = cv2.imread(imagePath)
    height,width,_ = img.shape
    
    detection_width = max(0,int( detection['width'] ))
    detection_height = max(0,int( detection['height'] ))
    detection_x1 =   max(0,int( detection['center_x'] ) - int(detection_width/2))
    detection_y1 =   max(0,int( detection['center_y'] ) - int(detection_height/2))
    
    old_box = {
        "p1":[detection_x1,detection_y1],
        "p2":[detection_x1+width,detection_y1],
        "p3":[detection_x1+width,detection_y1+height],
        "p4":[detection_x1,detection_y1+height]
    }
 
    print(old_box)
    cropped =  img[detection_y1:detection_y1+detection_height,detection_x1:detection_x1+detection_width]
    
    
    
    box =  generateCoordinates(cropped)
    
    
    box = order_points(box)
    
    DiffX = detection_x1
    DiffY = detection_y1
    
    
    
    def addDiff(p):
        p[0] += DiffX
        p[1] += DiffY
        return p
    
    for i in range (0,len(box)):
        box[i] = addDiff(box[i])
    
    
    
    new_box = old_box
    
    new_box["p1"][0] =  box[0][0]
    new_box["p1"][1] =  box[0][1]
    new_box["p2"][0] =  box[1][0]
    new_box["p2"][1] =  box[1][1]
    new_box["p3"][0] =  box[2][0]
    new_box["p3"][1] =  box[2][1]
    new_box["p4"][0] =  box[3][0]
    new_box["p4"][1] =  box[3][1]
    
    return new_box