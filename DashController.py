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






############ Printing Received Data Function

def on_message(client, userdata, message):
   
    ##print(message.topic,"says: ",str(message.payload.decode("utf-8")))
    mylist=str(message.payload.decode("utf-8")).split(':')
    global GearValue
    stringa =list(mylist[2])
    if GearValue!=int(stringa[0]):
   	 GearValue = int(stringa[0])
   	 tempGearValue = GearValue
   	 index = 0;
   	 lista = [0,0,0,0]
   	 while tempGearValue>=1:
   		 lista[index]= tempGearValue%2
    		 tempGearValue = int(tempGearValue/2)
       		 index = index + 1
    ###################################
   	 revlista = list(reversed(lista))
   	 print(revlista)
    ###################################
   	 bcdPin0 = lista[0]
    	 bcdPin1 = lista[1]
    	 bcdPin2 = lista[2]
    	 bcdPin3 = lista[3]

    	 GPIO.output(23,bcdPin0)
    	 GPIO.output(17,bcdPin1)
    	 GPIO.output(27,bcdPin2)       
    	 GPIO.output(22,bcdPin3)
	
    
    

    
   
########################################
    
broker_address="localhost" 

print("creating new instance")

client = mqtt.Client("GearReader") 
client.on_message=on_message #attach function to callback

print("connecting to broker")
client.connect(broker_address) #connect to broker
##client.loop_start() #start the loop
##SUBSCRIPTIONS

#to subscribe just type:
#client.subscribe("$SYS/formatted/ <formatted data Channel-name> ")

print("Subscribing to topic","formatted/gear")
client.subscribe("data/formatted/gear") #subscribing to Gear Channel

client.loop_start()

while True:

	debugFlag = GPIO.input(5)
	telemetryFlag = GPIO.input(6)
	accellerationModeFlag = GPIO.input(26)
	dataLoggerFlag = GPIO.input(16)
	print("debug: ",debugFlag)
	print("telemetry: ",telemetryFlag)
	print("accellerationMode: ",accellerationModeFlag)
	print("dataLogger: ",dataLoggerFlag)

	

