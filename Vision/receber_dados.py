import paho.mqtt.client as mqtt
import json
import time

def on_connect(client, userdata, flags, rc):
    print("Connected!")
    client.subscribe("sub/ji9j5sk4lq3l/out")

def on_message(client, data, msg):
    print(msg.topic + " " + str(msg.payload))


client2 = mqtt.Client()
client2.on_message = on_message
client2.on_connect = on_connect
client2.username_pw_set("ji9j5sk4lq3l", "gQdoyf4UBNIk")
client2.connect("mqtt.demo.konkerlabs.net", 1883)
client2.loop_forever()