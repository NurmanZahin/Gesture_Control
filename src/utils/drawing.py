
import time
import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


def draw_fps(img, fps_text):
    fps_msg = f'FPS: {fps_text}'
    cv2.putText(img, fps_msg, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 2)


def draw_hand_landmarks(hand_results, out_image):
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                out_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)


def calculate_ips(time_list, start_time):
    """Function to calculate inference per second

    Args:
        time_list (list): list of the inference time
        start_time (float): the starting time of the inference
    """
    time_list.append(time.perf_counter() - start_time)
    time_list.pop(0)
    ips_avg = len(time_list) / sum(time_list)
    return ips_avg
