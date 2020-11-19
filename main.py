from yahoo_fin import stock_info as si
import datetime
from time import sleep
import os
import asyncio
import websockets
import datetime
import json

port = int(os.environ.get('PORT', 8000))
host = str(os.environ.get('HOST', '0.0.0.0'))

async def handle(websocket, path):
    print("New connection")
    async for message in websocket:
        data = json.loads(message)
        print(data)
        if data['action'] == "getPrices":
            days = 10
            if data['days']: 
                days = data['days']
            end_date = datetime.datetime.now()
            sub = datetime.timedelta(int(days))
            start_date = end_date - sub
            prices = si.get_data(data['ticker'] + '.SA', start_date, end_date,
                                 index_as_date=False, interval=data['interval'])
            await websocket.send(prices.to_csv())
        elif data['action'] == "realTime":
            while True:
                sleep(10)
                price = si.get_live_price(data['ticker'] + '.SA')
                await websocket.send(str(price))
        else:
            await websocket.send('FALSE')

start_server = websockets.serve(handle, host, port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
