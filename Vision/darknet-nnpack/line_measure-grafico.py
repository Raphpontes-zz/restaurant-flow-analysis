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
import argparse
import csv
import glob

offline = 0
image_url = "http://smartcampus.prefeitura.unicamp.br/cameras/cam_ra.jpg"
time_new_picture = 10

def main():
    
    parser = argparse.ArgumentParser(description='This program intends to measure restaurant line')

    parser.add_argument('--mode', '-m', dest='mode',
                        help='Select mode to get images, online or offline')
    parser.add_argument('--sample', '-s', dest='img_input',
                        help='Classify one image for test')
    parser.add_argument('--thresh', '-t', dest='thresh_value', default = 0.15,
                        help='Select threshold for neural network classification')
    args = parser.parse_args()
    thresh_value = args.thresh_value
    

    if not os.path.exists('outputs_grafico'):
        os.mkdir('outputs_grafico')

    count = 0
  
    imglist = glob.glob("~/restaurant-flow-analysis/Vision/darknet-nnpack/images/*.jpg")
    imglist.sort()
    imgcount = 0
    imgmax = len(imglist)

    dados_fila = open('dados_fila.csv', mode='w')
    dados_fila_writer = csv.writer(dados_fila, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    dados_fila_writer.writerow(['Numero de pessoas','tamanho da fila','data','Numero de pessoas a esquerda','Numero de pessoas a direita','Tempo de execucao'])

    m = 14
    while imgcount < imgmax:

        m += 1
        data = '2019-11-11 %d:%s:00' % (11+m/60,str(m%60).zfill(2))
        print 11+m/60
        print m%60
        print data
        try:
            time_start = time.time()

            if True:
                imagename = imglist[imgcount]
                image = cv2.imread(imagename)
                imgcount += 1
                image = image[300:1000,350:1500]
                 
            if True:

                ##Passa a imagem de entrada para a rede neural
                out_img = 'outputs_grafico/out' + str(count).zfill(4)
                bashCommand = "./darknet detect yolov3-tiny-person.cfg yolov3-tiny-person_40000.weights %s -thresh %s -out %s" % (input_img, thresh_value, out_img)
                print bashCommand
                print bashCommand.split()
                process = Popen(bashCommand.split(), stdout=PIPE)
                output, error = process.communicate()
                print output

                ##Filtra os dados de saida da rede neural
                output = output.split("\n")
                detections = np.array(output[1:-1])
                left_line_counter = 0
                right_line_counter = 0
                people_counter = 0 
                status_fila = "pequena"

                print detections

                people_counter = len(detections)

                print people_counter
                            
                if people_counter > 10:
                    status_fila = "media"
                if people_counter > 20:
                    status_fila = "grande"

                timestamp = time.time()
                cycle_time = timestamp-time_start
                
                lista = []
                ##salva os dados processdor em um txt
                lista.append(str(people_counter)+'\n')
                lista.append(str(status_fila)+'\n')
                lista.append(data+'\n')

                dados_fila_writer.writerow(lista)
 
                count += 1

        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print e
            print repr(e)
            print e.args
            time.sleep(5)
            # sys.exit(1)

    dados_fila.close()
                    


if __name__ == '__main__':
    main()
