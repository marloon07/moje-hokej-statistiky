import streamlit as st
import pandas as pd
import requests

# Nastavenie stránky
st.set_page_config(page_title="NHL Live Tracker", layout="wide")
st.title("🏒 NHL Live OT/SO Tracker")
st.markdown("Sleduje všetky zápasy ukončené v predĺžení alebo nájazdoch (Výhry + Prehry).")

# Funkcia na sťahovanie dát
@st.cache_data(ttl=3600)
def get_nhl_data():
    try:
        url = "https://api-web.nhle.com/v1/standings/now"
        response = requests.get(url)
        data = response.json()
        nhl_list = []
        for team in data['standings']:
            # Výpočet: Všetky zápasy - tie čo skončili v riadnom čase
            gp = team['gamesPlayed']
            rw = team['regulationWins'] # Výhry v riadnom čase
            reg_l = team['losses']      # Prehry v riadnom čase
            all_ot_so = gp - rw - reg_l
            
            nhl_list.append({
                "Tím": team['teamName']['default'],
                "Zápasy (GP)": gp,
                "Výhry RČ": rw,
                "Prehry RČ": reg_l,
                "VŠETKY OT/SO": all_ot_so,
                "Body": team['points']
            })
        return pd.DataFrame(nhl_list)
    except:
        return pd.DataFrame()

# Spustenie
df = get_nhl_data()

if not df.empty:
    # Zoradenie podľa OT/SO
    df = df.sort_values(by="VŠETKY OT/SO", ascending=False)
    
    st.subheader("Kompletná tabuľka NHL")
    
    # Čistá tabuľka bez komplikovaného formátovania (aby neboli chyby)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    # Štatistický box pod tabuľkou
    top_team = df.iloc[0]
    st.info(f"Najviac predĺžení/nájazdov má aktuálne: **{top_team['Tím']}** (celkovo **{top_team['VŠETKY OT/SO']}** zápasov).")

else:
    st.error("Dáta sa nepodarilo načítať. Skúste obnoviť stránku neskôr.")
