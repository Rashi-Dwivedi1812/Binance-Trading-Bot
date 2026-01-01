import argparse
from src.client import get_client
from src.validators import validate_symbol, validate_quantity
from src.logger import setup_logger

logger = setup_logger()
client = get_client()

def place_market_order(symbol, side, quantity):
    validate_symbol(symbol)
    validate_quantity(quantity)

    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        type="MARKET",
        quantity=quantity
    )

    logger.info(f"Market order placed: {order}")
    return order

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("symbol")
    parser.add_argument("side")
    parser.add_argument("quantity", type=float)

    args = parser.parse_args()
    place_market_order(args.symbol, args.side, args.quantity)
