from dotenv import dotenv_values
import logging
from trading_ig import IGService, IGStreamService
from trading_ig.lightstreamer import Subscription

config = dotenv_values("../LiveTrade/.env")

logging.basicConfig(filename='LSLog.log', level=logging.INFO)
logging.info('So should this')
logging.error('And non-ASCII stuff, too, like Øresund and Malmö')

def on_prices_update(item_update):
    print("price: %s " % item_update)
    print(item_update['values'])
    logging.info("price: %s " % item_update)

def on_account_update(balance_update):
    print("ACCOUNT UPDATE %s " % balance_update)
    logging.info("ACCOUNT UPDATE: %s " % balance_update)

def stream(price_on_update):
    ig_service = IGService(config['IG_USERNAME'], config['IG_PASSWORD'], config['IG_API_KEY'], 'DEMO', config['CFDACC'])
    ig_stream_service = IGStreamService(ig_service)
    ig_stream_service.create_session()

    # Making a new Subscription in MERGE mode
    price_sub = Subscription(
        mode="MERGE",
        items=["MARKET:"+"CS.D.EURUSD.MINI.IP"],
        fields=["UPDATE_TIME", "BID", "OFFER", "CHANGE", "MARKET_STATE"],
    )

    # Adding the "on_price_update" function to Subscription
    price_sub.addlistener(price_on_update)

    # Registering the Subscription
    sub_key_prices = ig_stream_service.ls_client.subscribe(price_sub)

    # Making an other Subscription in MERGE mode
    acc_sub = Subscription(mode="MERGE",
                           items=["ACCOUNT:" + config['CFDACC']],
                           fields=["PNL", "DEPOSIT", "AVAILABLE_CASH", "PNL", "PNL_LR", "PNL_NLR", "MARGIN", "AVAILABLE_TO_DEAL", "EQUITY", "EQUITY_USED"]
                           )

    # Adding the "on_balance_update" function to Subscription
    acc_sub.addlistener(on_account_update)

    # Registering the Subscription
    # sub_key_account = ig_stream_service.ls_client.subscribe(acc_sub)

    input(
        "{0:-^80}\n".format(
            "HIT CR TO UNSUBSCRIBE AND DISCONNECT FROM \
    LIGHTSTREAMER"
        )
    )

    # Disconnecting
    ig_stream_service.disconnect()


if __name__ == "__main__":
    stream(on_prices_update)