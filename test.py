# from picamera2 import Picamera2
# import time
# import cv2
# from firebase_updating import playAudio
import tensorflow as tf
from pose import detect

picam2 = Picamera2()

config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()


# img = picam2.capture_array()
detection_threshold = 0.1

cv2.imwrite('frame.jpg', img)

image_path = 'pose_images/for lett/IMG_4174.JPG'

image = tf.io.read_file(image_path)
image = tf.io.decode_jpeg(image)
image_height, image_width, channel = image.shape

print(image_height, image_width, channel)

person = detect(image)

print(person)
min_landmark_score = min([keypoint.score for keypoint in person.keypoints])
should_keep_image = min_landmark_score >= detection_threshold

print(should_keep_image)