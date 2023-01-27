import cv2
import glob 
import numpy as np 
from datetime import datetime 

import warnings
warnings.filterwarnings('ignore')

def main():
    for selectPhoto in glob.iglob("C:/Users/lenovo/workFile/developerPaper/bubleDetectionCV/image/*.jpg"):
        image = cv2.imread(selectPhoto)
        #cv2.imshow("image1", image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

    # gray, blur, adptive threshold.
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (11,5), 0)
        thresh = cv2.threshold(blur, 0,255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    #morphological transformation.
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN,kernel)

    # Fint contours
        cnts = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else [1]

    # simple blop detector 
        params = cv2.SimpleBlobDetector_Params()
        params.filterByColor = True
        params.blobColor = 0
        params.minThreshold = 50
        params.maxThreshold = 255   
        params.minDistBetweenBlobs = 5 
        params.filterByArea = True
        params.minArea = 5
        params.maxArea = 300
        params.filterByConvexity = True
        params.minConvexity = 0.1
        params.filterByCircularity = True
        params.filterByInertia = False

        is_v2 = cv2.__version__.startswith("2.")
        if is_v2:
            detector = cv2.SimpleBlobDetector(params)
        else:
            detector = cv2.SimpleBlobDetector_create()
            keypoints = detector.detect(thresh)

    # count the number of circles 
        total_count = 0
        for i in keypoints:
            total_count = total_count + 1 

        for c in cnts: 
            perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)
            if len(approx) > 6:

                x,y,w,h = cv2.boundingRect(c)

                #Find measurements
                diameter = w
                radius = w/2

                # Find Centroid
                M = cv2.moments(c)

                cX = int(M["m10"] / M["m00"])
                cY = int(M["m10"] / M["m00"])

                # Draw the contour and center of the shape on image 
                cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 4)
                cv2.drawContours(image, [c], 0, (36,255,12), 4)
                cv2.circle(image, (cX,cY), 15, (32,159,22), -1)

                # draw line and diameter  information 
                cv2.line(image,  (x,y + int(h/2)), (x + w,y + int(h/2)), (156,188,24),3)
                cv2.putText(image, "Diameter: {}".format(diameter),(cX-50, cY-50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(160,255,255),1)


                #count the number of circles
                label_count = "total_count:{}".format(f'{total_count}')
                print(label_count)

                # buble total area ccalculation 
                label_diameter = "Diameter:{}".format(f'{diameter}')
                print(label_diameter)

                # image, date and time information

                location = "blob_detect_{}.JPG".format(f'{datetime.now(): %Y-%m-%d_%H:%M:%S%z}')
                print(location)

                cv2.imshow("image2", image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

if __name__ == '__main__':
    main()