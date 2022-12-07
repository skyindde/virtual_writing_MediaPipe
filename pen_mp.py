import cv2
import mediapipe
import numpy as np
import math

# virtual pen and wiping with mediapipe

drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

capture = cv2.VideoCapture(0)
capture.set(3, 1200)  # 3 for widthq
capture.set(4, 900)  # 4 for height
capture.set(10, 100) # 10 for brightness
setp = []
points = []

def wipe(imgg):
    contours, hierarchy = cv2.findContours(imgg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    for cnt in contours:
        area2 = cv2.contourArea(cnt)
        print(area2)
        if area2 > 45000:    # for work for only valid shapes
            # np.empty(points)
            points.clear()

with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.3, min_tracking_confidence=0.3,  #org--0.7,0.7
                       max_num_hands=2) as hands:
    while (True):

        ret, frame = capture.read()
        # frame.set(cv2.CAP_PROP_FPS, 5)
        frame = cv2.flip(frame, 1)
        img2 = frame.copy()
        imgHSV = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image_height, image_width, _ = frame.shape
        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                drawingModule.draw_landmarks(frame, handLandmarks, handsModule.HAND_CONNECTIONS)
                # print(handLandmarks)
                # points.append(handLandmarks)
                # print(points)
                # setp.clear()
                for ids, landmrk in enumerate(handLandmarks.landmark):
                    cx, cy = landmrk.x * image_width, landmrk.y*image_height
                    # print(ids, cx, cy)
                    setp.append([cx, cy])
                # points.append(setp)
        if bool(setp):
            # print(setp[1][1])
            d = math.sqrt((setp[8][0] - setp[4][0]) ** 2 + (setp[8][1] - setp[4][1]) ** 2)
            # print(d)
            if d < 30:
                print(int(setp[8][0]), int(setp[8][1]))
                points.append([int(setp[8][0]), int(setp[8][1])])
                cv2.circle(img2, (int(setp[8][0]), int(setp[8][1])), 5, (0, 0, 255), cv2.FILLED)
        for pt in points:
           cv2.circle(img2, (pt[0], pt[1]), 5, (0, 0, 255), cv2.FILLED)
        # getCountours(setp)
        setp.clear()

        lower2 = np.array([5, 31, 207])
        upper2 = np.array([27, 135, 255])
        mask2 = cv2.inRange(imgHSV, lower2, upper2)
        wipe(mask2)

        hor1 = np.hstack((frame, img2))
        #cv2.imshow('Test hand', hor1)
        cv2.imshow('Hand', frame)
        cv2.imshow('write', img2)

        if cv2.waitKey(1) == 27: # ESC key
            break

cv2.destroyAllWindows()
capture.release()
