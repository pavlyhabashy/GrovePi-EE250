import paho.mqtt.client as mqtt
import time

import requests
import json
from datetime import datetime

# MQTT variables
broker_hostname = "eclipse.usc.edu"
broker_port = 11000
ultrasonic_ranger1_topic = "ultrasonic_ranger1"
ultrasonic_ranger2_topic = "ultrasonic_ranger2"

# Lists holding the ultrasonic ranger sensor distance readings. Change the 
# value of MAX_LIST_LENGTH depending on how many distance samples you would 
# like to keep at any point in time.
MAX_LIST_LENGTH = 100
ranger1_dist = []
ranger2_dist = []


# 40 110
def ranger1_callback(client, userdata, msg):
    global ranger1_dist
    if (int(msg.payload) >= 125):
        ranger1_dist.append(125)
    else:
        ranger1_dist.append(int(msg.payload))
    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger1_dist = ranger1_dist[-MAX_LIST_LENGTH:]

def ranger2_callback(client, userdata, msg):
    global ranger2_dist
    if (int(msg.payload) >= 125):
        ranger2_dist.append(125)
    else:
        ranger2_dist.append(int(msg.payload))
    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger2_dist = ranger2_dist[-MAX_LIST_LENGTH:]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(ultrasonic_ranger1_topic)
    client.message_callback_add(ultrasonic_ranger1_topic, ranger1_callback)
    client.subscribe(ultrasonic_ranger2_topic)
    client.message_callback_add(ultrasonic_ranger2_topic, ranger2_callback)

# The callback for when a PUBLISH message is received from the server.
# This should not be called.
def on_message(client, userdata, msg): 
    print(msg.topic + " " + str(msg.payload))

def printIt(array):
    for i in range(0, len(array) - 1):
        print(array[i])
        

def moving_average(theArray, movAvgBuf, size):
    avg = sum(theArray[-size:])/size
    movAvgBuf.append(avg)

def diffAdj(movAvgBuf1, diffMov):
    for i in range(0, len(diffMov) - 1):
        diffMov[i] = diffMov[i+1]
    print("movavgbuf1")
    print(movAvgBuf1)
    for i in range(0, len(movAvgBuf1) - 1):
        sub = movAvgBuf1[i+1] - movAvgBuf1[i]
        if(abs(sub) < 0.5):
            diffMov[i] = 0
        else:
            diffMov[i] = sub


def detLoc(movAvgBuf1, movAvgBuf2, min, max):
    if( (movAvgBuf1[-1] <= min) & (movAvgBuf2[-1] >= max) ):
        print("Still-Right")
    elif( (movAvgBuf1[-1] >= max) & (movAvgBuf2[-1] <= min) ):
        print("Still-Left")
    elif( (movAvgBuf1[-1] <= max) & (movAvgBuf2[-1] <= max) ):
        print("Still-Middle")


def detMov(diffAve1, diffAve2):
    # if ((abs(diffAve1[-1]) < 2) & (abs(diffAve2[-1]) < 2)):
    #     print(abs(diffAve1[-1]))
    #     detLoc(movAvgBuf1, movAvgBuf2, 40, 120)
    elif((diffAve1[-1] > 3) & (diffAve2[-1] < -3)):
        print("Moving Left")
    elif((diffAve2[-1] > 3) & (diffAve1[-1] < -3)):
        print("Moving Right")
    elif((diffAve1[-1] > 3)):
        print("Moving Left")
    elif((diffAve2[-1] > 3)):
        print("Moving Right")
    elif((diffAve1[-1] < -3)):
        print("Moving Right")
    elif((diffAve2[-1] < -3)):
        print("Moving Left")
    else:
        print("Something went wrong")



if __name__ == '__main__':
    # Connect to broker and start loop    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_hostname, broker_port, 60)
    client.loop_start()

    movAvgBuf1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    movAvgBuf2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    diffMov1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    diffMov2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # diffAvg1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # diffAvg2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    hdr = {
        'Content-Type': 'application/json',
        'Authorization': None
    }
    k = 0
    i = 10
    while True:
        """ You have two lists, ranger1_dist and ranger2_dist, which hold a window
        of the past MAX_LIST_LENGTH samples published by ultrasonic ranger 1
        and 2, respectively. The signals are published roughly at intervals of
        200ms, or 5 samples/second (5 Hz). The values published are the 
        distances in centimeters to the closest object. Expect values between 
        0 and 512. However, these rangers do not detect people well beyond 
        ~125cm. """
        
        # TODO: detect movement and/or position
        print("ranger1: " + str(ranger1_dist[-1:]) + ", ranger2: " + 
            str(ranger2_dist[-1:]))

        # Moving average buffer
        moving_average(ranger1_dist, movAvgBuf1, 5)
        moving_average(ranger2_dist, movAvgBuf2, 5)
        print(movAvgBuf1[-5:])
        print(movAvgBuf2[-5:])


        print("Sensor 1 Average: " + str(movAvgBuf1[-1:]) +
            " Sensor 2 Average: " + str(movAvgBuf2[-1:]))


        diffAdj(movAvgBuf1[-5:], diffMov1[-5:])
        diffAdj(movAvgBuf2[-5:], diffMov2[-5:])
        print(diffMov1[-5:])
        print(diffMov2[-5:])

        #moving_average(diffMov1[-5:], diffAvg1[-5:], 5)
        #moving_average(diffMov2[-5:], diffAvg2[-5:], 5)
        #print(diffMov1[-5:])
        #print(diffMov2[-5:])
    

        # detLoc(movAvgBuf1[-5:], movAvgBuf2[-5:], 40, 110)
        # detLoc(movAvgBuf1, movAvgBuf2, 40, 110)
        # detMov(diffAvg1[-5:], diffAvg2[-5:])

        #flask
        # hdr = {
        # 'Content-Type': 'application/json',
        # 'Authorization': None
        # }
        # payload = {
        # 'time': str(datetime.now()),
        # 'event': detMov(diffAvg1, diffAvg2)
        # }

        # #flask
        # response = requests.post("http://0.0.0.0:5000/post-event", headers = hdr, data = json.dumps(payload))
        # print (response.json())

        
        time.sleep(0.2)
