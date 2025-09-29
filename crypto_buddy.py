# crypto_buddy.py
"""
Simple rule-based cryptocurrency advisor chatbot.
Run with: python crypto_buddy.py
Or paste into a Colab / Jupyter cell and run the `chat()` function.
"""

crypto_db = {
    "Bitcoin": {
        "price_trend": "rising",
        "market_cap": "high",
        "energy_use": "high",
        "sustainability_score": 3.0
    },
    "Ethereum": {
        "price_trend": "stable",
        "market_cap": "high",
        "energy_use": "medium",
        "sustainability_score": 6.0
    },
    "Cardano": {
        "price_trend": "rising",
        "market_cap": "medium",
        "energy_use": "low",
        "sustainability_score": 8.0
    }
}

BOT_NAME = "CryptoBuddy"
TONE = "friendly-professional"

# --- Decision rules ---

def recommend_most_sustainable(db):
    return max(db.keys(), key=lambda k: db[k]["sustainability_score"])

def recommend_for_profitability(db):
    candidates = [k for k, v in db.items() if v["price_trend"] == "rising"]
    if not candidates:
        candidates = [k for k, v in db.items() if v["market_cap"] == "high"]
    candidates.sort(key=lambda c: (db[c]["market_cap"] == "high", db[c]["sustainability_score"]), reverse=True)
    return candidates[0] if candidates else None

def filter_by_sustainability(db, min_score=7.0):
    return [k for k, v in db.items() if v["sustainability_score"] >= min_score and v["energy_use"] == "low"]

# --- Simple intent matching ---

IMPORT_KEYWORDS = {
    "sustainable": ["sustain", "eco", "green", "sustainable", "energy"],
    "trending_up": ["rising", "trend", "trending", "up"],
    "profit": ["profit", "buy", "investment", "growth", "long-term"],
    "compare": ["compare", "which is better", "best"]
}

def classify_query(q: str):
    q = q.lower()
    hits = {k: any(w in q for w in words) for k, words in IMPORT_KEYWORDS.items()}
    return hits

# --- Chatbot main logic ---

def respond(user_query: str, db=crypto_db):
    user_query = user_query.strip()
    if not user_query:
        return "Say something — I listen!"

    if any(x in user_query.lower() for x in ["hi", "hello", "hey"]):
        return f"Hey — I'm {BOT_NAME}! Ask me about trending coins or sustainability. Quick disclaimer: this is educational, not financial advice."

    if "disclaimer" in user_query.lower():
        return "Crypto is risky — always do your own research (DYOR). This bot is rule-based and educational."

    i = classify_query(user_query)

    if i["sustainable"]:
        candidates = filter_by_sustainability(db)
        if candidates:
            best = max(candidates, key=lambda c: db[c]["sustainability_score"])
            s = db[best]["sustainability_score"]
            return f"{best} — strong sustainability profile (score {s}/10). Good choice if energy-efficiency matters. 🌱"
        else:
            best = recommend_most_sustainable(db)
            s = db[best]["sustainability_score"]
            return f"No green coin meets strict filters, but {best} has the highest sustainability score ({s}/10)."

    if i["profit"] or i["trending_up"]:
        rec = recommend_for_profitability(db)
        if rec:
            info = db[rec]
            return (f"Consider {rec}. Trend: {info['price_trend']}, Market cap: {info['market_cap']}. "
                    f"Note sustainability score {info['sustainability_score']}/10. Always set risk controls. 🚀")
        else:
            return "I couldn't find a strong profitability candidate in the dataset."

    if i["compare"]:
        sorted_coins = sorted(db.keys(), key=lambda c: (db[c]["sustainability_score"], db[c]["price_trend"] == "rising"), reverse=True)
        lines = [f"{c}: trend={db[c]['price_trend']}, sustainability={db[c]['sustainability_score']}/10" for c in sorted_coins]
        return "\n".join(lines)

    for coin in db:
        if coin.lower() in user_query.lower():
            info = db[coin]
            return (f"{coin}: trend={info['price_trend']}, market_cap={info['market_cap']}, "
                    f"energy_use={info['energy_use']}, sustainability={info['sustainability_score']}/10")

    return "I'm not sure what you mean. Try: 'Which crypto is trending up?', 'Most sustainable coin?', or ask about a specific coin."

# --- Interactive loop for CLI ---

def chat(db=crypto_db):
    print(f"{BOT_NAME}: Hey — I can analyze a tiny crypto dataset for trend + sustainability. Type 'exit' to quit.")
    while True:
        user = input("You: ")
        if user.lower() in ("exit", "quit"):
            print(f"{BOT_NAME}: Bye — and DYOR! 👋")
            break
        print(f"{BOT_NAME}: {respond(user, db)}\n")

if __name__ == '__main__':
    chat()
