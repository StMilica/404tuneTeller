from app.utils.formatting import format_price_object

class ProfitCalculatorService:

    @staticmethod
    def get_best_trade(prices):
        if not prices:
            return None

        min_price = prices[0]
        max_profit = 0
        best_pair = (None, None)

        for price in prices[1:]:
            profit = price.close - min_price.close
            if profit > max_profit:
                max_profit = profit
                best_pair = (min_price, price)

            if price.close < min_price.close:
                min_price = price

        buy_date, buy_price = format_price_object(best_pair[0])
        sell_date, sell_price = format_price_object(best_pair[1])

        return {
            "buy_date": buy_date,
            "buy_price": buy_price,
            "sell_date": sell_date,
            "sell_price": sell_price,
            "profit": round(max_profit, 2)
        }

    @staticmethod
    def get_total_profit(prices):
        total = 0.0
        for i in range(1, len(prices)):
            if prices[i].close > prices[i-1].close:
                total += prices[i].close - prices[i-1].close
        return round(total, 2)