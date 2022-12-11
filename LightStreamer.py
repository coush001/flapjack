from dotenv import dotenv_values
import logging
from trading_ig import IGService, IGStreamService
from trading_ig.lightstreamer import Subscription

config = dotenv_values(".env")

logging.basicConfig(filename='example.log', level=logging.INFO)
logging.info('So should this')
logging.error('And non-ASCII stuff, too, like Øresund and Malmö')

def on_prices_update(item_update):
    print("price: %s " % item_update)
    logging.info("price: %s " % item_update)

def on_account_update(balance_update):
    print("balance: %s " % balance_update)
    logging.info("balance: %s " % balance_update)

def main():
    ig_service = IGService(config['IG_USERNAME'], config['IG_PASSWORD'], config['IG_API_KEY'], 'DEMO', config['CFDACC'])
    ig_stream_service = IGStreamService(ig_service)
    ig_stream_service.create_session()

    # Making a new Subscription in MERGE mode
    price_sub = Subscription(
        mode="MERGE",
        items=["L1:CS.D.GBPUSD.CFD.IP", "L1:CS.D.USDJPY.CFD.IP"],
        fields=["UPDATE_TIME", "BID", "OFFER", "CHANGE", "MARKET_STATE"],
    )

    # Adding the "on_price_update" function to Subscription
    price_sub.addlistener(on_prices_update)

    # Registering the Subscription
    sub_key_prices = ig_stream_service.ls_client.subscribe(price_sub)

    # Making an other Subscription in MERGE mode
    acc_sub = Subscription(mode="MERGE",
                           items=["ACCOUNT:" + config['CFDACC']],
                           fields=["AVAILABLE_CASH"]
                           )

    # Adding the "on_balance_update" function to Subscription
    acc_sub.addlistener(on_account_update)

    # Registering the Subscription
    sub_key_account = ig_stream_service.ls_client.subscribe(acc_sub)

    input(
        "{0:-^80}\n".format(
            "HIT CR TO UNSUBSCRIBE AND DISCONNECT FROM \
    LIGHTSTREAMER"
        )
    )

    # Disconnecting
    ig_stream_service.disconnect()


if __name__ == "__main__":
    main()