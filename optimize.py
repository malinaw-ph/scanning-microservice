from PIL import ImageOps, ImageDraw, Image
import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib


def remove_stamp(image):
    """
    Remove stamps using circle detection
    
    See https://dsp.stackexchange.com/questions/22648/in-opecv-function-hough-circles-how-does-parameter-1-and-2-affect-circle-detecti
    """
    width, height = image.size

    # Crop top left area where stamp usually is
    rect = (width * 0.65, 0, width, height * 0.2)
    image = image.crop(rect)

    # Convert to grayscale
    image = ImageOps.grayscale(image)
    cv_image = np.array(image)
    _, cv_image = cv2.threshold(cv_image, 10, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # cv_image = cv2.bitwise_and(cv_image, cv_image, mask=bw_image)

    # Find circles
    circles = cv2.HoughCircles(cv_image, cv2.HOUGH_GRADIENT, 
        20, 1000, 
        param1=10, 
        param2=300, 
        minRadius=280, 
        maxRadius=340)
    output = cv2.cvtColor(cv_image, cv2.COLOR_GRAY2RGB)

    # Draw circles
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(output, (x, y), r, (0, 255, 0), 2)
            print(x, y, r)
    else:
        print("No circles detected")

    print("Removing stamp")
    plt.imshow(output)
    plt.show()

def patch_stamp(image):
    width, height = image.size

    # Crop top left area where stamp usually is
    rect = (width * 0.65, 0, width, height * 0.2)
    draw = ImageDraw.Draw(image)
    draw.rectangle(rect, fill="white")

    cv_image = np.array(image)
    plt.imshow(cv_image)
    plt.show()

if __name__ == "__main__":
    image = Image.open("images/HB00003-0-0.jpeg")
    patch_stamp(image)
