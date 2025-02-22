import paho.mqtt.client as mqtt
import time
import numpy as np
import json
import os
from datetime import datetime

client = mqtt.Client()
client.connect("mosquitto", 1883, 60)

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
        client.publish("engine2/telemetry", json.dumps(telemetry, separators=(",", ":")))
        time.sleep(3)