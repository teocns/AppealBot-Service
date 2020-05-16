# USAGE
# python scan.py --image images/page.jpg

# import the necessary packages
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




OUTPUT_FOLDER = r"C:\\Users\\Teo\\Documents\\GitHub\\AppealBot-Service\\papersheet-detection\\images_cropped\\"




def generateCoordinates(image,draw = False):
    time.sleep(123)
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

if __name__ == "__main__":
    
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=False,help="For single")
    
    args = vars(ap.parse_args())
    
    ## load the image and compute the ratio of the old height
    ## to the new height, clone it, and resize it

    image = cv2.imread(args["image"])
    image = generateCoords(image)
    cv2.imwrite(
        OUTPUT_FOLDER+str(time.time())+".jpg",
        image
    )
    