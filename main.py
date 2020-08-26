import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind

# buys and holds every stock we have
class BuyAndHoldAll(bt.Strategy):
  def next(self):
    # buy everything
    for d in self.datas:
      buysize = int(self.broker.get_cash() / d / len(self.datas))
      if self.getposition(d).size == 0:
        self.buy(d, size=buysize)

# golden cross strategy
class GoldenCross(bt.Strategy):
  params = (
    ('longperiod', 200),
    ('shortperiod', 50)
  )

  def __init__(self):
    for d in self.datas:
      d.slowma = btind.MovingAverageSimple(d, period=self.p.longperiod)
      d.fastma = btind.MovingAverageSimple(d, period=self.p.shortperiod)

  def next(self):
    # sell
    for d in self.datas:
      if self.getposition(d).size != 0:
        if d.fastma < d.slowma:
          self.sell(d, size=self.getposition(d).size)

    # buy
    for d in self.datas:
      # don't buy twice
      if self.getposition(d).size != 0:
        continue
      
      if d.fastma > d.slowma:
        self.buy(d, size=int(self.broker.get_cash()/d))

cerebro = bt.Cerebro()
cerebro.adddata(btfeeds.YahooFinanceCSVData(
  dataname="SPY.csv"
))

#cerebro.broker.set_cash(10000) # we start with $10,000 by default!
cerebro.addstrategy(GoldenCross)
cerebro.run()

# extra optional stuff
print("% return:")
print((cerebro.broker.get_value() - 10000) / 10000)
print("CAGR:")
print(pow(cerebro.broker.get_value()/10000 ,1/25) - 1)
# these calculations can all be done with observers,
# but we won't get into that yet

# see our final plot, do everything before this!
cerebro.plot()
