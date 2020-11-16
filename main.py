from aiohttp import web
from yahoo_fin import stock_info as si
import datetime
from time import sleep
import os

end_date = datetime.datetime.now()
days = datetime.timedelta(0)
start_date = end_date - days

def handle(request):
    ticker = request.rel_url.query.get('ticker')
    data = si.get_data(f'{ticker}.SA', start_date, end_date, index_as_date=False, interval="1d")
    return web.Response(text=data.to_csv())
app = web.Application()
app.router.add_get('/', handle)

port = int(os.environ.get('PORT', 8000))
web.run_app(app, port=port)
