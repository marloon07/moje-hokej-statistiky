from odds_map = get_live_odds() utils import get_live_odds import requests

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
            odds = odds_map.get(f"{g['home']} vs {g['away']}", 3.8)

        odds_map[f"{home} vs {away}"] = odds

    return odds_maptop5 = df[(df["prob"] > 28) & (df["value"] > 0)] \
    .sort_values("value", ascending=False) \
    .head(5)

st.subheader("🏆 TOP 5 TIPY DNES")
st.dataframe(top5)if not top5.empty:
    msg = "🏒 TOP 5 OT TIPY\n\n"

    for _, r in top5.iterrows():
        msg += f"{r['match']} | {r['prob']}% | kurz {r['odds']} | value {r['value']}\n"

    send_telegram(msg)def update_results():
    bets = pd.read_csv("bets.csv")

    for i, row in bets.iterrows():
        if pd.notna(row["result"]):
            continue

        url = f"https://api-web.nhle.com/v1/gamecenter/{row['gameId']}/boxscore"
        data = requests.get(url).json()

        if data.get("gameState") == "OFF":
            if data.get("gameOutcome", {}).get("lastPeriodType") != "REG":
                bets.at[i, "result"] = "WIN"
            else:
                bets.at[i, "result"] = "LOSS"

    bets.to_csv("bets.csv", index=False)
    return bets
