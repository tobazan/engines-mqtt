FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Install cron
RUN apt-get update && apt-get install -y cron

# Add cron jobs
COPY cronjobs/crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab

CMD ["bash", "-c", "cron && python engine1.py & python engine2.py & python engine3.py"]