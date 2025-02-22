# IIoT Telemtry to the Cloud

```
engines/
├── README.md
├── docker-compose.yml
├── mqtt/
│   ├── config/
│   │   ├── mosquitto.conf
│   └── data/
├── shared/
|   ├── anomaly_active_e1.txt
|   ├── anomaly_active_e2.txt
|   └── anomaly_active_e3.txt
├── simul/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── engine1.py
│   ├── engine2.py
│   ├── engine3.py
│   └── cronjobs/
│       ├── inject_anomalies_e1.py
│       ├── inject_anomalies_e2.py
│       ├── inject_anomalies_e3.py
│       ├── anomalies_e1.sh
│       ├── anomalies_e2.sh
│       ├── anomalies_e3.sh
│       └── crontab
└── testing/
    ├── logs/
    ├── Dockerfile
    ├── requirements.txt
    └── logger.py
```

### High Level Steps
- Create an Azure IoT Hub instance
- Extract Connection Strings
- Create an IoT Device identity
- Create a SAS Policy
- TLS Certificate
- Pulling it all together
- Mosquitto_pub/Mosquitto_sub