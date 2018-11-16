<h1>Market Making Algo</h1>

This is recomended for a non-levered hodler who wants to reduce risk and generate income.  If you are levered you will open yourself up to margin calls, gaming, and losses from inventory fees.

Compared to a hodl strategy this will:
Underperform in non-volatile moonshots 
Same risk of a hodl strategy if the price drops below the user defined minimum price 
Outperform during sideways market, high volitility upward trend, and bear market above minimum price.

The under/over performance during an upward trend depends on user defined metrics


Currently this is only built out for Coinbase Pro and Binance APIs.

Before getting started you will have to create API keys for your trading accounts.  Once you have created the private keys update the keycodes.py file.

This algo will automatically retrieve all of your current trades about every 3-5 seconds.  If a trade has been executed it will create 2 new trades, a buy below the current price and a sell above. All you have to do is make sure the metrics file is updated and that the process hasn't exited.  

<h4> Below are the explanations for each column of the metrics_data.csv </h4>

<b>exchange</b>:  the exchange the trades occur.  This way you can trade the same pair on multiple exchanges.

<b> CurX</b>: The exchange currency, for example if you are trading BTC-USD on Coinbase Pro the CurX is BTC.  Quantity is denominated in units of exchange currency

<b>CurB</b>: Base currency, for BTC-USD CurB is USD.  pricing is denominated in units of base currency

<b>min</b>:  This is the lowest price at which you are willing to trade.  If the price falls below this point no trades will be sent to the exchange for this currency until the price recovers.  This sets your maximum amount of risk for this trading pair.

<b>price</b>:  used for calculating the size of your trades.  More below

<b>size</b>:  used with price to calculate the size of all trades. More below

<b>spread</b>: sets the price difference between each trade.  If the spread is .01 the price of a sell order would set 1% higher than the last executed trade.

<b>fee</b>: adds into the spread so your fees are included in the profit

<b>feeCur</b>:  sets the fee to BNB if you are using Binance coin to pay fees.

<b>profit</b>: set between 0 and 1 to determine if you want to take your profits as CurX or CurB. 
    0 takes pofit as exchange currency, 1 as base currency.  You can set it anywhere between to split the profits.
    
<b>suspend</b>: set as Y to stop trading on this currency pair.  This way you can keep the metrics for trading at a later date.


The value of a trade will be determined by the price and size column

EX: price $10, size 5
if the actual trading price is 12 the algo will make the trade quantity 4.16667
 
* with a slight difference depending on your profit indicator.


<b>Thought process:</b>

If you buy 10 coin for $10 it would cost a total of $100

* P x Q = Cost (C)

Now if you sell it later at $20 you would net a profit of $100

* P1 x Q1 = Revenue (R)

R - C = profit

* 200 - 100 = 100



Now if you think its going to take a long wandering route to get to $20, you might want to make some extra cash on the volatility. So you set two trades 

*  sell: 5 coin at $15 and 5 at $20

If you hit both trades right away you will only make $75

* cost = 100
* revenue = 75 +  100

But if the price drops back down to $10 and you buy that 5 back it starts to look like this

* original cost 10 x 10 = 100

* sell 1 = 5 x 15 = 75

* buy1 = 5 x 10 = 50

* sell 2 = 5 x 15 = 75

* sell 3 = 5 x 20 = 100

* total profit = -100 + 75 - 50 + 75 + 100 = 100

each time it hits your $5 spreads you make an additional $25

For that reason you can set your maximum risk at the price floor while making money / collecting quantity from volatility.  The downside of trading like this is if the price rockets without dipping, you will miss out on a maximum of half of your potential profit.  Additionally this is a volatility reducing strategy, so the more people that use it the less volatile the currency becomes.  

The tighter you make your spreads the more trades you will have to execute to make up for lost potential profits.  Using this strategy you could stay in the market forever as long as you keep at least half your quantity whenever the price doubles. 
