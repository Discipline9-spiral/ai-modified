import asyncio
from deriv_api import DerivAPI

API_TOKEN = "your_api_token_here"  # Replace with your Deriv API token
MARKET = "R_100"  # Choose your market

async def get_ticks(api, symbol):
    """Subscribe to tick stream and analyze statistics"""
    ticks_stream = await api.subscribe({"ticks": symbol})
    
    tick_prices = []
    window_size = 10  # Number of ticks for analysis

    async for tick in ticks_stream:
        price = float(tick['quote'])
        tick_prices.append(price)

        # Maintain a rolling window
        if len(tick_prices) > window_size:
            tick_prices.pop(0)

        # Calculate statistics
        if len(tick_prices) > 1:
            tick_trend = "Up" if tick_prices[-1] > tick_prices[-2] else "Down"
            moving_avg = sum(tick_prices) / len(tick_prices)
            volatility = max(tick_prices) - min(tick_prices)

            print(f"Latest Tick: {price} | Trend: {tick_trend} | MA({window_size}): {moving_avg:.5f} | Volatility: {volatility:.5f}")

            # Example trading condition (modify as needed)
            if tick_trend == "Up" and price > moving_avg:
                print("Potential Buy Signal")
            elif tick_trend == "Down" and price < moving_avg:
                print("Potential Sell Signal")

async def main():
    """Main function to run the tick statistics bot"""
    api = DerivAPI(token=API_TOKEN)
    await get_ticks(api, MARKET)

# Run the bot
asyncio.run(main())
