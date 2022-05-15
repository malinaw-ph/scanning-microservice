import os
from optimize import optimize_image
from parse import parse_image
from PIL import Image

def load_images():
  """
  Load images from disk
  """
  for fn in os.listdir("images"):
    image = Image.open(f"images/{fn}")
    image = optimize_image(image)
    text = parse_image(image)
    print(text)
    break

if __name__ == "__main__":
  load_images()