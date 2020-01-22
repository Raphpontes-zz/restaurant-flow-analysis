from subprocess import Popen, PIPE
import numpy as np
import sys
import time
import cv2
import os
import shutil 
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

    
    weights_list = glob.glob("backup/*.weights")
    weights_list.sort()

    dados_treino = open('dados_treino.csv', mode='w')
    dados_treino_writer = csv.writer(dados_treino, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    dados_treino_writer.writerow(['Peso','Fila pequena','Fila media','Fila grande','Tempo de execucao'])

    imagem_pequena = "~/Desktop/tcc/restaurant-flow-analysis/Vision/darknet-nnpack/imagens/out0232_cutted.jpg"
    imagem_media = "~/Desktop/tcc/restaurant-flow-analysis/Vision/darknet-nnpack/imagens/out0121_cutted.jpg"
    imagem_grande = "~/Desktop/tcc/restaurant-flow-analysis/Vision/darknet-nnpack/imagens/out0106_cutted.jpg"
    imagem_noite = "~/Desktop/tcc/restaurant-flow-analysis/Vision/darknet-nnpack/imagens/out0455_cutted.jpg"

    for weight in weights_list:
        try:
            time_start = time.time()
                 

            if True:

                ##Passa a imagem de entrada para a rede neural
                print weight
                out_img = 'testeimg'
                people_counter = [0,0,0,0]

                bashCommand = "./darknet detect yolov3-tiny-person.cfg %s %s -thresh %s -out %s" % (weight, imagem_pequena, thresh_value, out_img)
                process = Popen(bashCommand.split(), stdout=PIPE)
                output, error = process.communicate()
                ##Filtra os dados de saida da rede neural
                output = output.split("\n")
                detections = np.array(output[1:-1])
                # time.sleep(3)
                people_counter[0] = len(detections)

                bashCommand = "./darknet detect yolov3-tiny-person.cfg %s %s -thresh %s -out %s" % (weight, imagem_media, thresh_value, out_img)
                process = Popen(bashCommand.split(), stdout=PIPE)
                output, error = process.communicate()
                ##Filtra os dados de saida da rede neural
                output = output.split("\n")
                detections = np.array(output[1:-1])
                # time.sleep(3)
                people_counter[1] = len(detections)

                bashCommand = "./darknet detect yolov3-tiny-person.cfg %s %s -thresh %s -out %s" % (weight, imagem_grande, thresh_value, out_img)
                process = Popen(bashCommand.split(), stdout=PIPE)
                output, error = process.communicate()
                ##Filtra os dados de saida da rede neural
                output = output.split("\n")
                detections = np.array(output[1:-1])
                # time.sleep(3)
                people_counter[2] = len(detections)

                bashCommand = "./darknet detect yolov3-tiny-person.cfg %s %s -thresh %s -out %s" % (weight, imagem_noite, thresh_value, out_img)
                process = Popen(bashCommand.split(), stdout=PIPE)
                output, error = process.communicate()
                ##Filtra os dados de saida da rede neural
                output = output.split("\n")
                detections = np.array(output[1:-1])
                # time.sleep(3)
                people_counter[3] = len(detections)



                timestamp = time.time()
                cycle_time = timestamp-time_start
                
                lista = []
                ##salva os dados processdor em um txt
                lista.append(str(weight)+'\n')
                lista.append(str(people_counter[0])+'\n')
                lista.append(str(people_counter[1])+'\n')
                lista.append(str(people_counter[2])+'\n')
                lista.append(str(people_counter[3])+'\n')

                dados_treino_writer.writerow(lista)



        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print e
            print repr(e)
            print e.args
            time.sleep(5)
            # sys.exit(1)

    dados_treino.close()
                    


if __name__ == '__main__':
    main()
