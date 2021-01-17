import cv2
import numpy as np
from pynput.mouse import Button, Controller
import wx

from hand_tracking.get_gesture_coor import get_finger_coor

# Global Variables
LOWER_BOUND = np.array([100, 150, 0])
UPPER_BOUND = np.array([140, 255, 255])
KERNEL_OPEN = np.ones([5, 5])
KERNEL_CLOSE = np.ones([20, 20])
FLIP = True
DAMPING_FACTOR = 2  # >1
CLICKED = False
# To use wx need to create an app
app = wx.App(False)
sx, sy = wx.GetDisplaySize()  # Getting max size of screen in x-y coordinates
camx, camy = (320, 240)  # Setting size of capture

mouse = Controller()

cam = cv2.VideoCapture(0)  # Getting cam feed from webcam
cam.set(cv2.CAP_PROP_FRAME_WIDTH, camx)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, camy)

# Making mouse movement smoother
mouse_old_coor = np.array([0, 0])
mouse_coor_damp = np.array([0, 0])
curr_area = 0


def open_area(coor1, coor2):
    x1, y1, w1, h1 = coor1
    x2, y2, w2, h2 = coor2
    xl, yl = min(x1, x2), min(y1, y2)
    xr, yr = max(x1+w1, x2+w2), max(y1+h1, y2+h2)

    area = (xr-xl)*(yr-yl)
    return area


while True:
    ret, img = cam.read()

    if FLIP:
        img = cv2.flip(img, 1)

    # img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Creating mask that filters everything that isnt blue
    # mask = cv2.inRange(img_hsv, LOWER_BOUND, UPPER_BOUND)

    # mask_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL_OPEN)  # removes noise
    # mask_close = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, KERNEL_CLOSE)  # removes holes
    # conts, h = cv2.findContours(mask_close.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(img, conts, -1, (0, 120, 0), 1)
    screen_scale_x, screen_scale_y = sx/camx, sy/camy
    conts = get_finger_coor(img)

    if conts is not None:
        if len(conts) == 2:
            if CLICKED:
                CLICKED = False
                mouse.release(Button.left)
                curr_area = 0

            # x1, y1, w1, h1 = cv2.boundingRect(conts[0])
            # x2, y2, w2, h2 = cv2.boundingRect(conts[1])

            # cv2.rectangle(img, (x1, y1), (x1+w1, y1+h1), (255, 0, 0), 2)
            # cv2.rectangle(img, (x2, y2), (x2+w2, y2+h2), (255, 0, 0), 2)

            # cx1, cy1 = x1 + w1//2, y1 + h1//2
            # cx2, cy2 = x2 + w2//2, y2 + h2//2

            # Using pose estimation
            width, height = 30, 30
            x1, y1 = conts[0]
            x2, y2 = conts[1]
            cv2.rectangle(img, (x1, y1), (x1+width, y1+height), (255, 0, 0), 2)
            cv2.rectangle(img, (x2, y2), (x2+width, y2+height), (255, 0, 0), 2)

            cx1, cy1 = x1 + width//2, y1 + height//2
            cx2, cy2 = x2 + width//2, y2 + height//2

            cv2.line(img, (cx1, cy1), (cx2, cy2), (0, 255, 0), 2)

            clx, cly = (cx1+cx2)//2, (cy1+cy2)//2
            cv2.circle(img, (clx, cly), 5, (0, 0, 255), -1)

            mouse_coor_damp = mouse_old_coor + ((clx, cly)-mouse_old_coor) / DAMPING_FACTOR
            mouse.position = mouse_coor_damp[0]*screen_scale_x, mouse_coor_damp[1]*screen_scale_y

            mouse_old_coor = mouse_coor_damp

            # curr_area = open_area((x1, y1, w1, h1), (x2, y2, w2, h2))
            curr_area = open_area((x1, y1, width, width), (x2, y2, width, width))
    # if fingers are together
    # elif len(conts) == 1:
    #     x, y, w, h = cv2.boundingRect(conts[0])
    #     new_area = w*h
    #     if not CLICKED:
    #         if ((abs(new_area-curr_area)/new_area) * 100) < 20:
    #             CLICKED = True
    #             mouse.press(Button.left)

    #     else:

    #         cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    #         cx, cy = x + w//2, y + h//2
    #         cv2.circle(img, (cx, cy), (w+h)//4, (0, 0, 255), -1)

    #         mouse_coor_damp = mouse_old_coor + ((cx, cy)-mouse_old_coor) / DAMPING_FACTOR
    #         mouse.position = mouse_coor_damp[0]*screen_scale_x, mouse_coor_damp[1]*screen_scale_y

    #         mouse_old_coor = mouse_coor_damp

    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
