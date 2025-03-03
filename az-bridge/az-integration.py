import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime
import os

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
    # LOG WITH TS
    log_entry = {
        "processing_time": datetime.now().isoformat(),
        "data": json.loads(payload)
    }
    # APPEND TO LOG FILE
    with open(log_files[topic], "a") as f:
        f.write(json.dumps(log_entry, separators=(",", ":")) + "\n")

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