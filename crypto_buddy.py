# crypto_buddy.py
"""
CryptoBuddy — Rule-based cryptocurrency advisor with optional live data.
Run with: python crypto_buddy.py
"""

import requests

# --- Default static dataset (fallback) ---
crypto_db = {
    "bitcoin": {
        "symbol": "btc",
        "price_trend": "rising",
        "market_cap": "high",
        "energy_use": "high",
        "sustainability_score": 3.0
    },
    "ethereum": {
        "symbol": "eth",
        "price_trend": "stable",
        "market_cap": "high",
        "energy_use": "medium",
        "sustainability_score": 6.0
    },
    "cardano": {
        "symbol": "ada",
        "price_trend": "rising",
        "market_cap": "medium",
        "energy_use": "low",
        "sustainability_score": 8.0
    }
}

BOT_NAME = "CryptoBuddy"

# --- Live data fetch ---
def fetch_live_data(coins=("bitcoin", "ethereum", "cardano")):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(coins),
        "vs_currencies": "usd",
        "include_24hr_change": "true",
        "include_market_cap": "true"
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"[Warning] Could not fetch live data: {e}")
        return None

    enriched = {}
    for coin, stats in data.items():
        enriched[coin] = {
            "price_usd": stats.get("usd"),
            "change_24h": stats.get("usd_24h_change"),
            "market_cap": stats.get("usd_market_cap")
        }
    return enriched


def respond(user_input, live_data=None):
    text = user_input.lower()
    if "hello" in text:
        return f"Hi! I'm {BOT_NAME}. Ask me about Bitcoin, Ethereum, or Cardano."
    if "sustainability" in text:
        best = max(crypto_db, key=lambda c: crypto_db[c]["sustainability_score"])
        return f"{best.title()} 🌱 is most eco-friendly with a score of {crypto_db[best]['sustainability_score']}."
    if "trending" in text and live_data:
        trending = max(live_data, key=lambda c: live_data[c]["change_24h"] or 0)
        return f"{trending.title()} 🚀 is trending up! (24h change: {live_data[trending]['change_24h']:.2f}%)"
    if "profit" in text:
        return "Ethereum ⚡ has a balance of profitability and moderate sustainability."
    if "use live data" in text:
        return "📡 Pulled live data from CoinGecko! Now advising based on current market trends."
    return "I'm not sure. Ask about profitability, sustainability, or trends."


if __name__ == "__main__":
    print(f"{BOT_NAME} active. Type 'quit' to exit.")
    live_data = None
    while True:
        user = input("You: ")
        if user.lower() == "quit":
            break
        if "use live data" in user.lower():
            live_data = fetch_live_data()
        print(f"{BOT_NAME}: {respond(user, live_data)}")
