# For running inference on the TF-Hub module.
import errno
import tensorflow as tf
import tensorflow_hub as hub
# For downloading the image.
import matplotlib.pyplot as plt
import tempfile
# from six.moves.urllib.request import urlopen #don't think I need this for images saved to device
from six import BytesIO
# For processing the image
import cv2
# For drawing onto the image.
import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
# For measuring the inference time.
import time
# For iterating over the directory
import os
import csv

def displayImage(image):
    print("[INFO] Displaying image...")
    cv2.imshow("Image", image)
    cv2.waitKey(100)
    cv2.destroyAllWindows()

def loadImage(path):
    print("[INFO] Loading image...")
    img = tf.io.read_file(path)
    img = tf.image.decode_jpeg(img, channels=3)
    return img

def drawBoundingBox(image,
                               ymin,
                               xmin,
                               ymax,
                               xmax,
                               color,
                               font,
                               thickness=4,
                               display_str_list=()):
  print("[INFO] Drawing boxes on image")
  """Adds a bounding box to an image."""
  draw = ImageDraw.Draw(image)
  im_width, im_height = image.size
  (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                ymin * im_height, ymax * im_height)
  draw.line([(left, top), (left, bottom), (right, bottom), (right, top),
             (left, top)],
            width=thickness,
            fill=color)

# If the total height of the display strings added to the top of the bounding
  # box exceeds the top of the image, stack the strings below the bounding box
  # instead of above.
  display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
  # Each display_str has a top and bottom margin of 0.05x.
  total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

  if top > total_display_str_height:
    text_bottom = top
  else:
    text_bottom = top + total_display_str_height
  # Reverse list and print from bottom to top.
  for display_str in display_str_list[::-1]:
    text_width, text_height = font.getsize(display_str)
    margin = np.ceil(0.05 * text_height)
    draw.rectangle([(left, text_bottom - text_height - 2 * margin),
                    (left + text_width, text_bottom)],
                   fill=color)
    draw.text((left + margin, text_bottom - text_height - margin),
              display_str,
              fill="black",
              font=font)
    text_bottom -= text_height - 2 * margin

def draw_boxes(image, boxes, class_names, scores, max_boxes=10, min_score=0.1):
  """Overlay labeled boxes on an image with formatted scores and label names."""
  colors = list(ImageColor.colormap.values())

  try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf",
                              25)
  except IOError:
    print("Font not found, using default font.")
    font = ImageFont.load_default()

  for i in range(min(boxes.shape[0], max_boxes)):
    if scores[i] >= min_score:
      ymin, xmin, ymax, xmax = tuple(boxes[i])
      display_str = "{}: {}%".format(class_names[i].decode("ascii"),
                                     int(100 * scores[i]))
      color = colors[hash(class_names[i]) % len(colors)]
      image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
      drawBoundingBox(
          image_pil,
          ymin,
          xmin,
          ymax,
          xmax,
          color,
          font,
          display_str_list=[display_str])
      np.copyto(image, np.array(image_pil))
  return image

# Combines two arrays into an array of tuples, sorts by descending order
# Input: 
# Output: 
def sortDesc(entities, scores, topx):
  detected = []
  for entity in entities:
    detected.append(entity.decode("ascii"))
  tupArr = list(zip(detected, scores))
  return sorted(tupArr, key=lambda tup: tup[1], reverse=True)[0:topx]

# Writes the frame and objects into specified csv 
# Input: nameIn: column 1 of csv, the frame name, labels: top labels and respective confidences
# Input cont.: fileNameIn: csv file to write to, pathIn: the directory the csv sits in 
def writeCsv(nameIn, labels, fileNameIn, pathIn):
  try:
    if not os.path.exists(pathIn):
      os.makedirs(pathIn)
    file = open(f'{pathIn}/{fileNameIn}', 'a', newline="")
    file = csv.writer(file)
    file.writerow([nameIn, labels])
    print(f"[INFO] recorded in {pathIn}/{fileNameIn}")
  except OSError as e:
    if e.errno != errno.EEXIST:
      raise

def runDetector(detector, frame, fileNameIn, pathIn='TensorFlowHub/output'):
  print("[INFO] Running detector...")
  img = loadImage(frame)

  converted_img  = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
  start_time = time.time()
  result = detector(converted_img)
  end_time = time.time()

  result = {key:value.numpy() for key,value in result.items()}

  print("Found %d objects." % len(result["detection_scores"]))
  print("Inference time: ", end_time-start_time)

  image_with_boxes = draw_boxes(
      img.numpy(), result["detection_boxes"],
      result["detection_class_entities"], result["detection_scores"])

  # returns the top 10 (by confidence) detected objects 
  topTen = sortDesc(result["detection_class_entities"], result["detection_scores"], 10)

  writeCsv(frame, topTen, fileNameIn, pathIn)

  displayImage(image_with_boxes)
  print("[INFO] detector executed")

# Picking object detection module and applying to the downloaded image 
# module_handle = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1" #@param ["https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1", "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"]
detector = hub.load("faster_rcnn_openimages_v4").signatures['default']
# detector = hub.load(module_handle).signatures['default']
print("[INFO] Assigned detector")

def detectMercedes():
# Run object detector on all images in the 'TensorFlowHub/output/mercedes.csv'
  for entry in os.scandir("sample_media/mercedes_frames"):
      runDetector(detector, entry.path.replace(os.sep, '/'), 'mercedes.csv')
    
def detectOlympics():
  for entry in os.scandir("sample_media/nfl_frames"):
    runDetector(detector, entry.path.replace(os.sep, '/'), 'nfl_detected.csv')

def detectDir(directoryIn):
  for entry in os.scandir("sample_media/olympics0"):
    runDetector(detector, entry.path.replace(os.sep, '/'), 'olympics.csv')



detectOlympics()


