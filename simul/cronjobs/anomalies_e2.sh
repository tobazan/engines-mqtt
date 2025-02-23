#!/bin/bash
echo "$(date +%Y-%m-%d_%H:%M): Starting anomaly injection engine 02" >> /app/cronjobs/cron.log

/usr/local/bin/python3 /app/cronjobs/inject_anomalies_e2.py >> /app/cronjobs/cron.log 2>&1

echo "$(date +%Y-%m-%d_%H:%M): Finished anomaly injection engine 02" >> /app/cronjobs/cron.log   