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

# Create MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.connect(broker, port, 60)

while True:
    # IF ANOMALY INJECTION IS INACTIVE
    if not os.path.exists("/app/shared/anomaly_active_e3.txt"):
        # SIMULATE OLD ENGINE
        if np.random.random() < 0.085:  # 8.5% PROB FAILURE
            telemetry = {
                "oil_temp": None,
                "ambient_temp": None,
                "fuel_pressure": None,
                "rpm": None,
                "voltage": None,
                "vibrations": None,
            }
        else:
            telemetry = {
                "event_time": datetime.now().isoformat(),
                "oil_temp": float(np.random.normal(100, 15)),       # Moderate oil temperature
                "ambient_temp": float(np.random.normal(28, 3)),     # Ambient temperature
                "fuel_pressure": float(np.random.normal(45, 4)),    # Fuel pressure
                "rpm": int(np.random.normal(4000, 300)),            # Engine speed
                "voltage": float(np.random.normal(27, 1)),          # Voltage
                "vibrations": float(np.random.exponential(5)),      # Vibrations
            }

        # PUBLISH TELEMTRY EVERY 3 SECONDS
        client.publish(topic, json.dumps(telemetry, separators=(",", ":")))
        time.sleep(3)