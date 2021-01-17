import time
import cv2
import numpy as np
from pynput.mouse import Button, Controller
from pynput.keyboard import Controller as KController
from model import HandsModel

import wx

from utils import drawing


# Global Variables
LOWER_BOUND = np.array([100, 150, 0])
UPPER_BOUND = np.array([140, 255, 255])
KERNEL_OPEN = np.ones([5, 5])
KERNEL_CLOSE = np.ones([20, 20])
FLIP = True
DAMPING_FACTOR = 2  # >1
CLICK_DIST = 17
# To use wx need to create an app
app = wx.App(False)
sx, sy = wx.GetDisplaySize()  # Getting max size of screen in x-y coordinates
camx, camy = (320, 240)  # Setting size of capture

mouse = Controller()
keyboard = KController()
cam = cv2.VideoCapture(0)  # Getting cam feed from webcam
cam.set(cv2.CAP_PROP_FRAME_WIDTH, camx)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, camy)

# Making mouse movement smoother
mouse_old_coor = np.array([0, 0])
mouse_coor_damp = np.array([0, 0])


def check_dist(pt1, pt2):
    np_pt1, np_pt2 = np.array(pt1), np.array(pt2)
    eu_dist = np.linalg.norm(np_pt1-np_pt2)
    if eu_dist < CLICK_DIST:
        return True
    return False


def start_app():
    times = [0] * 15
    hand_model = HandsModel()
    CLICKED = False
    SCROLL_CLICKED = False
    mouse_old_coor = np.array([0, 0])
    while True:
        start_time = time.perf_counter()
        ret, img = cam.read()

        if FLIP:
            img = cv2.flip(img, 1)

        screen_scale_x, screen_scale_y = sx/camx, sy/camy
        conts, results = hand_model.predict(img, camx, camy)

        if conts is not None:
            drawing.draw_hand_landmarks(results, img)
            if check_dist(conts[2], conts[3]):
                keyboard.type('q')
            if check_dist(conts[0], conts[2]):
                mouse.click(Button.left, 2)
            if not check_dist(conts[1], conts[2]):
                if SCROLL_CLICKED:
                    SCROLL_CLICKED = False
                    mouse.release(Button.middle)

        # if ring and thumb are together
            if check_dist(conts[1], conts[2]):
                if not SCROLL_CLICKED:
                    SCROLL_CLICKED = True
                    mouse.press(Button.middle)

            if not check_dist(conts[0], conts[1]):
                if CLICKED:
                    CLICKED = False
                    mouse.release(Button.left)

        # if fingers are together
            else:
                if not CLICKED:
                    CLICKED = True
                    mouse.press(Button.left)

                # else:
            x1, y1 = conts[0]
            x2, y2 = conts[1]
            cx1, cy1 = x1, y1
            cx2, cy2 = x2, y2
            cx, cy = (cx1+cx2)//2, (cy1+cy2)//2
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1)

            mouse_coor_damp = mouse_old_coor + ((cx, cy)-mouse_old_coor) / DAMPING_FACTOR
            mouse.position = mouse_coor_damp[0] * \
                screen_scale_x, mouse_coor_damp[1]*screen_scale_y

            mouse_old_coor = mouse_coor_damp

        fps = drawing.calculate_ips(times, start_time)
        drawing.draw_fps(img, round(fps, 3))
        cv2.imshow('img', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    hand_model.close()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    start_app()
