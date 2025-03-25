def format_price_object(price):
    if not price:
        return None, None
    return price.date.strftime('%Y-%m-%d'), price.close