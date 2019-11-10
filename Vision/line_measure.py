from subprocess import Popen, PIPE
import numpy as np
import sys
import time
import cv2
import os
import requests
import shutil 

offline = 0
image_url = "http://smartcampus.prefeitura.unicamp.br/cameras/cam_ra.jpg"
time_new_picture = 2

def main():
    
    if offline:
        BUFFER = 15
        cam = cv2.VideoCapture('/dev/video1')
        cam.set(3,1280)
        cam.set(4,960)
        cam.set(10,8)
        for i in range(BUFFER):
            cam.read()
    if not os.path.exists('outputs'):
        os.mkdir('outputs')

    count = 0
    while True:

        time_start = time.time()
        if offline:
            ret,image = cam.read()
        else:
            ret = 1
            resp = requests.get(image_url, stream=True)
            input_file = open('input.jpg', 'wb')
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, input_file)
            input_file.close()
            del resp

        if ret == True:
            input_img = 'input.jpg'
            if offline:
                cv2.imwrite(input_img,image)


            out_img = 'outputs/out' + str(count).zfill(4) + '.jpg'
            bashCommand = "./darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights %s -thresh 0.15 -out %s" % (input_img,out_img) 
            process = Popen(bashCommand.split(), stdout=PIPE)
            output, error = process.communicate()

            output = output.split("\n")
            #print output

            detections = np.array(output[1:-1])

            # print detections

            left_line_counter = 0
            right_line_counter = 0
            people_counter = 0 
            #for i in range(number_box_detected):
            for item in detections:
                label = item.split()[0][:-1]
                if label == 'person':
                    people_counter += 1
                    position = float(item.split()[2]) 
                    if position < 0.5:
                        left_line_counter += 1
                    elif position >= 0.5:
                        right_line_counter += 1

            cycle_time = time.time()-time_start
            out_file = open(out_img[:-4]+'.txt','w') 
            out_file.write(str(people_counter))
            out_file.write(str(left_line_counter))
            out_file.write(str(right_line_counter))
            out_file.write(str(cycle_time))
            out_file.write(str(detections))

            count += 1
            time.sleep(time_new_picture)
main()
