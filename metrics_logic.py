import csv


def get_data(file_name='metrics_data.csv', exch='Binance'):
    metrics = []
    with open(file_name, newline='') as csvfile:
        cur_reader = csv.DictReader(csvfile, delimiter=',')
        for row in cur_reader:
            if row['exchange'] == exch and row['min'] != "":
                metrics.append(row)
    return metrics


# exchanges write currencies differently this corrects logicDict for each exchange
def exchange_pairs(cur1, cur2, exchange):
    if exchange == 'CBP':
        return '-'.join([cur1, cur2])
    elif exchange == 'Binance':
        return cur1 + cur2


# returns a dictionary key,value = currency, logic
def get_metric_dict(exchange, file_name):
    trade_dict = {}
    metrics = get_data(exch=exchange, file_name=file_name)
    for row in metrics:
        if row['exchange'] == exchange and row['min'] != "":
            cur = exchange_pairs(row['curX'], row['curB'], exchange)
            trade_dict[cur] = row
    return trade_dict


if __name__ == '__main__':
    print('metrics_logic has three main modules: \n'
          'exchange_pairs() breaks readable pairs from data sheet into exchange specific pairs \n'
          'get_data returns() list of data from .csv\n'
          'get_metrics_dict() calls get_data and returns a dict instead of list \n'
          )
