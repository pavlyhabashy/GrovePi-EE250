"""EE 250L Lab 07 Skeleton Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import grovepi
import time

global ultrasonicPIN, ledPIN, buttonPIN
ultrasonicPIN = 4
ledPIN = 3
buttonPIN = 2
# lcdPIN = #


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("anrg-pi7/led")
    client.message_callback_add("anrg-pi7/led", led_callback)

    client.subscribe("anrg-pi7/lcd")
    client.message_callback_add("anrg-pi7/lcd", lec_callback)

def led_callback(client, userdata, message):
    try:

    except:


    if str(message.payload) == "LED_ON":
        # Turn on LED
        digitalWrite(ledPIN, 1)
        print("LED_ON")
    elif str(message.payload) == "LED_OFF":
        # Turn off LED
        digitalWrite(ledPIN, 0)
        print("LED_ON")

def lcd_callback(client, userdata, message):

    if str(message.payload) == "w":
        # Write to LCD

    elif str(message.payload) == "a":
        # Write to LCD

    elif str(message.payload) == "s":
        # Write to LCD

    elif str(message.payload) == "d":
        # Write to LCD

# Default message callback. Please use custom callbacks.
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
        distance = str(grovepi.ultrasonicRead(ultrasonicPIN))
        print(distance)
        client.publish("anrg-pi7/ultrasonicRanger", distance)
        time.sleep(1)

        # If button is pressed
        if grovepi.digitalOutput(2) > 0:
            # Publish the string "Button pressed!" to “anrg-pi#/button”
            client.publish("anrg-pi7/button", "Button pressed!")
            

