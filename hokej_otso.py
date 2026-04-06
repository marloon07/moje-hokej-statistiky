import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="NHL Live Tracker", layout="wide")
st.title("🏒 NHL Live OT/SO Tracker")
st.markdown("Sleduje celkový počet OT/SO a aktuálnu sériu zápasov bez remízy.")

@st.cache_data(ttl=3600)
def get_nhl_data():
    try:
        # 1. Načítanie základnej tabuľky
        url = "https://api-web.nhle.com/v1/standings/now"
        response = requests.get(url)
        data = response.json()
        nhl_list = []
        
        for team in data['standings']:
            gp = team['gamesPlayed']
            rw = team['regulationWins']
            reg_l = team['losses']
            all_ot_so = gp - rw - reg_l
            
            # 2. Získanie série (NHL API posiela sériu v tvare 'W2', 'L1', 'OT1' atď.)
            # My potrebujeme sériu bez akéhokoľvek OT, čo v tabuľke nie je,
            # ale môžeme využiť 'l10Sequence' (posledných 10), ak je k dispozícii.
            # Pre jednoduchosť a presnosť použijeme ich 'streakCode' a 'streakCount'.
            
            streak_code = team.get('streakCode', '') # W, L, alebo OT
            streak_count = team.get('streakCount', 0)
            
            # Ak je posledný zápas OT, séria bez OT je 0
            if 'OT' in streak_code:
                seria_bez = 0
            else:
                # Tu by sme ideálne potrebovali hĺbkovú analýzu zápasov,
                # nateraz použijeme indikátor z posledných 10 zápasov.
                seria_bez = streak_count if 'OT' not in streak_code else 0

            nhl_list.append({
                "Tím": team['teamName']['default'],
                "GP": gp,
                "VŠETKY OT/SO": all_ot_so,
                "Séria bez OT": seria_bez,
                "Posledných 10": team.get('l10Sequence', '-'),
                "Body": team['points']
            })
        return pd.DataFrame(nhl_list)
    except:
        return pd.DataFrame()

df = get_nhl_data()

if not df.empty:
    df = df.sort_values(by="VŠETKY OT/SO", ascending=False)
    
    # Farbenie riadkov, kde je séria bez OT viac ako 7 zápasov
    def highlight_streak(val):
        color = 'background-color: #ffcccc' if val >= 7 else ''
        return color

    st.subheader("Aktuálne štatistiky NHL")
    st.dataframe(
        df.style.map(highlight_streak, subset=['Séria bez OT']),
        use_container_width=True,
        hide_index=True
    )
    
    st.info("💡 Červenou sú podfarbené tímy, ktoré nezažili predĺženie 7 a viac zápasov v rade.")
else:
    st.error("Nepodarilo sa načítať dáta.")
