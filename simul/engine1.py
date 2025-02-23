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
    if not os.path.exists("/app/shared/anomaly_active_e1.txt"):
        # SIMULATE HARSH CONDITIONS
        telemetry = {
            "event_time": datetime.now().isoformat(),
            "oil_temp": float(np.random.normal(120, 10)),       # Oil temperature
            "ambient_temp": float(np.random.normal(30, 5)),     # Ambient temperature
            "fuel_pressure": float(np.random.normal(50, 5)),    # Fuel pressure
            "rpm": int(np.random.normal(5000, 500)),            # Engine speed
            "voltage": float(np.random.normal(28, 1)),          # Voltage
            "vibrations": float(np.random.exponential(10)),     # Vbrations
        }

        # PUBLISH TELEMTRY EVERY 3 SECONDS
        client.publish("engine1/telemetry", json.dumps(telemetry, separators=(",", ":")))
        time.sleep(3)