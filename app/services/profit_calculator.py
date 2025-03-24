from datetime import timedelta

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

        return {
            "buy_date": best_pair[0].date.strftime('%Y-%m-%d') if best_pair[0] else None,
            "buy_price": best_pair[0].close if best_pair[0] else None,
            "sell_date": best_pair[1].date.strftime('%Y-%m-%d') if best_pair[1] else None,
            "sell_price": best_pair[1].close if best_pair[1] else None,
            "profit": round(max_profit, 2)
        }

    @staticmethod
    def get_total_profit(prices):
        total = 0.0
        for i in range(1, len(prices)):
            if prices[i].close > prices[i-1].close:
                total += prices[i].close - prices[i-1].close
        return round(total, 2)