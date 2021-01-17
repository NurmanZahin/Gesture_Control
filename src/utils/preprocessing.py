import cv2


def prepare_img(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img.flags.writeable = False
    return img
