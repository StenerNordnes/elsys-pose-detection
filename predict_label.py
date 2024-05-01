from PIL import Image
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import cv2
from pose import detect, draw_prediction_on_image


with open('pose_labels.txt', 'r') as  f:
    labels = f.readlines()

detection_threshold = 0.5
# image_path = "./tmp/vjmi7zdpxmo31.jpg"
# image = tf.io.read_file(image_path)

# fileformat = image_path.split(".")[-1]

# if fileformat == "png":
#     image = tf.io.decode_png(image)
# else:
#     image = tf.io.decode_jpeg(image)


def predictImage(image):
    person = detect(image)

    # Save landmarks if all landmarks were detected
    min_landmark_score = min([keypoint.score for keypoint in person.keypoints])
    should_keep_image = min_landmark_score >= detection_threshold

    if not should_keep_image:
        pass

    # Get landmarks and scale it to the same size as the input image
    pose_landmarks = np.array(
        [
            [keypoint.coordinate.x, keypoint.coordinate.y, keypoint.score]
            for keypoint in person.keypoints
        ],
        dtype=np.float32,
    )

    # Normalize landmarks
    coordinates = pose_landmarks.flatten().astype(np.float32).tolist()
    coordinates = np.array(coordinates, dtype=np.float32).reshape((1, -1))

    # Load the model
    interpreter = tf.lite.Interpreter(model_path="pose_classifier.tflite")
    interpreter.allocate_tensors()

    # Get input and output tensors
    input_index = interpreter.get_input_details()[0]["index"]
    output_index = interpreter.get_output_details()[0]["index"]

    # Run the model
    interpreter.set_tensor(input_index, coordinates)
    interpreter.invoke()
    output = interpreter.tensor(output_index)

    print(output())

    labelIdx = np.argmax(output()[0])

    confidence = output()[0][labelIdx]

    classification = labels[labelIdx].strip()

    print(classification, confidence)
    wireframe_image = None
    wireframe_image = draw_prediction_on_image(
        np.array(image), person, close_figure=True, keep_input_size=True
    )


    return (
        classification, 
            confidence, 
            wireframe_image
            )
# %%
def test_image(filename):
    image = tf.io.read_file(f'./tmp/{filename}.jpg') 
    image = tf.io.decode_jpeg(image)
    person = detect(image)
    # img = draw_prediction_on_image(image.numpy(), person, crop_region=None, 
    #                             close_figure=False, keep_input_size=True)

    clss, conf, img = predictImage(image)
    print(clss, conf)
    plt.imshow(img)
    plt.show()

# %%


def VideoCapture():
    # Open the webcam
    cap = cv2.VideoCapture(0)
    name = ""

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        if not ret:
            print("Error reading frame")
            break

        # Convert the frame to RGB (OpenCV uses BGR by default)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the frame to a TensorFlow tensor
        frame_tensor = tf.convert_to_tensor(frame)

        # Run the prediction model on the frame
        newName, conf, frame = predictImage(frame_tensor)

        if True:
            name = newName
        else:
            name = "Unknown"

        cv2.putText(frame, name, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 10)

        # Display the frame
        cv2.imshow("Video", frame)

        # If the user presses 'q', exit the loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()


# make a video with overlay and classification from existing video


def VideoCapture2():
    cap = cv2.VideoCapture("./tmp/test.mp4")
    name = ""
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter.fourcc(*"MP4V")  # Change the codec here
    out = cv2.VideoWriter("output.mp4", fourcc, fps, (width, height))

    # Create an empty list to store the frames

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_tensor = tf.convert_to_tensor(frame)

        newName, conf, frame = predictImage(frame_tensor)

        if conf > 0.98:
            name = newName
        else:
            name = "Unknown"

        cv2.putText(frame, name, (50, 50), cv2.FONT_HERSHEY_PLAIN, 10, (0, 255, 0), 2)
        out.write(frame)

        # Append the frame to the list

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Write the frames to a file

    out.release()

if __name__ == "__main__":
    # test_image("vjmi7zdpxmo31")
    # VideoCapture2()
    VideoCapture()