import argparse
from src.client import get_client
from src.logger import setup_logger
from src.validators import validate_symbol, validate_quantity, validate_price

logger = setup_logger()
client = get_client()

def grid_strategy(symbol, quantity, lower_price, upper_price, grid_count):
    try:
        # Basic validations
        validate_symbol(symbol)
        validate_quantity(quantity)
        validate_price(lower_price)
        validate_price(upper_price)

        # 🔹 Market price sanity check
        ticker = client.futures_mark_price(symbol=symbol)
        current_price = float(ticker["markPrice"])

        if upper_price < current_price * 0.9 or lower_price > current_price * 1.1:
            raise ValueError(
                f"Grid range too far from market price {current_price}"
            )

        # 🔹 Minimum notional validation (Binance Futures rule)
        min_notional = 100
        if (lower_price * quantity) < min_notional:
            raise ValueError(
                f"Order notional too small: "
                f"{lower_price * quantity:.2f} < {min_notional}"
            )

        price_step = (upper_price - lower_price) / grid_count

        logger.info(
            f"Grid strategy started | Levels={grid_count} "
            f"MarketPrice={current_price:.2f} "
            f"Range=({lower_price}-{upper_price}) "
            f"Qty={quantity}"
        )

        for i in range(grid_count):
            buy_price = round(lower_price + (i * price_step), 2)
            sell_price = round(buy_price + price_step, 2)

            buy_order = client.futures_create_order(
                symbol=symbol,
                side="BUY",
                type="LIMIT",
                price=buy_price,
                quantity=quantity,
                timeInForce="GTC"
            )

            sell_order = client.futures_create_order(
                symbol=symbol,
                side="SELL",
                type="LIMIT",
                price=sell_price,
                quantity=quantity,
                timeInForce="GTC"
            )

            logger.info(
                f"Grid placed | BUY={buy_price} SELL={sell_price} "
                f"Qty={quantity}"
            )

    except Exception as e:
        logger.error(
            f"Grid strategy failed | Symbol={symbol} Error={str(e)}",
            exc_info=True
        )
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Grid trading strategy")
    parser.add_argument("symbol")
    parser.add_argument("quantity", type=float)
    parser.add_argument("lower_price", type=float)
    parser.add_argument("upper_price", type=float)
    parser.add_argument("grid_count", type=int)

    args = parser.parse_args()
    grid_strategy(
        args.symbol,
        args.quantity,
        args.lower_price,
        args.upper_price,
        args.grid_count
    )