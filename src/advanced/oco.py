import time
from src.client import get_client
from src.logger import setup_logger
from src.validators import validate_symbol, validate_quantity, validate_price

logger = setup_logger()
client = get_client()

def place_oco_futures(symbol, side, quantity, take_profit_price, stop_loss_price):
    try:
        validate_symbol(symbol)
        validate_quantity(quantity)
        validate_price(take_profit_price)
        validate_price(stop_loss_price)

        tp_order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            price=take_profit_price,
            quantity=quantity,
            timeInForce="GTC"
        )

        sl_order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP_MARKET",
            stopPrice=stop_loss_price,
            quantity=quantity
        )

        logger.info(f"OCO simulated: TP {tp_order['orderId']} | SL {sl_order['orderId']}")

        while True:
            tp_status = client.futures_get_order(symbol=symbol, orderId=tp_order["orderId"])
            sl_status = client.futures_get_order(symbol=symbol, orderId=sl_order["orderId"])

            if tp_status["status"] == "FILLED":
                client.futures_cancel_order(symbol=symbol, orderId=sl_order["orderId"])
                logger.info("TP hit — SL cancelled")
                break

            if sl_status["status"] == "FILLED":
                client.futures_cancel_order(symbol=symbol, orderId=tp_order["orderId"])
                logger.info("SL hit — TP cancelled")
                break

            time.sleep(5)

    except Exception as e:
        logger.error(f"OCO failed: {str(e)}")
        raise
