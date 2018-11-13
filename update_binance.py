from keycodes import binance_key
from binance.client import Client
from binance.exceptions import BinanceAPIException


def client_setup():
    key, secret = binance_key()
    client = Client(key, secret)
    return client


# specific for binance metric_setup()
def find_round(num):  # counts zeros for rounding size
    count = 1
    if num[0] == '1':
        count = 0
    else:
        for c in num[2:]:
            if c == '0':
                count = count + 1
            else:
                break
    return count


def metrics_setup(self, metrics):
    new_metrics = {}
    for row in metrics:
        if metrics[row]['suspend'] != 'Y':
            cur = metrics[row]['curX'] + metrics[row]['curB']
            temp = self.client.get_symbol_info(cur)
            for i in temp['filters']:
                if 'tickSize' in i:
                    metrics[row]['tick'] = find_round(i['tickSize'])
                elif 'minNotional' in i:
                    metrics[row]['minNotional'] = float(i['minNotional'])
                elif 'stepSize' in i:
                    metrics[row]['stepSize'] = find_round(i['stepSize'])
                else:
                    pass
            new_metrics[row] = metrics[row]
    return new_metrics


def send_trade(self, cur_pair, trades):
    result = []
    try:
        for t in trades:
            if t == 'NA':
                pass

            else:

                result.append(self.client.create_order(
                    side=t[0].upper(),
                    price=t[1],
                    quantity=str(t[2]),
                    timeInForce='GTC',
                    symbol=cur_pair,
                    type='LIMIT'
                ))


    except BinanceAPIException as e:
        print('Binance Api e:', cur_pair, e)
    finally:
        return result


def get_open_trades(self, cur):
    open_orders = {'buy': [], 'sell': []}
    res = self.client.get_open_orders(symbol=cur)
    if res:
        for row in res:
            open_orders[row['side'].lower()].append([row['price'], row['orderId']])
    # returns a dict of {buy:[price, id],sell: [price,id]}
    return open_orders


def get_last_fill(self, currency='BTC-USD', limit=1):
    temp = self.client.get_my_trades(symbol=currency, limit=limit)[0]
    if temp['isBuyer']:
        side = 'Buy'
    else:
        side = "Sell"
    # print(temp['symbol'], side, temp['price'], temp['qty'], time.ctime())
    return [temp['orderId'], temp['price']]
    pass


def cancel_trade(self, cur, open_orders):
    # TODO: Add the logic to sort buys and sells, to cancel the furthest from current price
    res = []
    for side in open_orders:
        if open_orders[side]:
            res.append(self.client.cancel_order(symbol=cur, orderId=open_orders[side][0][1]))
    return res


def get_ticker(self, cur):
    ticker = self.client.get_ticker(symbol=cur)
    return ticker['lastPrice']


def update_exchange(exchange):
    exchange.client = client_setup()
    exchange.metrics = metrics_setup(exchange, exchange.metrics)
    exchange.cancel_trade = cancel_trade.__get__(exchange)
    exchange.send_trade = send_trade.__get__(exchange)
    exchange.get_last_fill = get_last_fill.__get__(exchange)
    exchange.get_open_trades = get_open_trades.__get__(exchange)
    exchange.get_ticker = get_ticker.__get__(exchange)
    return exchange
