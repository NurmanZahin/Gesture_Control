import mediapipe as mp

mp_hands = mp.solutions.hands


def get_coor(hand_results):
    if hand_results.multi_hand_landmarks:
        hand_landmarks = hand_results.multi_hand_landmarks[0]
        res_index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        res_middle = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        res_thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        res_pinky = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
        return (res_index, res_middle, res_thumb, res_pinky)
    else:
        return None


def scale_coor(coordinates, scale_width, scale_height):
    scaled_coordinates = []
    if coordinates:
        for coor in coordinates:
            x_scaled = int(coor.x * scale_width)
            y_scaled = int(coor.y * scale_height)
            scaled_coordinates.append((x_scaled, y_scaled))
        return scaled_coordinates
    else:
        return None
