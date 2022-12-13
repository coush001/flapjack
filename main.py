from IPython.core.display import display
import uuid
import Trade as Tr
import Session as Se
import Admin as Ad
from Admin import Admin

session = Se.SessionManager()
session.create_live_session()
session.what_account()

trade = Tr.Trade(session)
Admin = Ad.Admin(session)
Admin.get_positions()
# Admin.get_transactions()
tslamkt = Admin.search_market("TSLA")
display(tslamkt.to_string())


trade.create_position(150, "USD", tslamkt.to_dict("records")[0], "SELL", uuid.uuid4().hex[:8])