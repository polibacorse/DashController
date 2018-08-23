#!/bin/env python3

import json
import paho.mqtt.client as mqtt  # import the client1

import RPi.GPIO as GPIO

# importing variables

debugSwitchPin = 5
telemetrySwitchPin = 6
accelerationModeSwitchPin = 26
dataLoggerSwitchPin = 16
lapEndButton = 10
BCD0Pin = 23
BCD1Pin = 17
BCD2Pin = 27
BCD3Pin = 22
LE_Strobe_Pin = 2


# SETTING UP GPIOs
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BCD0Pin, GPIO.OUT)
GPIO.setup(BCD1Pin, GPIO.OUT)
GPIO.setup(BCD2Pin, GPIO.OUT)
GPIO.setup(BCD3Pin, GPIO.OUT)
GPIO.setup(LE_Strobe_Pin, GPIO.OUT)
GPIO.setup(debugSwitchPin, GPIO.IN)
GPIO.setup(telemetrySwitchPin, GPIO.IN)
GPIO.setup(accelerationModeSwitchPin, GPIO.IN)
GPIO.setup(dataLoggerSwitchPin, GPIO.IN)
GPIO.setup(lapEndButton, GPIO.IN)


global GearValue
GearValue = 0
global LapNumber
LapNumber = 0


# function that reads buttons states
def buttonInterrupt(self):
    debugFlag = not GPIO.input(debugSwitchPin)
    telemetryFlag = not GPIO.input(telemetrySwitchPin)
    accelerationModeFlag = not GPIO.input(accelerationModeSwitchPin)
    dataLoggerFlag = not GPIO.input(dataLoggerSwitchPin)

    # printing and publishing switches states

    client.publish("data/formatted/auto_acc_flag", accelerationModeFlag)
    client.publish("data/formatted/debug_mode", debugFlag)
    client.publish("data/formatted/datalog_on-off", dataLoggerFlag)
    client.publish("data/formatted/telemetria_on-off", telemetryFlag)
    # print("debug: ", debugFlag)
    # print("telemetry: ", telemetryFlag)
    # print("accellerationMode: ", accelerationModeFlag)
    # print("dataLogger: ", dataLoggerFlag)


# function that increments lap number when lap button is pressed
def lapEndButtonInterrupt(self):
    global LapNumber
    LapNumber += 1
    client.publish("data/formatted/lapnumber", LapNumber)
    # print("lapNumber: ", LapNumber)


def dec2binary(dec):  # function used to convert decimal numbers to binary numbers

    index = 0
    revBinary = [0, 0, 0, 0]
    while dec >= 1:
        revBinary[index] = (dec % 2)
        dec = int(dec/2)
        index = index + 1

    binary = list(reversed(revBinary))
    return binary

# function called when messages are received


def on_message(client, userdata, message):

    # print(message.topic,"says: ",str(message.payload.decode("utf-8")))
    try:
        if message.topic == "data/formatted/gear":
            # processing message to collect GearValue
            jsonMessage = json.loads(message.payload.decode("utf-8"))
            currentGear = int(jsonMessage["value"])
            global GearValue
            
            if GearValue != currentGear:
                GearValue = currentGear
                binary = dec2binary(GearValue)
                GPIOstateList = list(reversed(binary))   # generating a list that contains the future state that the BCDpins will have to assume
                # print(binary)
                # updating GPIO state
                GPIO.output(LE_Strobe_Pin, 0)
                GPIO.output(BCD0Pin, GPIOstateList[0])
                GPIO.output(BCD1Pin, GPIOstateList[1])
                GPIO.output(BCD2Pin, GPIOstateList[2])
                GPIO.output(BCD3Pin, GPIOstateList[3])
                GPIO.output(LE_Strobe_Pin, 1)

    except:
        print("error")


########################################
    
broker_address = "localhost"

print("creating new instance")

client = mqtt.Client("DashController") 
client.on_message = on_message  # attach function to callback

print("connecting to broker")
client.connect(broker_address)  # connect to broker

# SUBSCRIPTIONS

# to subscribe just type:
# client.subscribe("data/formatted/ <formatted data Channel-name> ")


client.subscribe("data/formatted/gear")  # subscribing to Gear Channel
# client.subscribe("data/formatted/auto_acc_flag")
# client.subscribe("data/formatted/debug_mode")
# client.subscribe("data/formatted/datalog_on-off")
# client.subscribe("data/formatted/telemetria_on-off")
# client.subscribe("data/formatted/lapnumber")
client.publish("data/formatted/lapnumber", LapNumber)

# attaching interrupt functions
GPIO.add_event_detect(debugSwitchPin, GPIO.BOTH, callback=buttonInterrupt, bouncetime=1)
GPIO.add_event_detect(telemetrySwitchPin, GPIO.BOTH, callback=buttonInterrupt, bouncetime=1)
GPIO.add_event_detect(accelerationModeSwitchPin, GPIO.BOTH, callback=buttonInterrupt, bouncetime=1)
GPIO.add_event_detect(dataLoggerSwitchPin, GPIO.BOTH, callback=buttonInterrupt, bouncetime=1)
GPIO.add_event_detect(lapEndButton, GPIO.FALLING, callback=lapEndButtonInterrupt, bouncetime=5000)
###################

client.loop_forever()

while True:
    buttonInterrupt()
