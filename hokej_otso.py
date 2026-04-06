import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="NHL OT/SO Tracker", layout="wide")
st.title("🏒 NHL Live: Fixný Tracker Séria")

@st.cache_data(ttl=600)
def get_final_stats():
    try:
        url_standings = "https://api-web.nhle.com/v1/standings/now"
        standings = requests.get(url_standings).json()
        
        results = []
        for team in standings['standings']:
            abbrev = team['teamAbbrev']['default']
            
            # 1. Výpočet celkových OT/SO (z oficiálnych stĺpcov tabuľky)
            gp = team.get('gamesPlayed', 0)
            rw = team.get('regulationWins', 0) # Výhry v riadnom čase
            l_reg = team.get('losses', 0)      # Prehry v riadnom čase
            total_ot_so = gp - rw - l_reg
            
            # 2. Výpočet série analýzou posledných zápasov
            url_sched = f"https://api-web.nhle.com/v1/club-schedule-season/{abbrev}/now"
            sched = requests.get(url_sched).json()
            
            # Len odohraté zápasy základnej časti
            played = [g for g in sched['games'] if g['gameState'] == "OFF" and g['gameType'] == 2]
            
            count = 0
            for game in reversed(played):
                # KLÚČOVÝ TEST: Ak sa skóre po 3. tretine (P3) nerovná konečnému skóre, bolo OT/SO
                home_final = game.get('homeTeam', {}).get('score', 0)
                away_final = game.get('awayTeam', {}).get('score', 0)
                
                # Zisťujeme stav po 60 minútach
                # Ak zápas skončil remízou po 3. tretine, periodDescriptor bude mať 'number' > 3
                is_overtime = game.get('periodDescriptor', {}).get('number', 3) > 3
                
                if not is_overtime:
                    count += 1
                else:
                    break
            
            results.append({
                "Tím": team['teamName']['default'],
                "GP": gp,
                "Všetky OT/SO": total_ot_so,
                "Séria bez OT": count,
                "Body": team.get('points', 0)
            })
        return pd.DataFrame(results)
    except:
        return pd.DataFrame()

with st.spinner('Sťahujem a overujem zápasy...'):
    df = get_final_stats()

if not df.empty:
    df = df.sort_values(by="Séria bez OT", ascending=False)
    
    # Zvýraznenie série (červená nad 9 zápasov)
    def style_streak(val):
        color = '#ff4b4b' if val >= 10 else ('#ffcccc' if val >= 7 else None)
        return f'background-color: {color}' if color else ''

    st.dataframe(
        df.style.map(style_streak, subset=['Séria bez OT']),
        use_container_width=True,
        hide_index=True
    )
    
    st.info("💡 **Séria bez OT** teraz počíta len zápasy, ktoré skončili v riadnom hracom čase (Period 3).")
else:
    st.error("Dáta momentálne nie sú dostupné.")
