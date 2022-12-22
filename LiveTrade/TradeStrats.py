from utils import *
from FeedHandlers.stream_IG import *


class FirstStrat:
    def __init__(self, Session, Trader, Admin, epic):
        self.Session = Session
        self.Trader = Trader
        self.epic = epic
        self.Admin = Admin
        self.conn = create_connection(r"../FeedHandlers/flapDB.db")
        self.dir = None
        self.old_dir = None
        self.swing = False
        self.first = True
        print("INITIALISE STRATEGY SUCCESS")

    # something that retrieves last x data
    def pull_data(self, db=False, table=False, prev_secs=60):
        sql = """SELECT * FROM EURGBPprod WHERE dt >= ?"""
        cursor = self.conn.cursor()
        from_time = datetime.now()-timedelta(seconds=prev_secs)

        cursor.execute(sql, (from_time,))
        record = cursor.fetchall()
        df = pd.DataFrame(record, columns=['Ticker', 'dt', 'igtime', 'bid', 'ask'])
        # display(df)
        cursor.close()
        return df

    # something that calcs indicators
    def calc_indicators(self):
        self.MA_60 = self.pull_data(prev_secs=20)['bid'].mean()
        self.MA_240 = self.pull_data(prev_secs=40)['bid'].mean()
        if self.MA_240 < self.MA_60:
            self.dir = "RISING"
        elif self.MA_240 > self.MA_60:
            self.dir = "FALLING"
        if (self.dir != self.old_dir) & (self.first != True):
            swing = True
        else:
            swing = False
        self.old_dir = self.dir
        self.first = False
        return swing

    # something that actively polls indicatores and pulls trade trigger when needed
    def strat_core(self):
        while True:
            swing = self.calc_indicators()
            print(self.MA_60, self.MA_240, self.dir, "delta:", '{0:.10f}'.format(float(self.MA_60-self.MA_240)))
            if swing == True:
                if self.dir == "RISING":
                    DIR = "BUY"
                else:
                    DIR = "SELL"
                print("TRADE CALL:", DIR)
                self.Trader.create_position(15, "GBP", self.Admin.search_market("EURGBP", "CURRENCIES"), DIR, get_uuid())
            time.sleep(2)

        return


    # something that activates the strategy and calls the shots
    def turn_on(self):
        return
