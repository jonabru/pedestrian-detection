# import the necessary packages
from __future__ import print_function
from imutils.object_detection import non_max_suppression
import numpy as np
import cv2

#initialise the Histogram of Oriented Gradient (HOG) descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

#find people in the image provided
def detect(imagePath):
    #load the image and resize it to reduce detection time and improve detection accuracy
    img = cv2.imread(imagePath)
    width = 800
    ratio = width/img.shape[1]
    size = (width, int(img.shape[0]*ratio))
    img = cv2.resize(img, size)
    orig = img.copy()

    #using HOG to detect people in the iamge
    (rects, weights) = hog.detectMultiScale(img, winStride=(4,4), padding=(8,8), scale=1.075)
    #drawing the bounding boxes generated by HOG
    for(x, y, w, h) in rects:
        cv2.rectangle(orig, (x, y), (x+w, y+h), (0, 0 , 255), 2)

    #applying non-maxima supressions ot the bounding boxes using a faily large
    #overlap threshold to try to maintain overlapping boxes that are still people
    rects = np.array([[x,y,x+w, y+h] for(x,y,w,h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    #draw final bounding boxes
    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(img, (xA, yA), (xB, yB), (0,255,0), 2)


    filename = imagePath[imagePath.rfind("/")+1:]
    print("[INFO] {}: {} original boxes, {} after supression".format(filename, len(rects), len(pick)))

    #show output images
    cv2.imshow("Without Non-maxima Supression", orig)
    cv2.imshow("With Non-Maxima Supression", img)
    cv2.waitKey(0)

detect('pictures/jaywalkers.jpg')
#detect('pictures/street.jpg')
#detect('pictures/street_2.jpg')
#detect('pictures/street_3.jpg')
#detect('pictures/street_4.jpg')