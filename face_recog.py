import cv2
import numpy as np
import os
import sys
import math
import face_recognition


class FaceRecognition:
    def __init__(self):
        self.known_face_encodings, self.known_face_names = self.encode_faces()

    def encode_faces(self):
        known_face_encodings = []
        known_face_names = []

        for image in os.listdir('tmp/faces'):
            face_image = face_recognition.load_image_file(f"tmp/faces/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            known_face_encodings.append(face_encoding)
            known_face_names.append(image)

        return known_face_encodings, known_face_names

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            sys.exit('Video source not found...')

        process_current_frame = True

        while True:
            ret, frame = video_capture.read()

            if process_current_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                face_locations = face_recognition.face_locations(small_frame)
                face_encodings = face_recognition.face_encodings(small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    confidence = '???'

                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index].split('.')[0]
                        confidence = self.face_confidence(face_distances[best_match_index])

                    face_names.append(f'{name} ({confidence})')

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Create the frame with the name
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            process_current_frame = not process_current_frame

            print(face_names)

            cv2.imshow('Face Recognition', frame)
            if cv2.waitKey(1) == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

    @staticmethod
    def face_confidence(face_distance, face_match_threshold=0.6):
        range = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range * 2.0)

        if face_distance > face_match_threshold:
            return str(round(linear_val * 100, 2)) + '%'
        else:
            value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
            return str(round(value, 2)) + '%'


if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()