import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="NHL OT/SO Tracker", layout="wide")
st.title("🏒 Presný NHL OT/SO Tracker")
st.markdown("Séria sa počíta z posledných odohratých zápasov (iba 3. tretiny).")

@st.cache_data(ttl=600)
def get_detailed_data():
    try:
        # 1. Získame zoznam tímov a celkové OT/SO z tabuľky
        standings_url = "https://api-web.nhle.com/v1/standings/now"
        standings_data = requests.get(standings_url).json()
        
        results = []
        for team in standings_data['standings']:
            abbrev = team['teamAbbrev']['default']
            name = team['teamName']['default']
            
            # Celkové štatistiky
            gp = team.get('gamesPlayed', 0)
            rw = team.get('regulationWins', 0)
            reg_l = team.get('losses', 0)
            all_ot_so = gp - rw - reg_l
            
            # 2. Pre každý tím stiahneme jeho posledné zápasy (Schedule)
            sched_url = f"https://api-web.nhle.com/v1/club-schedule-season/{abbrev}/now"
            sched_data = requests.get(sched_url).json()
            
            # Vyfiltrujeme len odohraté zápasy základnej časti
            finished_games = [g for g in sched_data['games'] if g['gameType'] == 2 and g['gameState'] == "OFF"]
            
            # Počítame sériu od posledného zápasu dozadu
            current_streak = 0
            for game in reversed(finished_games):
                # periodDescriptor.number: 3 = Riadny čas, 4 = OT, 5 = SO
                last_period = game.get('periodDescriptor', {}).get('number', 3)
                
                if last_period == 3:
                    current_streak += 1
                else:
                    break # Narazili sme na OT/SO, séria končí
            
            results.append({
                "Tím": name,
                "GP": gp,
                "Všetky OT/SO": all_ot_so,
                "Séria bez OT": current_streak,
                "Body": team.get('points', 0)
            })
            
        return pd.DataFrame(results)
    except Exception as e:
        st.error(f"Chyba pri analýze: {e}")
        return pd.DataFrame()

with st.spinner('Prepočítavam série z histórie zápasov...'):
    df = get_detailed_data()

if not df.empty:
    # Zoradenie podľa tvojej série
    df = df.sort_values(by="Séria bez OT", ascending=False)
    
    # Zobrazenie
    st.subheader("Tabuľka s reálnymi sériami")
    
    def highlight_alert(val):
        if val >= 10: return 'background-color: #ff4b4b; color: white'
        if val >= 7: return 'background-color: #ffcccc'
        return ''

    st.dataframe(
        df.style.map(highlight_alert, subset=['Séria bez OT']),
        use_container_width=True,
        hide_index=True
    )
    
    st.info("💡 **Séria bez OT** = počet zápasov v rade, ktoré skončili presne po 60 minútach.")
else:
    st.error("Nepodarilo sa načítať dáta.")
