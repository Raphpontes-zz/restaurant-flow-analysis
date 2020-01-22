import cv2
import time
import os


cam = cv2.VideoCapture('/dev/video0')
imagename = 'readed_image.jpg'
result_image = 'predictions.jpg'
count = 0

while True:

    time.sleep(1)
    ret,image = cam.read()

    if ret == True:
        # cv2.imwrite(imagename,image)

        # command = './darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights %s -thresh 0.15' % imagename
        # os.system(command)
        # time.sleep(3)

        number = str(count).zfill(6)
        new_name = 'prediction'+number+'.jpg'
        new_result_image = 'prediction_results/%s' % new_name
        cv2.imwrite(new_result_image,image)
        # command = 'cp %s %s' % (result_image,new_result_image)
        # os.system(command)
        count += 1
        # print result_image,new_result_image

        # result = cv2.imread(new_result_image)

        # cv2.imshow("foto",image)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break

# ret,image = cam.read()
# cv2.imshow("foto",image)
# cv2.waitKey(3000)

cam.release()
cv2.destroyAllWindows()