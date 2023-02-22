import cv2
import mediapipe
import numpy as np
import math

# virtual pen and wiping with mediapipe

drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

setp = []
points = []
o = 0
d0 = 50

def wipe(imgg):
    contours, hierarchy = cv2.findContours(imgg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    for cnt in contours:
        area2 = cv2.contourArea(cnt)
        # print(area2)
        if area2 > 5000:    # for work for only valid shapes
            # np.empty(points)
            points.clear()

capture = cv2.VideoCapture(0)
capture.set(3, 1200)  # 3 for widthq
capture.set(4, 900)  # 4 for height
capture.set(10, 100)  # 10 for brightness

with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.3, min_tracking_confidence=0.3,
                       # org--0.7,0.7
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
                # storing all the hand landmark points in the array setp
                for ids, landmrk in enumerate(handLandmarks.landmark):
                    cx, cy = landmrk.x * image_width, landmrk.y * image_height
                    # print(ids, cx, cy)
                    setp.append([cx, cy])
                # points.append(setp)
        if len(points) == 0:
            o = 0
        if bool(setp):
            # print(setp[1][1])
            # d is distance between tips of forefinger and thumb
            d = math.sqrt((setp[8][0] - setp[4][0]) ** 2 + (setp[8][1] - setp[4][1]) ** 2)
            # print(d)
            # writing occurs only when d is less than set value and the points are appended in an array points as circular dots
            if d < 30:
                if d0 > 30:
                    points.append([])
                    o = o + 1
                    points[o - 1].append([int(setp[8][0]), int(setp[8][1])])

                if d0 < 30:
                    #                     print(int(setp[8][0]), int(setp[8][1]))
                    points[o - 1].append([int(setp[8][0]), int(setp[8][1])])
            #                     cv2.circle(img2, (int(setp[8][0]), int(setp[8][1])), 5, (0, 0, 255), cv2.FILLED)
            d0 = d

        for pts in points:
            for pt in pts:
                cv2.circle(img2, (pt[0], pt[1]), 5, (0, 0, 255), cv2.FILLED)
            if len(pts) > 1:
                # for pt in points[:-1]:
                for i in range(len(pts) - 1):
                    cv2.line(img2, (pts[i][0], pts[i][1]), (pts[i + 1][0], pts[i + 1][1]), (0, 0, 255), 5)
        # getCountours(setp)
        setp.clear()

        lower2 = np.array([1, 54, 173]) #[5, 31, 207])
        upper2 = np.array([19, 97, 223]) #[27, 135, 255])
        mask2 = cv2.inRange(imgHSV, lower2, upper2)
        wipe(mask2)

        hor1 = np.hstack((frame, img2))
        # cv2.imshow('Test hand', hor1)
        cv2.imshow('Hand', frame)
        cv2.imshow('write', img2)

        if cv2.waitKey(1) == 27:  # ESC key
            break

cv2.destroyAllWindows()
capture.release()
