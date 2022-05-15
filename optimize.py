from PIL import ImageOps, ImageDraw, Image
import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib

from display import display_cv_image, display_image


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

    # cv_image = np.array(image)
    # plt.imshow(cv_image)
    # plt.show()
    return image

def adjust_gamma(cv_image, gamma=1.0):
    """
    Adjust contrast of the image using gamma correction
    """

    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    new_image = cv2.LUT(cv_image, table)
    return new_image

def mask_image(image):
    """
    Convert image to black and white
    """

    # Generate mask
    image = image.convert("L")
    cv_image = np.array(image)
    _, mask = cv2.threshold(cv_image, 127, 255, cv2.THRESH_BINARY_INV)
    mask_inv = cv2.bitwise_not(mask)

    # Generate white paper background
    white_background = np.ones(cv_image.shape, dtype="uint8") * 255

    # Extract important parts from the document and remove relevant areas from background
    document_fg = cv2.bitwise_and(cv_image, cv_image, mask=mask)
    masked_bg = cv2.bitwise_and(white_background, white_background, mask=mask_inv)

    # Place important content onto white background
    dst = cv2.add(masked_bg, document_fg)
    dst = adjust_gamma(dst, 0.1)

    # display_image(image)
    output = cv2.cvtColor(dst, cv2.COLOR_GRAY2RGB)
    display_cv_image(output)

    image = Image.fromarray(output)

    return image

def optimize_image(image):
    image = patch_stamp(image)
    image = mask_image(image)

    return image

if __name__ == "__main__":
    image = Image.open("images/HB00003-0-0.jpeg")
    patch_stamp(image)
