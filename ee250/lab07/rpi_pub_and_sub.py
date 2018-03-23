"""EE 250L Lab 07 Skeleton Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import grovepi
import time

global ultrasonicPIN, ledPIN, buttonPIN
ultrasonicPIN = 4
ledPIN = 3
buttonPIN = 2


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("anrg-pi7/led")
    client.message_callback_add("anrg-pi7/led", LED)

    client.subscribe("anrg-pi7/lcd")
    client.message_callback_add("anrg-pi7/lcd", LCD)

    client.publish("anrg-pi7/ultrasonicRanger", distance)


def custom_callback(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    print("custom_callback: " + message.topic + " " + str(message.payload))
    print("custom_callback: message.payload is of type " + 
          str(type(message.payload)))


#Default message callback. Please use custom callbacks.

# def on_message(client, userdata, msg):
#     print("on_message: " + msg.topic + " " + str(msg.payload))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        # print("delete this line")
        distance = str(grovepi.ultrasonicRead(ultrasonicPIN))
        print(distance)
        client.publish("anrg-pi7/ultrasonicRanger", distance)
        time.sleep(1)
            

