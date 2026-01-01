import argparse
from src.client import get_client
from src.logger import setup_logger
from src.validators import validate_symbol, validate_quantity, validate_price

logger = setup_logger()
client = get_client()

def place_stop_limit_order(symbol, side, quantity, stop_price, limit_price):
    try:
        validate_symbol(symbol)
        validate_quantity(quantity)
        validate_price(stop_price)
        validate_price(limit_price)

        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP",
            quantity=quantity,
            stopPrice=stop_price,
            price=limit_price,
            timeInForce="GTC"
        )

        logger.info(f"Stop-Limit order placed: {order}")
        return order

    except Exception as e:
        logger.error(f"Stop-Limit order failed: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("symbol")
    parser.add_argument("side")
    parser.add_argument("quantity", type=float)
    parser.add_argument("stop_price", type=float)
    parser.add_argument("limit_price", type=float)

    args = parser.parse_args()
    place_stop_limit_order(
        args.symbol,
        args.side,
        args.quantity,
        args.stop_price,
        args.limit_price
    )
