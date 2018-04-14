import paho.mqtt.client as mqtt
import grovepi
from grovepi import *
import time
from grove_rgb_lcd import *

global ledPIN, buttonPIN
ledPIN = 3
dhtPIN = 7

# LED callback
def led_callback(client, userdata, message):
	# Print message sent from button (for debugging)
	# print(str(message.payload, "utf-8"))
    if (str(message.payload, "utf-8") == "LED_toggle"):
        if (digitalRead(ledPIN) == 1):
            digitalWrite(ledPIN, 0)
        elif(digitalRead(ledPIN) == 0):
            digitalWrite(ledPIN, 1)

# LCD callback
def lcd_callback(client, userdata, message):
	# Print text to console (for debugging)
	# print(str(message.payload, "utf-8"))
	
	# Set text on LCD
	setText(str(message.payload, "utf-8"))

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    # Subscribe to LED
    client.subscribe("anrg-pi7/led")
    client.message_callback_add("anrg-pi7/led", led_callback)
    print("Connected to LED topic")

    # Subscribe to LCD
    client.subscribe("anrg-pi7/lcd")
    client.message_callback_add("anrg-pi7/lcd", lcd_callback)
	print("Connected to LCD topic")


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
		# Read temperature and humidity
		[temp, hum] = dht(dhtPIN, 1)
		
		# Print to temperature and humidity to console (for debugging)
		# print ("temp =", temp, "C\thumidity =", hum, "%")
		
		# Publish temperature and humidity to their respective topics
		client.publish("anrg-pi7/temperature", str(temp))
		client.publish("anrg-pi7/humidity", str(hum))
		time.sleep(1) 
		
