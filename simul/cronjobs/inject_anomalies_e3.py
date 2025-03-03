import paho.mqtt.client as mqtt
import time
import numpy as np
import json
from datetime import datetime
import os

# MQTT broker details
broker = "mosquitto"
port = 1883
topic = "engine3/telemetry"

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

# Shared flag file
flag_file = "/app/shared/anomaly_active_e3.txt"

# Simulate anomalies
def inject_anomalies():
    # Create the shared flag file
    with open(flag_file, "w") as f:
        f.write("anomaly_active")

    # Create MQTT client
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.connect(broker, port, 60)

    for _ in range(30):  # Send anomalies 30 iterations with 3-second sleep
        # Worsen values
        telemetry = {
            "event_time": datetime.now().isoformat(),
            "oil_temp": float(np.random.normal(120, 18)),       # Higher oil temperature
            "ambient_temp": float(np.random.normal(28, 4)),
            "fuel_pressure": float(np.random.normal(40, 6)),    # Lower fuel pressure
            "rpm": int(np.random.normal(4350, 380)),            # Higher engine speed
            "voltage": float(np.random.normal(26, 3)),          # Lower  voltage
            "vibrations": float(np.random.exponential(6.5)),    # Higher vibrations
        }

        # Publish
        client.publish(topic, json.dumps(telemetry, separators=(",", ":")))
        time.sleep(3)

    # Delete the shared flag file
    os.remove(flag_file)

if __name__ == "__main__":
    inject_anomalies()