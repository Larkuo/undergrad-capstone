import sys
import time

import cv2
from numpy import double
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions
import utils


def run(model: str, camera_id: int, width: int, height: int, num_threads: int,
        score_threshold: float, enable_edgetpu: bool) -> None:

  # Variables to calculate FPS
  counter, fps = 0, 0
  start_time = time.time()

  # Start capturing video input from the camera
  cap = cv2.VideoCapture(camera_id)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

  # Visualization parameters
  row_size = 20  # pixels
  left_margin = 24  # pixels
  text_color = (0, 0, 255)  # red
  font_size = 1
  font_thickness = 1
  fps_avg_frame_count = 10

  # Initialize the object detection model
  options = ObjectDetectorOptions(
      num_threads=num_threads,
      score_threshold=score_threshold,
      max_results=3,
      enable_edgetpu=enable_edgetpu)
  detector = ObjectDetector(model_path=model, options=options)

  # Continuously capture images from the camera and run inference
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      sys.exit('ERROR: Unable to read from webcam. Please verify your webcam settings.')

    counter += 1
    image = cv2.flip(image, 1)

    # Run object detection estimation using the model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    detections = detector.detect(rgb_image)

    # Draw keypoints and edges on input image
    image = utils.visualize(image, detections)

    # Calculate the FPS
    if counter % fps_avg_frame_count == 0:
      end_time = time.time()
      fps = fps_avg_frame_count / (end_time - start_time)
      start_time = time.time()

    # Show the FPS
    fps_text = 'FPS = {:.1f}'.format(fps)
    text_location = (left_margin, row_size)
    cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                font_size, text_color, font_thickness)

    # Stop the program if the ESC key is pressed.
    if cv2.waitKey(1) == 27:
      break
    cv2.imshow('object_detector', image)

  cap.release()
  cv2.destroyAllWindows()


def main():
  model_path = '/model_final.tflite'
  camera_id = 0
  frame_width = 300 # pixels
  frame_height = 250 # pixels
  num_threads = 4
  score_threshold = 0.3
  enable_edgetpu = False


  run(model_path, camera_id, frame_width, frame_height, num_threads, score_threshold, enable_edgetpu)


if __name__ == '__main__':
  main()