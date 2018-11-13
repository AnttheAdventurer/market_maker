from git.exchange import Exchange, update
from git.trade_logic import bracket
import time

exchanges = {'CBP': ''
    , 'Binance': ''
             }
file_name = 'metrics_data.csv'

for exch in exchanges:
    exchanges[exch] = Exchange(exch)
    update(exch, exchanges[exch])


def create_trade(exch, cur):
    try:
        ticker = float(exch.get_ticker(cur))
        if ticker > float(exch.metrics[cur]['min']):
            lastfill = exch.get_last_fill(currency=cur)
            new_trades = bracket(lastfill[1], exch.metrics[cur], ticker)
            sendtrade = True
            if new_trades:
                for t in new_trades:
                    if t == 'NA':
                        sendtrade = False
                    else:
                        pass
                if sendtrade == True:
                    msg = exch.send_trade(cur, new_trades)
                    exch.cancel_trade(cur, open_orders)
    except Exception as e:
        print(e, cur)


while True:
    try:
        for exch in exchanges:
            for cur in exchanges[exch].metrics:
                open_orders = exchanges[exch].get_open_trades(cur)
                for o in open_orders:
                    if len(open_orders[o]) < 1:
                        create_trade(exchanges[exch], cur)
        time.sleep(3)
    except Exception as e:
        print(
            e, '\n', e.args, cur)
