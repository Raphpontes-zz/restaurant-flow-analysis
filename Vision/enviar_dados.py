import paho.mqtt.client as mqtt
import json
import time

client = mqtt.Client()
client.username_pw_set("ji9j5sk4lq3l", "gQdoyf4UBNIk")
client.connect("mqtt.demo.konkerlabs.net", 1883)
timestamp = time.time()
print timestamp
client.publish("data/ji9j5sk4lq3l/pub/teste", 
                 json.dumps({"temperature": 22, "unit": "celsius", "_lat": -23.5746571, "_lon": -46.6910183 , "_hdop": 10, "_elev": 3.66, "_ts": timestamp}))

