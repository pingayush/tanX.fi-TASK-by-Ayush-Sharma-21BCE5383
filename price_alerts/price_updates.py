# price_alerts/price_updates.py

import asyncio
import websockets
import json

async def listen_price_updates():
    uri = "wss://stream.binance.com:9443/ws/btcusdt@trade"
    
    async with websockets.connect(uri) as websocket:
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            print(data)  # Process the price data
