from keycodes import coinbase_pro_key
from gdax import AuthenticatedClient


def client_setup():
    key, secret, phrase = coinbase_pro_key()
    client = AuthenticatedClient(key, secret, phrase)
    return client


def metrics_setup(metrics):  # exchange specific setup
    newMetrics = {}
    for cur in metrics:
        if metrics[cur]['suspend'] != 'Y':
            metrics[cur]['minNotional'] = 8
            metrics[cur]['stepSize'] = 8  # the rounding for quantity
            if metrics[cur]['curB'] == 'USD':  # price rounding by base currency
                metrics[cur]['tick'] = 2
            else:
                metrics[cur]['tick'] = 5
            newMetrics[cur] = metrics[cur]
    return newMetrics


def send_trade(self, cur_pair, trades):  # actual trade execution
    result = []
    for t in trades:
        if t == 'NA':
            pass
        elif t[0] == 'buy':
            result.append(self.client.buy(
                price=str(t[1]),
                size=str(t[2]),
                product_id=cur_pair,
                type='limit'
            ))
        elif t[0] == 'sell':
            result.append(self.client.sell(
                price=str(t[1]),
                size=str(t[2]),
                product_id=cur_pair,
                type='limit'
            ))
    return result


def get_open_trades(self, cur):
    open_orders = {'buy': [], 'sell': []}
    res = self.client.get_orders()
    for row in res[0]:
        if row['product_id'] == cur:
            open_orders[row['side']].append([row['price'], row['id']])

    # returns a dict of {buy:[price, id],sell: [price,id]}
    return open_orders


def get_last_fill(self, currency='BTC-USD', limit=1):
    temp = self.client.get_fills(product_id=currency, limit=limit)[0][0]
    return [temp['trade_id'], temp['price']]


def cancel_trade(self, cur, open_orders):
    # TODO: Add the logic to sort buys and sells, to cancel the furthest from current price in case bracket spans more than one buy/sell
    for side in open_orders:
        if open_orders[side]:
            self.client.cancel_order(open_orders[side][0][1])


def get_ticker(self, cur):
    ticker = self.client.get_product_ticker(cur)
    return ticker['price']


def update_exchange(exchange):
    exchange.client = client_setup()
    exchange.metrics = metrics_setup(exchange.metrics)
    exchange.cancel_trade = cancel_trade.__get__(exchange)
    exchange.send_trade = send_trade.__get__(exchange)
    exchange.get_last_fill = get_last_fill.__get__(exchange)
    exchange.get_open_trades = get_open_trades.__get__(exchange)
    exchange.get_ticker = get_ticker.__get__(exchange)
    return exchange
