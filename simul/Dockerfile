FROM python:3.9-slim

WORKDIR /app

# INSTALL PY LIBRARIES + CRON
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y cron

# ADD CRONJOBS
COPY cronjobs/ /app/cronjobs/
COPY cronjobs/crontab /etc/cron.d/crontab

# SET CRONJOBS
RUN chmod +x /app/cronjobs/*.sh
RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab

# COPY ENGINE SIMULATOR FILES
COPY shared /app/shared
COPY engine*.py ./

CMD ["bash", "-c", "cron && python3 engine1.py & python3 engine2.py & python3 engine3.py"]