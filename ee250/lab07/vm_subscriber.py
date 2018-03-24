import paho.mqtt.client as mqtt
import time

# Ultrasonic ranger callback
def ultrasonic_callback(client, userdata, message):
    print(str(message.payload, "utf-8"))

# Button callback
def button_callback(client, userdata, message):
    print(str(message.payload, "utf-8"))

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    # Subscribe to ultrasonic ranger
    client.subscribe("anrg-pi7/ultrasonicRanger")
    client.message_callback_add("anrg-pi7/ultrasonicRanger", ultrasonic_callback)

    # Subscribe to button
    client.subscribe("anrg-pi7/button")
    client.message_callback_add("anrg-pi7/button", button_callback)

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
            

