import json
from pprint import pprint
import requests
from io import BytesIO
import fitz
import os
import glob

url = "https://hrep-website.s3.ap-southeast-1.amazonaws.com/legisdocs/basic_18/HB00001.pdf"

def extract_images():
  """
  Download PDF and extract images
  """
  print("Retrieving PDF")
  # res = requests.get(url)
  # pdf_stream = BytesIO(res.content)

  if not os.path.exists("images"):
    os.makedirs("images")

  files = glob.glob("*.pdf")
  for file in files:
    file_name = os.path.splitext(file)[0]
    fstream = open(file, "rb")
    pdf_stream = BytesIO(fstream.read())

    pdf = fitz.open(stream=pdf_stream)

    for page in pdf:
      images = page.get_images()

      for i, img in enumerate(images):
        xref = img[0]
        base_image = pdf.extract_image(xref)
        img_bytes = base_image["image"]
        img_ext = base_image["ext"]

        fn = f"{page.number}-{i}.{img_ext}"
        with open(f"images/{file_name}-{fn}", "wb") as f:
          f.write(img_bytes)

if __name__ == "__main__":
  extract_images()