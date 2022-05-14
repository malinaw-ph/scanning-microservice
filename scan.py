import json
from pprint import pprint
import requests
from io import BytesIO
import fitz
import os
import pytesseract
from pytesseract import Output
from PIL import Image, ImageOps, ImageDraw

url = "https://hrep-website.s3.ap-southeast-1.amazonaws.com/legisdocs/basic_18/HB00001.pdf"

def extract_images():
  """
  Download PDF and extract images
  """
  print("Retrieving PDF")
  # res = requests.get(url)
  # pdf_stream = BytesIO(res.content)

  fstream = open("HB00001.pdf", "rb")
  pdf_stream = BytesIO(fstream.read())

  print("Reading PDF")
  pdf = fitz.open(stream=pdf_stream)

  os.mkdir("images")

  for page in pdf:
    images = page.get_images()

    for i, img in enumerate(images):
      xref = img[0]
      base_image = pdf.extract_image(xref)
      img_bytes = base_image["image"]
      img_ext = base_image["ext"]

      fn = f"{page.number}-{i}.{img_ext}"
      with open(f"images/{fn}", "wb") as f:
        f.write(img_bytes)

def optimize_image(image):
  """
  Perform heuristic image optimization for better OCR
  """
  image = ImageOps.grayscale(image)
  image = ImageOps.colorize(image, black="black", white="white")
  draw = ImageDraw.Draw(image)
  draw.rectangle((image.width * 0.65, 0, image.width, image.height * 0.2), fill="white")

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

  for x1, y1, w, h in zip(left, top, width, height):
    x2 = x1 + w
    y2 = y1 + h
    draw.rectangle((x1, y1, x2, y2), outline="red")

  image.show()
  # print(text)

def load_images():
  """
  Load images from disk
  """
  for fn in os.listdir("images"):
    image = Image.open(f"images/{fn}")
    optimize_image(image)
    parse_image(image)
    break

if __name__ == "__main__":
  load_images()