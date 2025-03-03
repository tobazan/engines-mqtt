import json
import time
from datetime import datetime

import paho.mqtt.client as mqtt

import asyncio
import uuid
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

import os
from dotenv import load_dotenv

load_dotenv()

# ENV VARS
IOT_HUB_CONN_STR = os.get("HUB_CONN_STR")

# MQTT BROKER DETAILS
broker = "mosquitto"
port = 1883
topics = ["engine1/telemetry", "engine2/telemetry", "engine3/telemetry"]

# LOG PATHS
log_files = {
    "engine1/telemetry": "/app/logs/engine1_log.json",
    "engine2/telemetry": "/app/logs/engine2_log.json",
    "engine3/telemetry": "/app/logs/engine3_log.json"
}

# CREATE LOG DIR
os.makedirs("/app/logs", exist_ok=True)

async def az_bridge(payload,processing_time):
    device_client = IoTHubDeviceClient.create_from_connection_string(IOT_HUB_CONN_STR)
    await device_client.connect()

    msg = Message("{ \"DateTime\": \"" + str(processing_time) + "\"Payload\": \"" + payload + "\" }")
    msg.message_id = uuid.uuid4()
    msg.content_encoding = "utf-8"
    msg.content_type = "application/json"

    await device_client.send_message(msg)
    await device_client.shutdown()

def connect_with_retry(client, broker, port, retries=3, delay=2):
    for i in range(retries):
        try:
            client.connect(broker, port, 60)
            print("Connected to MQTT Broker!")
            return True
        except Exception as e:
            print(f"Connection failed (attempt {i + 1}/{retries}): {e}")
            time.sleep(delay)
    print("Failed to connect to MQTT Broker after retries.")
    return False

# MQTT on_message CALLBACK
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode("utf-8")
    processing_time = datetime.now().isoformat()

    # LOG WITH TS - APPEND TO LOG FILE
    log_entry = {"processing_time": processing_time,"data": json.loads(payload)}

    with open(log_files[topic], "a") as f:
        f.write(json.dumps(log_entry, separators=(",", ":")) + "\n")
    
    # SENT TO CLOUD ONLY TOPIC 1
    if topic == "engine1/telemetry":
        try:
           asyncio.run(az_bridge(payload,processing_time))
        except: 
            pass

# MQTT CLIENT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
if not connect_with_retry(client, broker, port):
    exit(1)  # Exit if connection fails after retries

for topic in topics:
    client.subscribe(topic)
    print(f"Subscribed to {topic}")

# START CLIENT
client.loop_forever()