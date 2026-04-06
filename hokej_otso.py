import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="NHL OT/SO Tracker", layout="wide")
st.title("🏒 NHL Live: Séria bez predĺženia")
st.markdown("Počíta sa počet po sebe idúcich zápasov rozhodnutých v riadnom hracom čase.")

@st.cache_data(ttl=900)
def get_nhl_stats():
    try:
        # 1. Získame základnú tabuľku
        standings_url = "https://api-web.nhle.com/v1/standings/now"
        standings = requests.get(standings_url).json()
        
        results = []
        
        # Prejdeme tímy (obmedzíme počet požiadaviek, aby nás server nezablokoval)
        for team in standings['standings']:
            abbrev = team['teamAbbrev']['default']
            name = team['teamName']['default']
            
            # Celkové štatistiky
            gp = team.get('gamesPlayed', 0)
            rw = team.get('regulationWins', 0)
            reg_l = team.get('losses', 0)
            total_ot_so = gp - rw - reg_l
            
            # 2. Získame posledné zápasy tímu
            sched_url = f"https://api-web.nhle.com/v1/club-schedule-season/{abbrev}/now"
            sched_data = requests.get(sched_url).json()
            
            # Vyfiltrujeme len ukončené zápasy základnej časti
            played_games = [g for g in sched_data['games'] if g['gameType'] == 2 and g['gameState'] == "OFF"]
            
            # Výpočet série (ideme od konca do minulosti)
            current_streak = 0
            for game in reversed(played_games):
                # periodDescriptor.number: 3=Riadny čas, 4=OT, 5=SO
                last_period = game.get('periodDescriptor', {}).get('number', 3)
                
                if last_period == 3:
                    current_streak += 1
                else:
                    break # Narazili sme na predĺženie, séria končí
            
            results.append({
                "Tím": name,
                "GP": gp,
                "Všetky OT/SO": total_ot_so,
                "Séria bez OT": current_streak,
                "Body": team.get('points', 0)
            })
            # Krátka pauza, aby nás NHL server neoznačil za útok
            time.sleep(0.05)
            
        return pd.DataFrame(results)
    except Exception as e:
        return pd.DataFrame()

with st.spinner('Prepočítavam históriu zápasov...'):
    df = get_nhl_stats()

if not df.empty:
    # Zoradenie podľa najdlhšej série
    df = df.sort_values(by="Séria bez OT", ascending=False)
    
    # Štatistický box
    top_streak = df.iloc[0]
    st.error(f"🔥 Najdlhšia séria: **{top_streak['Tím']}** nezažil predĺženie už **{top_streak['Séria bez OT']}** zápasov!")

    # Tabuľka s podfarbením
    def highlight_streak(val):
        if val >= 10: return 'background-color: #ff4b4b; color: white'
        if val >= 7: return 'background-color: #ffcccc'
        return ''

    st.dataframe(
        df.style.map(highlight_streak, subset=['Séria bez OT']),
        use_container_width=True,
        hide_index=True
    )
    
    st.info("💡 **Séria bez OT** = počet zápasov v rade rozhodnutých v riadnom hracom čase (60 min).")
else:
    st.warning("NHL server je momentálne zaneprázdnený. Skús obnoviť stránku (Refresh) o pár sekúnd.")
