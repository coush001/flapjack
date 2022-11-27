import Trade as Tr
import Session as Se

session = Se.SessionManager()

trade = Tr.Trade(session)
trade.session_manager.login()
trade.session_manager.get_history()
trade.session_manager.market_nav()


