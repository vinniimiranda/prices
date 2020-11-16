from aiohttp import web
from yahoo_fin import stock_info as si
import datetime
from time import sleep
import os


def handle(request):
    ticker = request.rel_url.query.get('ticker')
    days = request.rel_url.query.get('days') or 0
    end_date = datetime.datetime.now()
    sub = datetime.timedelta(int(days))
    start_date = end_date - sub
    data = si.get_data(f'{ticker}.SA', start_date, end_date, index_as_date=False, interval="1d")
    return web.Response(text=data.to_csv())
app = web.Application()
app.router.add_get('/', handle)

port = int(os.environ.get('PORT', 8000))
web.run_app(app, port=port)
