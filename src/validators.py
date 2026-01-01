def validate_symbol(symbol: str):
    if not symbol.endswith("USDT"):
        raise ValueError("Only USDT-M futures symbols allowed")

def validate_quantity(qty: float):
    if qty <= 0:
        raise ValueError("Quantity must be positive")

def validate_price(price: float):
    if price <= 0:
        raise ValueError("Price must be positive")
