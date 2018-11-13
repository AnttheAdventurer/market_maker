"""
The trade logic data is passed through metrics.  Bracket method uses the logic to create a new buy and sell side trade.
The new trades are returned and should be sent to the exchange client for execution
"""


# headers = ['exchange','curX','curB','min','size','spread','fee','feeCur','feeType','profit']


def bracket(tradeprice, tradelogic, ticker):  # creates a buy and sell for trade called
    try:
        tradeprice = float(tradeprice)
        ticker = float(ticker)
        minimum = float(tradelogic['min'])
        ref_price = float(tradelogic['price'])
        size = float(tradelogic['size'])
        spread = float(tradelogic['spread'])
        fee = float(tradelogic['fee'])
        feeCur = tradelogic['feeCur']  # to be updated if there is a non percent style fee
        feeType = tradelogic['feeType'] # to be updated if there is a non percent style fee
        profit = float(tradelogic['profit'])  # 0 is all profit for curX, 1 = curB, any amount between splits profit
    except ValueError as e:
        print(e)
        print(e.args)
    try:
        rounding = "{:." + str(tradelogic['tick']) + 'f}'  # percent style fees

        # sell side metrics
        price = round(tradeprice * (1 + spread + fee), tradelogic['tick'])
        if price < ticker: price = round(ticker * (1 + spread / 4), tradelogic['tick'])
        quantity = round(ref_price / price * size * (1 + spread * profit), tradelogic['stepSize'])
        sell = ['sell', rounding.format(price), quantity]

        # buy side trade
        price = round(tradeprice / (1 + spread + fee), tradelogic['tick'])
        if price > ticker: price = round(ticker / (1 + spread / 4), tradelogic['tick'])
        quantity = round(ref_price / price * size, tradelogic['stepSize'])
        buy = ['buy', rounding.format(price), quantity]

        trades = []
        for t in [buy, sell]:
            if float(t[1]) < float(minimum):  # prevents trading below minimum price
                trades.append('NA')
            else:
                trades.append(t)
        return trades[0], trades[1]
    except ValueError as e:
        print('no trade data available')
    except (RuntimeError, TypeError, NameError) as e:
        # traceback.print_exc()
        print(e)
        print(e.args)
