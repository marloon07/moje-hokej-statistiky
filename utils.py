import requests

API_KEY = "SEM_DAJ_ODDS_API_KLUC"

def get_live_odds():
    url = f"https://api.the-odds-api.com/v4/sports/icehockey_nhl/odds/?apiKey={API_KEY}&regions=eu&markets=h2h"
    data = requests.get(url).json()

    odds_map = {}

    for g in data:
        home = g["home_team"]
        away = g["away_team"]

        try:
            outcomes = g["bookmakers"][0]["markets"][0]["outcomes"]
            odds = max(o["price"] for o in outcomes)
        except:
            odds = 3.5

        odds_map[f"{home} vs {away}"] = odds

    return odds_map
