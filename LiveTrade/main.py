import uuid
import Trade as Tr
import Session as Se
import Admin as Ad
from TradeStrats import OneEpicStrat

session = Se.SessionManager()
session.create_live_session()
session.what_account()
#
trade = Tr.Trade(session)
Admin = Ad.Admin(session)
EURGBP = Admin.search_market("EURGBP", "CURRENCIES").iloc[0]


trade.create_position(50, "GBP", EURGBP, "BUY", str(uuid.uuid4())[:8])

moneymaker = OneEpicStrat(session, "CS.D.EURUSD.MINI.IP")
moneymaker.turn_on()