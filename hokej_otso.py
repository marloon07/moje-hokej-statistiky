import streamlit as st
import pandas as pd
import requests

# Nastavenie vzhľadu
st.set_page_config(page_title="NHL Live Tracker", layout="wide")
st.title("🏒 NHL Live OT/SO Tracker")
st.markdown("Dáta sa sťahujú automaticky z oficiálneho NHL API.")

# Funkcia na získanie dát
@st.cache_data(ttl=3600)
def get_nhl_data():
    try:
        url = "https://api-web.nhle.com/v1/standings/now"
        response = requests.get(url)
        data = response.json()
        nhl_list = []
        for team in data['standings']:
            nhl_list.append({
                "Tím": team['teamName']['default'],
                "Zápasy (GP)": team['gamesPlayed'],
                "OT/SO (Prehry)": team['otLosses'],
                "Body": team['points'],
                "Divízia": team['divisionName']
            })
        return pd.DataFrame(nhl_list)
    except:
        return pd.DataFrame()

# Spustenie sťahovania
df = get_nhl_data()

if not df.empty:
    # Zoradenie podľa OT prehier
    df = df.sort_values(by="OT/SO (Prehry)", ascending=False)
    
    # Zobrazenie tabuľky
    st.subheader("Aktuálne poradie tímov")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Štatistický box
    top_team = df.iloc[0]
    st.metric("Tím s najviac OT prehrami", top_team["Tím"], f"{top_team['OT/SO (Prehry)']} zápasov")
else:
    st.error("Nepodarilo sa pripojiť k NHL serveru. Skúste neskôr.")
