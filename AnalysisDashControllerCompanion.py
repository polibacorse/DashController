import paho.mqtt.client as mqtt  # import the client1
import json


global gear
global debug
global telemetry
global accmode
global datalog
global lapnum
gear = 0
debug = 0
telemetry = 0
accmode = 0
datalog = 0
lapnum = 0
# Printing Received Data Function


def on_message(client, userdata, message):

    global gear
    global debug
    global telemetry
    global accmode
    global datalog
    global lapnum

    if message.topic == "data/formatted/gear":
        jsonMessage = json.loads(message.payload.decode("utf-8"))
        gear = int(jsonMessage['value'])
        
    elif message.topic == "data/formatted/debug_mode":
        debug = str(message.payload.decode("utf-8"))
    elif message.topic == "data/formatted/auto_acc_flag":
        accmode = str(message.payload.decode("utf-8"))
    elif message.topic == "data/formatted/telemetria_on-off":
        telemetry = str(message.payload.decode("utf-8"))
    elif message.topic == "data/formatted/datalog_on-off":
        datalog = str(message.payload.decode("utf-8"))
    elif message.topic == "data/formatted/lapnumber":
        lapnum = str(message.payload.decode("utf-8"))
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print("############################################ ")
    print()
    print("gear : ", gear)
    print("debug : ", debug)
    print("telemetry : ", telemetry)
    print("accmode : ", accmode)
    print("datalog : ", datalog)
    print("lapnumber : ", lapnum)


########################################


print("creating new instance")

client = mqtt.Client("Analysis companion")
client.on_message = on_message  # attach function to callback

print("connecting to broker")
client.connect("localhost")  # connect to broker


# SUBSCRIPTIONS

# to subscribe just type:
# client.subscribe("data/formatted/ <formatted data Channel-name> ")


client.subscribe("data/formatted/gear")  # subscribing to gear Channel
client.subscribe("data/formatted/auto_acc_flag")
client.subscribe("data/formatted/debug_mode")
client.subscribe("data/formatted/datalog_on-off")
client.subscribe("data/formatted/telemetria_on-off")
client.subscribe("data/formatted/lapnumber")


client.loop_forever()  # start the loop
