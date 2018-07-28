# DashController
Python script used as software interface for Dashboard hardware, in particular:
-Reads the state of the Switches
-Reads Gear value from MQTT and converts it in a 4 bit signal that is used by the BCD latch to control the 7 seg display
-Keeps count of the LapNumber
-sends LapNumber and Switches states via MQTT to the propers topics
-it has inside some commented line that can be uncommented for debug purposes
[needs root permissions]


# AnalysisDashControllerCompanion
A software that subscribes to DashController topics and shows a more readable output of DashController making easier the debugging
[needs that DashController is in running mode]
[needs that Mosquitto is in running mode]
