from paho.mqtt import client as mqtt
import time
import json


client = mqtt.Client("GearSimulator")
client.connect("localhost")

client.loop_start()


while True:
    for i in range(0, 10):
        GearMessageDict = {'time': time.time(), 'value': i }
        GearMessageJSON = json.dumps(GearMessageDict)
        client.publish("data/formatted/gear", GearMessageJSON)
        print(GearMessageJSON)
        time.sleep(1)
