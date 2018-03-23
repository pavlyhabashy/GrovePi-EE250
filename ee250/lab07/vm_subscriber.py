"""EE 250L Lab 07 Skeleton Code

Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time


def ultrasonic_callback(client, userdata, message):
    print(str(message.payload))

def button_callback(client, userdata, message):
    print(str(message.payload, "utf-8"))

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("anrg-pi7/ultrasonicRanger")
    client.message_callback_add("anrg-pi7/led", ultrasonic_callback)

    client.subscribe("anrg-pi7/button")
    client.message_callback_add("anrg-pi7/led", button_callback)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)
            

