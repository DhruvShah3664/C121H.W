import cv2
import time
import numpy as np 

#To save the output in a file output.avi
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

#Starting the Webcam
cap = cv2.VideoCapture(0)

#Allowing the webcam to start by making the code sleep for 2 seconds
time.sleep(2)
bg = 0

#Capturing background for 60 frames
for i in range(60):
    ret, bg = cap.read()
#Filipping the backgroud
bg = np.flip(bg, axis = 1)

#Reading the captured frame unit camera is open
while(cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break

    img = np.flip(img, axis =1 )

    #Converting comment to BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    #Generating mask to deteact red color
    lower_black = np.array([30, 30, 0])
    upper_black = np.array([104, 153, 70])
    mask1 = cv2.inRange(hsv, lower_black, upper_black)

    lower_black = np.array([170, 120, 70])
    upper_black = np.array([180, 255,  255])
    mask2 = cv2.inRange(hsv, lower_black, upper_black)

    mask1 = mask1+mask2

    #Open and expand the image where there is mask1 (color)
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    #Selecting the part that does not have mask1 and saving in mask2
    mask2 = cv2.bitwise_not(mask1)

    #Keeping only the part of the images without red color
    res1 = cv2.bitwise_and(img, img, mask = mask2)

    #keeping only the part images with red color
    res2 = cv2.bitwise_and(bg, bg, mask = mask1)
    
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
    output_file.write(final_output)

    cv2.imshow("magic", final_output)
    cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()