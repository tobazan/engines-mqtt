import paho.mqtt.client as mqtt
import time
import numpy as np
import json
import os
from datetime import datetime

# MQTT broker details
broker = "mosquitto"
port = 1883
topic = "engine2/telemetry"

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
    if not os.path.exists("/app/shared/anomaly_active_e2.txt"):
        # SIMULATE NEW ENGINE
        telemetry = {
            "event_time": datetime.now().isoformat(),
            "oil_temp": float(np.random.normal(90, 5)),             # Oil temperature
            "ambient_temp": float(np.random.normal(25, 2)),         # Ambient temperature
            "fuel_pressure": float(np.random.normal(40, 3)),        # Fuel pressure
            "rpm": int(np.random.normal(3000, 200)),                # Engine speed
            "voltage": float(np.random.normal(28, 0.5)),            # Voltage
            "vibrations": float(np.random.exponential(2)),          # Vibrations    
        }

        # PUBLISH TELEMTRY EVERY 3 SECONDS
        client.publish(topic, json.dumps(telemetry, separators=(",", ":")))
        time.sleep(3)