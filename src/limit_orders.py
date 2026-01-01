import argparse
from src.client import get_client
from src.validators import validate_symbol, validate_quantity, validate_price
from src.logger import setup_logger


logger = setup_logger()
client = get_client()

def place_limit_order(symbol: str, side: str, quantity: float, price: float):
    """
    Place a LIMIT order on Binance USDT-M Futures
    """
    try:
        # Input validation
        validate_symbol(symbol)
        validate_quantity(quantity)
        validate_price(price)

        side = side.upper()
        if side not in ["BUY", "SELL"]:
            raise ValueError("Side must be BUY or SELL")

        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=price,
            timeInForce="GTC"
        )

        logger.info(
            f"LIMIT order placed | Symbol={symbol} Side={side} "
            f"Qty={quantity} Price={price} OrderID={order.get('orderId')}"
        )

        return order

    except Exception as e:
        logger.error(
            f"LIMIT order failed | Symbol={symbol} Side={side} "
            f"Qty={quantity} Price={price} Error={str(e)}",
            exc_info=True
        )
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Place a LIMIT order on Binance USDT-M Futures"
    )

    parser.add_argument("symbol", help="Trading pair (e.g. BTCUSDT)")
    parser.add_argument("side", help="BUY or SELL")
    parser.add_argument("quantity", type=float, help="Order quantity")
    parser.add_argument("price", type=float, help="Limit price")

    args = parser.parse_args()

    place_limit_order(
        symbol=args.symbol,
        side=args.side,
        quantity=args.quantity,
        price=args.price
    )
