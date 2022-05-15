from PIL import Image
import matplotlib.pyplot as plt

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

def display_cv_image(cv_image):
    """
    Resize image to fit in display
    """
    plt.imshow(cv_image)
    plt.show()