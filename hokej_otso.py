import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="NHL OT/SO Tracker", layout="wide")
st.title("🏒 NHL Live: Presné série bez OT/SO")
st.markdown("Počíta zápasy v rade, ktoré skončili presne po 3. tretine (60 min).")

@st.cache_data(ttl=600)
def get_verified_stats():
    try:
        # 1. Základná tabuľka
        url_standings = "https://api-web.nhle.com/v1/standings/now"
        standings = requests.get(url_standings).json()
        
        results = []
        for team in standings['standings']:
            abbrev = team['teamAbbrev']['default']
            name = team['teamName']['default']
            
            # Celkové OT/SO z tabuľky
            gp = team.get('gamesPlayed', 0)
            rw = team.get('regulationWins', 0)
            l_reg = team.get('losses', 0)
            total_ot_so = gp - rw - l_reg
            
            # 2. Detailný rozpis zápasov pre tento tím
            url_sched = f"https://api-web.nhle.com/v1/club-schedule-season/{abbrev}/now"
            sched = requests.get(url_sched).json()
            
            # Len odohraté zápasy (OFF = Finished)
            played = [g for g in sched['games'] if g['gameState'] == "OFF" and g['gameType'] == 2]
            
            # Analýza série od najnovšieho zápasu
            count = 0
            for game in reversed(played):
                # periodDescriptor number: 3 = Riadny čas, 4 = OT, 5 = SO
                last_p = game.get('periodDescriptor', {}).get('number', 3)
                
                if last_p == 3:
                    count += 1
                else:
                    # Akonáhle narazíme na OT (4) alebo SO (5), séria končí
                    break
            
            results.append({
                "Tím": name,
                "GP": gp,
                "Všetky OT/SO": total_ot_so,
                "Séria bez OT": count,
                "Body": team.get('points', 0)
            })
        return pd.DataFrame(results)
    except:
        return pd.DataFrame()

with st.spinner('Počítam série...'):
    df = get_verified_stats()

if not df.empty:
    # Zoradenie podľa série
    df = df.sort_values(by="Séria bez OT", ascending=False)
    
    # Zobrazenie top tímu
    top = df.iloc[0]
    st.error(f"Aktuálne najdlhšia séria: **{top['Tím']}** ({top['Séria bez OT']} zápasov)")

    # Tabuľka
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    st.info("💡 Ak vidíš pri Detroite 10, znamená to, že ich posledných 10 zápasov malo presne 3 tretiny.")
else:
    st.error("Chyba pri sťahovaní dát.")
