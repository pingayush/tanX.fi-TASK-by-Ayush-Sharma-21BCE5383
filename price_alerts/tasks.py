# price_alerts/tasks.py

from celery import shared_task
import asyncio
import websockets
import json
from django.core.mail import send_mail
from django.conf import settings
from .models import Alert

@shared_task
def listen_price_updates():
    asyncio.run(_listen_price_updates())

async def _listen_price_updates():
    uri = "wss://stream.binance.com:9443/ws/btcusdt@trade"

    async with websockets.connect(uri) as websocket:
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            price = float(data['p'])
            check_alerts(price)

def check_alerts(price):
    alerts = Alert.objects.filter(target_price__lte=price)
    for alert in alerts:
        send_alert_email(alert.user.email, alert.crypto, alert.target_price)
        alert.delete()

def send_alert_email(user_email, crypto, target_price):
    subject = 'Price Alert Triggered'
    message = f'The price of {crypto} has reached {target_price}.'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])


from celery import shared_task
import requests
from django.core.mail import send_mail
from .models import Alert

@shared_task
def check_price_task(crypto, target_price, user_email):
    # Use the Binance WebSocket or CoinGecko API to get the current price
    response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd')
    current_price = response.json()[crypto]['usd']

    if current_price >= target_price:
        send_mail(
            'Price Alert Triggered',
            f'The price of {crypto} has reached your target price of {target_price}. Current price is {current_price}.',
            'from@example.com',
            [user_email],
            fail_silently=False,
        )
        alert = Alert.objects.filter(crypto=crypto, target_price=target_price, user__email=user_email).first()
        if alert:
            alert.status = 'triggered'
            alert.save()
