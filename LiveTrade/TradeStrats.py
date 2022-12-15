import Session as Se
import Admin as Ad


class OneEpicStrat:

    def __init__(self, session_manager, epic):
        self.session_manager = session_manager
        self.epic = epic

    # something that updates from live data
    def pull_data(self):

        return

    # something that calcs indicators
    def calc_indicators(self):
        return

    # something that reads indicators and calls trades
    def StratCore(self):
        return

    # something that trades
    def trader(self):
        return

    def turn_on(self):
        return
