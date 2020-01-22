import cv2
import glob
import os

input_img = "in0470.jpg"
image = cv2.imread(input_img)
image = image[300:1000,350:1500]
# cv2.imshow('cutted',image)
# cv2.waitKey(0)
input_img = 'out0470_cutted.jpg'
cv2.imwrite(input_img,image)


# imglist = glob.glob("001/*.jpg")
# imglist.sort()

# for image in imglist:
# 	input_img = image
# 	# path,file = os.path.split(input_img)
# 	image = cv2.imread(input_img)
# 	image = image[300:1000,350:1500]
# 	# cv2.imshow('cutted',image)
# 	# cv2.waitKey(0)
# 	output_img = input_img[:-4]+"_cropped.jpg"
# 	cv2.imwrite(output_img,image)