import time
import random
import json
import ibmiotf.application
import ibmiotf.device
import sys

#Provide your IBM Watson Device Credentials
organization = "zkpdkt"
deviceType = "iotdevice"
deviceId = "1001"
authMethod = "token"
authToken = "1234567890"


# Initialize the device client.
Waterlevel=0

def myCommandCallback(cmd):
    print("Message received from IBM IoT Platform: %s" % cmd.data['command'])

    
    if cmd.data['command']=='Servomotor ON':
                print("Servomotor ON is received")

                
    elif cmd.data['command']=='Servomotor OFF':
                print("Servomotor OFF is received")

                
    elif cmd.data['command']=='WaterPump ON':
                 print("Water Pump ON is received")

                 
    elif cmd.data['command']=='WaterPump OFF':
                 print("Water Pump OFF is received")

    if cmd.command == "setInterval":
                if 'interval' not in cmd.data:
                        print("Error - command is missing required information: 'interval'")
                else:
                        interval = cmd.data['interval']
    elif cmd.command == "print":
                if 'message' not in cmd.data:
                        print("Error - command is missing required information: 'message'")
                else:
                        print(cmd.data['message'])

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
    Waterlevel=random.randint(0,100)
    data={"d":{'Waterlevel': Waterlevel}}
    def myOnPublishCallback():
        print("published Waterlevel = %s" %Waterlevel,"to ibm watson iot")
        
    success = deviceCli.publishEvent("Data", "json", data, qos=0, on_publish=myOnPublishCallback)
    if not success:
       print("Not connected to IOTF")
    time.sleep(2)
    
    deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()

