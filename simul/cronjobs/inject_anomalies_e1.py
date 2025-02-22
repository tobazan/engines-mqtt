import paho.mqtt.client as mqtt
import time
import numpy as np
import json
from datetime import datetime
import os

# MQTT broker details
broker = "mosquitto"
port = 1883
topic = "engine1/telemetry"

# Shared flag file
flag_file = "/app/shared/anomaly_active_e1.txt"

# Simulate anomalies
def inject_anomalies():
    # Create the shared flag file
    with open(flag_file, "w") as f:
        f.write("anomaly_active")

    client = mqtt.Client()
    client.connect(broker, port, 60)

    for _ in range(5):  # Send anomalies 5 iterations with 3-second sleep
        # Worsen values
        telemetry = {
            "event_time": datetime.now().isoformat(),
            "oil_temp": float(np.random.normal(150, 20)),       # Higher oil temperature
            "ambient_temp": float(np.random.normal(30, 5)),
            "fuel_pressure": float(np.random.normal(30, 5)),    # Lower fuel pressure
            "rpm": int(np.random.normal(6000, 1000)),           # Higher engine speed
            "voltage": float(np.random.normal(25, 2)),          # Lower  voltage
            "vibrations": float(np.random.exponential(20)),     # Higher vibrations
        }

        # Publish
        client.publish(topic, json.dumps(telemetry, separators=(",", ":")))
        time.sleep(3)

    # Delete the shared flag file
    os.remove(flag_file)

if __name__ == "__main__":
    inject_anomalies()