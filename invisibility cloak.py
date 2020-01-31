#importing the libraries
import cv2
import numpy as np

#capture the background and saving it

cap = cv2.VideoCapture(0) # video is captured

while(1):
    _, frame = cap.read() #reading the image
    cv2.imshow('frame', frame) #display the image
    
    k = cv2.waitKey(5)#wait
    
    if k==27:
        cv2.imwrite('background.jpg', frame)
        break



    
cap.release() #switching off the camera 
cv2.destroyAllWindows()


#set the hsv values of the cloak using trackbar

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow("Tracking")#creates a window for the trackbar to be setup
cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

while True:
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("LH", "Tracking")
    l_s = cv2.getTrackbarPos("LS", "Tracking")
    l_v = cv2.getTrackbarPos("LV", "Tracking")

    u_h = cv2.getTrackbarPos("UH", "Tracking")
    u_s = cv2.getTrackbarPos("US", "Tracking")
    u_v = cv2.getTrackbarPos("UV", "Tracking")

    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, l_b, u_b)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow("res", res)
    key = cv2.waitKey(5)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()


#image operations to achive invisibility

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('invisibility.avi', fourcc, 20.0, (640,480))
image=cv2.imread("background.jpg")

cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, l_b, u_b)
    
    #noise reduction purpose
    mask = cv2.erode(mask, np.ones((3, 3), np.uint8), iterations = 2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations = 2)
    res1 = cv2.bitwise_and(image, image, mask=mask)
    cv2.imshow("res1",res1)


    
    mask1=255-mask#color inversion
    res2 = cv2.bitwise_and(frame, frame, mask=mask1)
    cv2.imshow("res2",res2)
    add = cv2.addWeighted(res1, 1, res2, 1, 0)
    
    cv2.imshow("invisible cloak",add)
    out.write(add)
    key = cv2.waitKey(5)
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()


    
