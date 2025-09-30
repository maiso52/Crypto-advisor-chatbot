# CryptoBuddy 🤖💰 (Live Data Edition)

A simple rule-based cryptocurrency advisor chatbot built in Python, now with live data from CoinGecko!

## Features
* Rule-based logic (no ML required)
* Advice on profitability (price trends, market cap) and sustainability (energy use, eco score)
* Pulls real-time price + 24h change from CoinGecko API

## Usage

### Run locally
```bash
python crypto_buddy.py
```

### Run in Google Colab / Jupyter
Paste the code into a cell, then call:
```python
respond("use live data")
respond("Which crypto is trending up?")
```

### Example
```
You: use live data
CryptoBuddy: 📡 Pulled live data from CoinGecko! Now advising based on current market trends.

You: Which crypto is trending up?
CryptoBuddy: Ethereum 🚀 is trending up! (24h change: 2.35%)
```

## Disclaimer
⚠️ This chatbot is for educational purposes only. Crypto is risky — always do your own research (DYOR).

## Assignment Submission Checklist
- [x] crypto_buddy.py (with live data support)
- [x] README.md
- [ ] Screenshot of chatbot interaction
- [ ] 50-word summary for LMS
- [ ] Optional: 30-second screen recording
