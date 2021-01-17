import mediapipe as mp
from utils.preprocessing import prepare_img
from utils.postprocessing import get_coor, scale_coor


class HandsModel:

    def __init__(self, det_conf=0.5, track_conf=0.5):
        mp_hands = mp.solutions.hands
        self.hand_model = mp_hands.Hands(min_detection_confidence=det_conf,
                                         min_tracking_confidence=track_conf)

    @staticmethod
    def preprocess(image):
        return prepare_img(image)

    @staticmethod
    def postprocess(results, scale_w, scale_h):
        finger_landmarks = get_coor(results)
        if finger_landmarks:
            return scale_coor(finger_landmarks, scale_w, scale_h), results
        else:
            return None, None

    def predict(self, image, scale_width, scale_height):
        preprocess_img = self.preprocess(image)
        hand_results = self.hand_model.process(preprocess_img)
        coors, results = self.postprocess(hand_results, scale_width, scale_height)
        return coors, results

    def close(self):
        self.hand_model.close()
