import cv2
import numpy as np
image = cv2.imread('stack.jpg',-1)
paper = cv2.resize(image,(500,500))
ret, thresh_gray = cv2.threshold(cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY),
                        200, 255, cv2.THRESH_BINARY)
contours, hier = cv2.findContours(thresh_gray, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
for c in contours:
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    # convert all coordinates floating point values to int
    box = np.int0(box)
    # draw a green 'nghien' rectangle
    cv2.drawContours(paper, [box], 0, (0, 255, 0),1)

cv2.imshow('paper', paper)
cv2.imwrite('paper.jpg',paper)
cv2.waitKey(0)