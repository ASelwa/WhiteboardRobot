import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 2 because red wraps around
    # define range of red color in HSV
    [H1, H2] = [
    lower_red1 = np.array([H1,S1,V1], dtype=np.uint8)
    upper_red1 = np.array([180,S2,V2], dtype=np.uint8)
    lower_red2 = np.array([0,S1,V1], dtype=np.uint8)
    upper_red2 = np.array([H2,S2,V2], dtype=np.uint8)

    # Threshold the HSV image to get only blue colors
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

#    ret,thresh = cv2.threshold(mask,127,255,0)
#    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
