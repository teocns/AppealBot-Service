# USAGE
# python scan.py --image images/page.jpg

# import the necessary packages
from pyimagesearch.transform import four_point_transform
from skimage.filters import threshold_local
from operator import mul
from collections import namedtuple
import time
import numpy as np
import argparse
import cv2
import imutils
import sys
import os






# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False,help="For single")
# ap.add_argument("-j", "--json", required=False,help="Load from json")
args = vars(ap.parse_args())


# if not args['image'] and not args['json']:
#     exit(0)
    
# if 'json'


## load the image and compute the ratio of the old height
## to the new height, clone it, and resize it
tmpimg = cv2.imread(args["image"])
#image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)






# Resize image
# ratio = image.shape[0] / 500.0
# orig = image.copy()
# image = imutils.resize(image, height=500)

# Increase contrast
# lab= cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
# l, a, b = cv2.split(lab)
# clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(32,32))
# cl = clahe.apply(l)
# limg = cv2.merge((cl,a,b))
# final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

#Show increased contrast
# cv2.imshow('final', final)
# cv2.waitKey(0)

#image = final


#image = cv2.GaussianBlur(image, (11,11), 0)


images = []
images.append(tmpimg)
# files = os.scandir(os.getcwd()+'\\images\\')
# for file in files:
#     images.append(
#         cv2.imread(os.getcwd()+'\\images\\'+file.name)
#     )
    

for image in images:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # # red
    # rmin = gray[..., 0].min()
    # rmax = gray[..., 0].max()
    # # green
    # gmin = gray[..., 1].min()
    # gmax = gray[..., 1].max()
    # # blue
    # bmin = gray[..., 2].min()
    # bmax = gray[..., 2].max()

    # rgbmin_str = ','.join([str(v) for v in [rmin,gmin,bmin]])
    # rgbmax_str = ','.join([str(v) for v in [rmax,gmax,gmax]])
    # print(f"MIN RGB found in GRAYSCALE: {rgbmin_str}"  )
    # print(f"MAX RGB found in GRAYSCALE: {rgbmax_str}"  )
    # rgbmin = np.average([rmin,gmin,bmin])
    # rgbmax = np.average([rmax,gmax,gmax])

    # print(F"MIN : {str(rgbmin)}")
    # print(F"MAX : {str(rgbmax)}")



    # ----------------------------------
    # Calculate average and median color
    # ----------------------------------
    median = int(np.median(gray))
    average_color = int(np.mean(gray))
    image_height,image_width,hierarchy = image.shape
    print(f"Width: {image_width}px\nHeight: {image_height}px")
    print(f"Average: {average_color}px\nMedian: {median}px")
    # cv2.imshow('Edges',gray)
    # cv2.waitKey(0)

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

    crop_threshold = average_color

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

    # cv2.imshow('test',crop_img)
    # cv2.waitKey(0)
    # exit()
        
    # ------------ CALCULATE AVERAGE OF RGB COLORS





    # ------------ IF DIFFERENCE OF COLORS IS HIGH, THEN WE APPLY A STRONG THRESHOLD


    # print(mean)
    # cv2.imshow('Edges',gray)
    # cv2.waitKey(0)

    ret,  mask= cv2.threshold(
        crop_img,
        median * 0.875,
        255,
        cv2.THRESH_BINARY,
    )

    #exit(mask.shape[0:2])
    # Draw black rectagnle around mask
    # cv2.rectangle(
    #     mask,
    #     (0,0),
    #     mask.shape[0:2],
    #     (0,0,0),
    #     2,
    # )

    # cv2.imshow('Edges',mask)
    # cv2.waitKey(0)

    # find the contours in the edged image, keeping only the
    # largest ones, and initialize the screen contour
    
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)


    # Get with the largest area

    for c in cnts:
        cv2.drawContours(crop_img, [c], 0, (0, 128, 0), 2)
        # cv2.imshow("Result", crop_img)
        # cv2.waitKey(0)
        
        
        
        
        #exit (min(c))
        # exit(
        #     findMaxRect(
        #         cv2.contourArea(c)
        #     )
        # )
        
        # rect = cv2.minAreaRect(c)
        # box = cv2.boxPoints(rect)
        # box = np.int0(box)
        
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        rect = cv2.minAreaRect(approx)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        
        cv2.drawContours(original_cropped, [box], 0, (0, 128, 0), 2)
        cv2.imwrite(
            os.getcwd()+"\\images_cropped\\"+str(time.time())+".jpg",
            original_cropped
        )
        # cv2.imshow("Result", original_cropped)
        # cv2.waitKey(0)
        break
        
        
        # Extract the approximate rectangle of the contour from the image
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        box = cv2.rectangle(rect, (x,y), (x+w,y+h), (0,0,255), 2)
        cropped = mask[y: y+h, x: x+w]
        cv2.imshow("Show Boxes", cropped)
        cv2.waitKey(0)



        # Remove black area
        
        approx = cv2.approxPolyDP(saved_c,0.01*cv2.arcLength(saved_c,True),True)
        exit(approx)
        far = approx[np.product(approx,2).argmax()][0]
        exit(far)
        # ymax = approx[approx[:,:,0]==1].max()
        # xmax = approx[approx[:,:,1]==1].max()
        
        xmin = min(far[0],xmax)
        ymin = min(far[1],ymax)
        exit(xmin,xmax,ymin,ymax)

        #box = cv2.boxPoints(rect)
        #box = np.int0(box)
        
        # [x1,y1],[x2,y2],[x3,y3],[x4,y4] = box
        
        # exit (y1)
        # print(box)
        
        #displayimg = cv2.contourArea(c)
        
        displayimg = image.copy()
        
        # draw a green 'nghien' rectangle
        #cv2.drawContours(image, [c], 0, (0, 128, 0), 2)
        # cv2.imshow("Result", image)
        # cv2.waitKey(0)
        
        cv2.drawContours(image, [box], 0, (0, 128, 0), 2)
        cv2.imshow("Result", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        exit()

