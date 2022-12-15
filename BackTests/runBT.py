from backtesting.test import GOOG
from backtesting import Backtest
from Strats import SmaCross

bt = Backtest(GOOG, SmaCross, cash=10_000, commission=.002)
stats = bt.run()
print(stats)
bt.plot(plot_volume=False, plot_pl=False)