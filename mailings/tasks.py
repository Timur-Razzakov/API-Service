import datetime
import os

import pytz
import requests

from notification_service.celery import app
from .models import Message, Client, Mailing

URL = os.environ.get("TOKEN")
TOKEN = os.environ.get("URL")


@app.task(bind=True, retry_backoff=True)
def send_message(self, data, client_id, mailing_id,
                 url=URL, token=TOKEN):
    """Функция для отправки сообщений"""
    mailing = Mailing.objects.get(pk=mailing_id)
    client = Client.objects.get(pk=client_id)
    timezone = pytz.timezone(client.timezone)
    now = datetime.datetime.now(timezone)

    if mailing.mailings_started <= now.time() <= mailing.mailings_ended:
        header = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'}
        try:
            requests.post(url=url + str(data['id']), headers=header, json=data)
        except requests.exceptions.RequestException as err:
            raise self.retry(exc=err)
        else:
            Message.objects.filter(pk=data['id']).update(sending_status='True')
    else:
        # если время указанное оказалось больше, то мы ждём и запускаем снова
        time = 24 - (int(now.time().strftime('%H:%M:%S')[:2]) -
                     int(mailing.mailings_started.strftime('%H:%M:%S')[:2]))
        return self.retry(countdown=60 * time)
