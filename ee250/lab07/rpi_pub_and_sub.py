import paho.mqtt.client as mqtt
import grovepi
from grovepi import *
import time
from grove_rgb_lcd import *

global ultrasonicPIN, ledPIN, buttonPIN
ultrasonicPIN = 4
ledPIN = 3
buttonPIN = 2

# LED callback
def led_callback(client, userdata, message):

    if str(message.payload, "utf-8") == "LED_ON":
        # Turn on LED
        digitalWrite(ledPIN, 1)
        print("LED_ON")
    elif str(message.payload, "utf-8") == "LED_OFF":
        # Turn off LED
        digitalWrite(ledPIN, 0)
        print("LED_OFF")
# LCD callback
def lcd_callback(client, userdata, message):
    if str(message.payload, "utf-8") == "w":
        print("w")
        setText("w")
    elif str(message.payload, "utf-8") == "a":
        print("a")
        setText("a")
    elif str(message.payload, "utf-8") == "s":
        print("s")
        setText("s")
    elif str(message.payload, "utf-8") == "d":
        print("d")
        setText("d")

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    # Subscribe to LED
    client.subscribe("anrg-pi7/led")
    client.message_callback_add("anrg-pi7/led", led_callback)

    # Subscribe to LED
    client.subscribe("anrg-pi7/lcd")
    client.message_callback_add("anrg-pi7/lcd", lcd_callback)

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
    pinMode(ledPIN,"OUTPUT")
    time.sleep(1)
    setRGB(250,250,250)
    while True:
        # Read ultrasonic ranger
        distance = ultrasonicRead(ultrasonicPIN)
        # Print locally on console
        print(str(distance))
        # Publish to topic "anrg-pi7/ultrasonicRanger"
        client.publish("anrg-pi7/ultrasonicRanger", distance)
        time.sleep(1)

        # If button is pressed
        if (grovepi.digitalRead(2) > 0):
            # Publish the string "Button pressed!" to “anrg-pi#/button”
            client.publish("anrg-pi7/button", "Button pressed!")
            

