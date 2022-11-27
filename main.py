import Trade as Tr
import Session as Se
import Admin as Ad


session = Se.SessionManager()
trade = Tr.Trade(session)
admin = Ad.Admin(session)


trade.session_manager.create_live_session()


admin.get_history()
admin.market_nav()

