import numpy as np 
import cv2
# load image
image = cv2.imread('photo.jpg')
# resize to easily view on screen, remove for final processing
image = cv2.resize(image,None,fx=0.2, fy=0.2, interpolation = cv2.INTER_CUBIC)

### remove outer black edge
# create grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# perform threshold
retr , mask = cv2.threshold(gray_image, 190, 255, cv2.THRESH_BINARY)
# remove noise
kernel =  np.ones((5,5),np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
# create emtpy mask
mask_2 = np.zeros(image.shape[:3], dtype=image.dtype)
# find contours
ret, contours, hier = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# draw the found shapes (white, filled in ) on the empty mask
for cnt in contours:
    cv2.drawContours(mask_2, [cnt], 0, (255,255,255), -1)

# invert mask and combine with original image - this makes the black outer edge white
mask_inv_2 = cv2.bitwise_not(mask_2)
tmp = cv2.bitwise_or(image, mask_inv_2)

### Select photo - not inner edge
# create grayscale
gray_image2 = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)
# perform threshold
retr, mask3 = cv2.threshold(gray_image2, 190, 255, cv2.THRESH_BINARY)
# remove noise
maskX = cv2.morphologyEx(mask3, cv2.MORPH_CLOSE, kernel)
# invert mask, so photo area can be found with findcontours
maskX = cv2.bitwise_not(maskX)
# findcontours
ret, contours2, hier = cv2.findContours(maskX, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# select the largest contour
largest_area = 0
for cnt in contours2:
    if cv2.contourArea(cnt) > largest_area:
        cont = cnt
        largest_area = cv2.contourArea(cnt)

# find the rectangle (and the cornerpoints of that rectangle) that surrounds the contours / photo
rect = cv2.minAreaRect(cont)
box = cv2.boxPoints(rect)
box = np.int0(box)
print(rect)

#### Warp image to square
# assign cornerpoints of the region of interest
pts1 = np.float32([box[1],box[0],box[2],box[3]])
# provide new coordinates of cornerpoints
pts2 = np.float32([[0,0],[0,450],[630,0],[630,450]])

# determine and apply transformationmatrix
M = cv2.getPerspectiveTransform(pts1,pts2)
result = cv2.warpPerspective(image,M,(630,450))

#draw rectangle on original image
cv2.drawContours(image, [box], 0, (255,0,0), 2)

#show image
cv2.imshow("Result", result)
cv2.imshow("Image", image)

cv2.waitKey(0)
cv2.destroyAllWindows()