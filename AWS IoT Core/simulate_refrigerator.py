'''
Python script to simulate a virtual refrigeration unit, written by @snowcrashcode

'''


from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import random

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print(f"Received a new message: {message.payload}")
    print(f"from topic: {message.topic}\n")

# Initialize the MQTT client
myMQTTClient = AWSIoTMQTTClient("SimulatedRefrigerationUnit")
myMQTTClient.configureEndpoint("a21hhk6vuxg487-ats.iot.ap-southeast-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials(
    "C:/users/notan/.aws/aws-iot-device-sdk-python-v2/certs/AmazonRootCA1.pem",     # Path to root CA Certificate
    "C:/Users/notan/.aws/aws-iot-device-sdk-python-v2/certs/13f5d247d3c793049f0f27408104d8cf000c58241fd7100f5de29be33d6f2ffc-private.pem.key",  # Path to private key 
    "C:/Users/notan/.aws/aws-iot-device-sdk-python-v2/certs/13f5d247d3c793049f0f27408104d8cf000c58241fd7100f5de29be33d6f2ffc-certificate.pem.crt")

# Configure the MQTT Client
myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline publish queueing
myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec

# Connect and subscribe to AWS IoT
myMQTTClient.connect()
myMQTTClient.subscribe("refrigeration/temperature", 1, customCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
while True:
    temperature = random.uniform(-20, 5) # Simulate temperature readings
    message = {
        "temperature": temperature,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    myMQTTClient.publish("refrigeration/temperature", json.dumps(message), 1)
    print(f"Published: {message} to the topic: refrigeration/temperature")
    time.sleep(5) # Publish every 5 seconds