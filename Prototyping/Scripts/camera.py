import sys
import cv2
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions


def run(model: str, camera_id: int, width: int, height: int, num_threads: int) -> None:
  # Start capturing video input from the camera
  cap = cv2.VideoCapture(camera_id)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

  # Visualization parameters
  text_color = (0, 0, 255)  # red
  font_size = 1
  font_thickness = 1

  # Initialize the object detection model
  options = ObjectDetectorOptions(
      num_threads=num_threads,
      score_threshold=0.9,
      max_results=3,
      enable_edgetpu=False)
  detector = ObjectDetector(model_path=model, options=options)

  # Continuously capture images from the camera and get predictions
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      sys.exit('ERROR: Unable to read from webcam. Please verify your webcam settings.')

    image = cv2.flip(image, 1)

    # Run object detection estimation using the model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    detections = detector.detect(rgb_image)

    # Draw bound boxes on input image
    for detection in detections:
        category = detection.categories[0]

        xmin = detection.bounding_box.left
        ymin = detection.bounding_box.top
        xmax = detection.bounding_box.right
        ymax = detection.bounding_box.bottom

        start = xmin, ymin
        end = xmax, ymax

        cv2.rectangle(image, start, end, text_color, 3)

        label = category.label
        score = round(category.score, 2)

        box_text = label + '(' + str(score) + ')'

        cv2.putText(image, box_text, (10+xmin,20+ymin), cv2.FONT_HERSHEY_PLAIN,
                font_size, text_color, font_thickness)

    cv2.imshow('Object Detections', image)

  cap.release()

  return detections
