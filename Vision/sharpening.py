import cv2
import numpy as np
from PIL import ImageEnhance
from PIL import Image
# Reading in and displaying our image
# image = cv2.imread('106-cutted.jpg')
# cv2.imshow('Original', image)
# # Create our shapening kernel, it must equal to one eventually
# kernel_sharpening = np.array([[-1,-1,-1], 
#                               [-1, 9,-1],
#                               [-1,-1,-1]])
# # applying the sharpening kernel to the input image & displaying it.
# sharpened = cv2.filter2D(image, -1, kernel_sharpening)
# cv2.imshow('Image Sharpening', sharpened)
# cv2.waitKey(0)
# cv2.imwrite('106-cutted-sharpened.jpg',sharpened)

# image = cv2.imread("106-cutted.jpg")  # uint8 image

# norm_image = cv2.normalize(image, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

# cv2.imshow('Image Normalized', norm_image)
# cv2.waitKey(0)
# cv2.imwrite('106-cutted-normalized.jpg',norm_image)

# cv2.destroyAllWindows()


image = Image.open("106-cutted.jpg")
# enhancer = ImageEnhance.Sharpness(image)
# enhancer = ImageEnhance.Color(image)
# enhancer = ImageEnhance.Contrast(image)
enhancer = ImageEnhance.Brightness(image)

factor = 3.0
image = enhancer.enhance(factor)
image.show("Sharpness %f" % factor)

image.save("106-cutted-brightness.jpg")