from Trade import Trader
from Session import SessionManager
from Admin import Admin
from TradeStrats import FirstStrat
from utils import *

# create session with IG
Session = SessionManager()
Session.create_live_session()
Session.what_account()

# Create Trade agent and admin agent
Trader = Trader(Session)
Admin = Admin(Session)

# Find our asset epic
EURGBP = Admin.search_market("EURGBP", "CURRENCIES")
# Trader.create_position(50, "GBP", EURGBP, "BUY", get_uuid())

# Initialise the strategy and watch it RAIN dollars
moneymaker = FirstStrat(Session, Trader, Admin, "CS.D.EURUSD.MINI.IP")
moneymaker.strat_core()


