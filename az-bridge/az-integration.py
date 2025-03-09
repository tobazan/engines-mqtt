import json
import time
from datetime import datetime, date

import paho.mqtt.client as mqtt

import asyncio
import uuid
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

import os

# ENV VARS
IOT_HUB_CONN_STR = os.getenv("HUB_CONN_STR")

# MQTT BROKER DETAILS
broker = "mosquitto"
port = 1883
topics = ["engine1/telemetry", "engine2/telemetry", "engine3/telemetry"]
today = date.today().strftime("%Y%m%d")

# LOG PATHS - FILE PER DAY
log_files = {
    "engine1/telemetry": f"/app/logs/engine1_log_{today}.json",
    "engine2/telemetry": f"/app/logs/engine2_log_{today}.json",
    "engine3/telemetry": f"/app/logs/engine3_log_{today}.json"
}

# CREATE LOG DIR
os.makedirs("/app/logs", exist_ok=True)

async def az_bridge(log_entry):
    device_client = IoTHubDeviceClient.create_from_connection_string(IOT_HUB_CONN_STR)
    await device_client.connect()

    msg = Message(json.dumps(log_entry, separators=(",", ":")))
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
    payload = message.payload.decode("utf-8")
    processing_time = datetime.now().isoformat()

    # LOG WITH TS - APPEND TO LOG FILE
    log_entry = {
                "processing_time": processing_time,
                "topic": message.topic,
                 "data": json.loads(payload)
                }

    with open(log_files[message.topic], "a") as f:
        f.write(json.dumps(log_entry, separators=(",", ":")) + "\n")
    
    # SENT TO CLOUD ONLY TOPIC 1
    if message.topic == "engine1/telemetry":
        try:
           asyncio.run(az_bridge(log_entry))
        except: 
            pass

# MQTT CLIENT
client = mqtt.Client()
client.on_message = on_message

if not connect_with_retry(client, broker, port):
    exit(1)  # Exit if connection fails after retries
for topic in topics:
    client.subscribe(topic)
    print(f"Subscribed to {topic}")

# START CLIENT
client.loop_forever()