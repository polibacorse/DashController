import paho.mqtt.client as mqtt #import the client1
import time
import RPi.GPIO as GPIO
###SETTING UP GPIOs 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(5, GPIO.IN)
GPIO.setup(6, GPIO.IN)
GPIO.setup(26, GPIO.IN)
GPIO.setup(16, GPIO.IN)
global GearValue
GearValue = 0



def dec2binary(dec): ##function used to convert decimal numbers to binary numbers

    index = 0
    revBinary = [0,0,0,0]
    while dec >= 1:
        revBinary[index]=(dec%2)
        dec = int(dec/2)
        index = index + 1

    binary = list(reversed(revBinary))
    return(binary)



############ function used when messages are received

def on_message(client, userdata, message):
   
    ##print(message.topic,"says: ",str(message.payload.decode("utf-8")))
    
    #############processing message to collect GearValue
    rawMessage=str(message.payload.decode("utf-8")).split(':')
    global GearValue
    stringa =list(rawMessage[2])
    
    if GearValue!=int(stringa[0]):
        GearValue = int(stringa[0])
        binary = dec2binary(GearValue)
        GPIOstateList = list( reversed(binary))
        print(binary)
        ##updating GPIO state
        GPIO.output(23, GPIOstateList[0])
        GPIO.output(17, GPIOstateList[1])
        GPIO.output(27, GPIOstateList[2])       
        GPIO.output(22, GPIOstateList[3])
	
    
    

    
   
########################################
    
broker_address="localhost" 

print("creating new instance")

client = mqtt.Client("DashController") 
client.on_message=on_message #attach function to callback

print("connecting to broker")
client.connect(broker_address) #connect to broker

##########################################SUBSCRIPTIONS

#to subscribe just type:
#client.subscribe("data/formatted/ <formatted data Channel-name> ")


client.subscribe("data/formatted/gear") #subscribing to Gear Channel
client.subscribe("data/formatted/auto_acc_flag")
client.subscribe("data/formatted/debug_mode")
client.subscribe("data/formatted/datalog_on-off")
client.subscribe("data/formatted/telemetria_on-off")



client.loop_forever()

while True:
        ##reading switches states
	debugFlag = GPIO.input(5)
	telemetryFlag = GPIO.input(6)
	accellerationModeFlag = GPIO.input(26)
	dataLoggerFlag = GPIO.input(16)

	##printing and publishing switches states
	print("debug: ",debugFlag)
	print("telemetry: ",telemetryFlag)
	print("accellerationMode: ",accellerationModeFlag)
	print("dataLogger: ",dataLoggerFlag)
	
	client.publish("data/formatted/auto_acc_flag",accellerationModeFlag)
	client.publish("data/formatted/debug_mode", debugFlag)
	client.publish("data/formatted/datalog_on-off", dataLoggerFlag)
	client.publish("data/formatted/telemetria_on-off", telemetryFlag)

	
