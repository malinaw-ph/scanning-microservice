import pytesseract
from pytesseract import Output
from PIL import ImageDraw, Image

def parse_image(image):
  """
  Extract text and display bounding boxes
  """
  results = pytesseract.image_to_data(image, output_type=Output.DICT)
  conf = results["conf"]
  filter_out = set([i for i, c in enumerate(conf) if float(c) < 0.5])

  fields = ["text", "left", "top", "width", "height", "conf"]
  for field in fields:
    values = results[field]
    values = [v for i, v in enumerate(values) if i not in filter_out]
    results[field] = values

  left = results["left"]
  top = results["top"]
  width = results["width"]
  height = results["height"]

  draw = ImageDraw.Draw(image)
  for x1, y1, w, h in zip(left, top, width, height):
    x2 = x1 + w
    y2 = y1 + h
    draw.rectangle((x1, y1, x2, y2), outline="red")

  display_image(image)
  # print(text)

def display_image(image):
  """
  Resize image to fit in display
  """
  display_height = 1080
  new_height = display_height * 9 // 10
  width, height = image.size
  new_width = new_height * width // height
  display = image.resize((new_width, new_height), Image.ANTIALIAS)

  display.show()