import argparse
import time
from src.client import get_client
from src.logger import setup_logger
from src.validators import validate_symbol, validate_quantity

logger = setup_logger()
client = get_client()

def twap_order(symbol, side, total_quantity, chunks, interval):
    try:
        validate_symbol(symbol)
        validate_quantity(total_quantity)

        chunk_qty = round(total_quantity / chunks, 6)

        logger.info(f"TWAP started: {chunks} orders, {chunk_qty} each")

        for i in range(chunks):
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=chunk_qty
            )

            logger.info(f"TWAP order {i+1}/{chunks}: {order}")
            time.sleep(interval)

        logger.info("TWAP execution completed")

    except Exception as e:
        logger.error(f"TWAP failed: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("symbol")
    parser.add_argument("side")
    parser.add_argument("total_quantity", type=float)
    parser.add_argument("chunks", type=int)
    parser.add_argument("interval", type=int)

    args = parser.parse_args()
    twap_order(
        args.symbol,
        args.side,
        args.total_quantity,
        args.chunks,
        args.interval
    )
