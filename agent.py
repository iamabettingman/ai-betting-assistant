# agent.py

import requests
from config import API_KEY, REGION, MARKET
from utils import implied_probability

class AIBettingAgent:
    def __init__(self, auto_place=False):
        self.auto_place = auto_place
        self.bet_log = []

    def fetch_odds(self, sport_key):
        url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/"
        params = {
            "apiKey": API_KEY,
            "regions": REGION,
            "markets": MARKET,
            "oddsFormat": "decimal"
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print("Error fetching odds:", response.text)
            return []
        return response.json()

    def suggest_bets(self, events, threshold=0.5):
        suggestions = []
        for event in events:
            match = f"{event['home_team']} vs {event['away_team']}"
            for bookmaker in event.get("bookmakers", []):
                for market in bookmaker.get("markets", []):
                    for outcome in market.get("outcomes", []):
                        odds = outcome["price"]
                        prob = implied_probability(odds)
                        if prob < threshold:
                            suggestions.append({
                                "match": match,
                                "bookmaker": bookmaker["title"],
                                "bet": outcome["name"],
                                "odds": odds,
                                "value": round(1 - prob, 2)
                            })
        return suggestions

    def place_bet(self, bet):
        print(f"Placing bet: {bet['bet']} on {bet['match']} at {bet['odds']} odds.")
        self.bet_log.append(bet)
