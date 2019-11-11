from subprocess import Popen, PIPE
import numpy as np
import sys
import time
import cv2
import os
import requests
import shutil 
import paho.mqtt.client as mqtt
import json
import time
import datetime


offline = 0
image_url = "http://smartcampus.prefeitura.unicamp.br/cameras/cam_ra.jpg"
time_new_picture = 10

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
    if not os.path.exists('inputs'):
        os.mkdir('inputs')
        
    count = 0
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    old_minute = minute
    
    #while True:
    while hour >= 23 and hour <= 24 and minute > 30 and minute < 50:

        time_start = time.time()
        if offline:
            ret,image = cam.read()
        else:
            ret = 1
            resp = requests.get(image_url, stream=True)
            input_img = 'inputs/in' + str(count).zfill(4) + '.jpg'
            #input_file = open('input.jpg', 'wb')
            input_file = open(input_img, 'wb')
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, input_file)
            input_file.close()
            del resp
        old_minute = minute
        if ret == True:
            #input_img = 'input.jpg'
            #input_img = 'P_20191016_120756.jpg'
            #input_img = 'IMG_20190906_181756281.jpg'
            
            if offline:
                cv2.imwrite(input_img,image)

            ##Passa a imagem de entrada para a rede neural
            out_img = 'outputs/out' + str(count).zfill(4) + '.jpg'
            bashCommand = "./darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights %s -thresh 0.15 -out %s" % (input_img,out_img) 
            process = Popen(bashCommand.split(), stdout=PIPE)
            output, error = process.communicate()

            ##Filtra os dados de saida da rede neural
            output = output.split("\n")
            detections = np.array(output[1:-1])
            left_line_counter = 0
            right_line_counter = 0
            people_counter = 0 
            status_fila = "pequena"

            for item in detections:
                label = item.split()[0][:-1]
                if label == 'person':
                    people_counter += 1
                    position = float(item.split()[2]) 
                    if position < 0.5:
                        left_line_counter += 1
                    elif position >= 0.5:
                        right_line_counter += 1
                        
            if people_counter > 10:
                status_fila = "media"
            if people_counter > 20:
                status_fila = "grande"

            timestamp = time.time()
            cycle_time = timestamp-time_start
            
            
            ##salva os dados processdor em um txt
            out_file = open(out_img[:-4]+'.txt','w') 
            out_file.write('Numero de pessoas: '+str(people_counter)+'\n')
            out_file.write('Numero de pessoas a esquerda: ' + str(left_line_counter)+'\n')
            out_file.write('Numero de pessoas a direita: ' + str(right_line_counter)+'\n')
            out_file.write('Tempo de execucao: ' + str('%.2f' % cycle_time)+' segundos\n')
            out_file.write(str(detections))
            out_file.close()

            ##envia os dados processados para o konker
            client = mqtt.Client()
            client.username_pw_set("ic4hlicdjr83", "zARvyT9PmiOh")
            client.connect("mqtt.demo.konkerlabs.net", 1883)
            client.publish("data/ic4hlicdjr83/pub/fila_ra", 
                            json.dumps({"Status da fila": status_fila, "Numero de pessoas": people_counter, "Numero de pessoas a esquerda": left_line_counter, "Numero de pessoas a direita": right_line_counter, "Timestamp": timestamp}))
            
            
            count += 1
            now = datetime.datetime.now()
            hour = now.hour
            minute = now.minute
            while old_minute == minute:
                now = datetime.datetime.now()
                minute = now.minute
                time.sleep(5)
            time.sleep(time_new_picture)
            
            


if __name__ == '__main__':
    main()