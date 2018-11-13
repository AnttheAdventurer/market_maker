from git import update_Coinbase_pro, update_binance, metrics_logic


class Exchange:
    def __init__(self, name):
        self.metrics = metrics_logic.get_metric_dict(name, 'metrics_data.csv')  # must be updated with each new exchange
        # creates a list of all currency pairs and trade metrics for this exchange
        self.client = ''
        # trade client is created during the update function


def update(exch, exchange):
    if exch == "CBP":
        exchange = update_Coinbase_pro.update_exchange(exchange)
    elif exch == 'Binance':
        exchange = update_binance.update_exchange(exchange)
    else:
        pass

    return exchange
