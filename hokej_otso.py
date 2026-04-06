import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="NHL Live Tracker", layout="wide")
st.title("🏒 NHL Live OT/SO Tracker")
st.markdown("Sleduje všetky zápasy ukončené v predĺžení alebo nájazdoch (Výhry + Prehry).")

@st.cache_data(ttl=3600)
def get_nhl_data():
    try:
        url = "https://api-web.nhle.com/v1/standings/now"
        response = requests.get(url)
        data = response.json()
        nhl_list = []
        for team in data['standings']:
            # Výpočet všetkých OT/SO:
            # Celkové zápasy (GP) - Výhry v riadnom čase (RW) - Prehry v riadnom čase (L)
            gp = team['gamesPlayed']
            rw = team['regulationWins']
            reg_l = team['losses']
            all_ot_so = gp - rw - reg_l
            
            nhl_list.append({
                "Tím": team['teamName']['default'],
                "Zápasy (GP)": gp,
                "Výhry v RČ (RW)": rw,
                "Prehry v RČ (L)": reg_l,
                "VŠETKY OT/SO": all_ot_so,
                "Body": team['points']
            })
        return pd.DataFrame(nhl_list)
    except:
        return pd.DataFrame()

df = get_nhl_data()

if not df.empty:
    # Zoradenie podľa celkového počtu OT/SO
    df = df.sort_values(by="VŠETKY OT/SO", ascending=False)
    
    st.subheader("Kompletná tabuľka NHL")
    
    # Zvýraznenie tímov s extrémne vysokým počtom OT/SO
    def highlight_max(s):
        return ['background-color: #d1e7dd' if v == s.max() else '' for v in s]

    st.dataframe(
        df.style.apply(highlight_high_ot, subset=['VŠETKY OT/SO']),
        use_container_width=True, 
        hide_index=True
    )
    
    # Štatistický box
    top_team = df.iloc[0]
    st.success(f"Tím s najväčším počtom predĺžení: **{top_team['Tím']}** (celkovo **{top_team['VŠETKY OT/SO']}** zápasov).")
else:
    st.error("Nepodarilo sa načítať dáta. Skontroluj pripojenie.")
