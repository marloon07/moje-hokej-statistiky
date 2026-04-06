import streamlit as st
import pandas as pd
import requests

# Základné nastavenie
st.set_page_config(page_title="NHL Remízy", layout="wide")
st.title("🏒 NHL: Prehľad predĺžení a nájazdov")

@st.cache_data(ttl=600)
def get_simple_data():
    try:
        # Stiahneme len hlavnú tabuľku standings
        url = "https://api-web.nhle.com/v1/standings/now"
        r = requests.get(url, timeout=10)
        data = r.json()
        
        nhl_list = []
        for team in data['standings']:
            gp = team.get('gamesPlayed', 0)
            rw = team.get('regulationWins', 0) # Výhry v riadnom čase
            l_reg = team.get('losses', 0)      # Prehry v riadnom čase
            
            # REMÍZA (OT/SO) = Všetky zápasy - tie, čo skončili v riadnom čase
            all_remizy = gp - rw - l_reg
            
            nhl_list.append({
                "Tím": team['teamName']['default'],
                "Zápasy (GP)": gp,
                "Remízy (OT/SO)": all_remizy,
                "Body": team.get('points', 0)
            })
        
        return pd.DataFrame(nhl_list)
    except:
        return pd.DataFrame()

# Načítanie dát
df = get_simple_data()

if not df.empty:
    # ZORADENIE: Od najväčšieho počtu remíz
    df = df.sort_values(by="Remízy (OT/SO)", ascending=False)
    
    # Zobrazenie tabuľky
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    # Krátke info pod tabuľkou
    st.info("Tabuľka je zoradená podľa celkového počtu zápasov, ktoré dospeli do predĺženia alebo nájazdov.")
else:
    st.error("Dáta sa nepodarilo načítať. Skús obnoviť stránku.")
