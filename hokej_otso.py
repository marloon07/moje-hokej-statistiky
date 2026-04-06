import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="NHL Live Tracker", layout="wide")
st.title("🏒 NHL Live OT/SO Tracker")
st.markdown("Presné štatistiky založené na analýze posledných zápasov.")

@st.cache_data(ttl=3600)
def get_detailed_nhl_data():
    try:
        # 1. Načítanie tabuľky pre celkové OT/SO
        standings_url = "https://api-web.nhle.com/v1/standings/now"
        standings_data = requests.get(standings_url).json()
        
        nhl_list = []
        
        for team in standings_data['standings']:
            team_name = team['teamName']['default']
            team_abbrev = team['teamAbbrev']['default']
            gp = team['gamesPlayed']
            rw = team['regulationWins']
            reg_l = team['losses']
            all_ot_so = gp - rw - reg_l
            
            # 2. Načítanie posledných zápasov tímu pre presnú sériu
            # Tento link nám vráti všetky odohraté zápasy tímu v sezóne
            scores_url = f"https://api-web.nhle.com/v1/club-schedule-season/{team_abbrev}/now"
            scores_data = requests.get(scores_url).json()
            
            # Zoberieme len odohraté zápasy (gameType 2 je základná časť)
            played_games = [g for g in scores_data['games'] if g['gameType'] == 2 and g['gameState'] == "OFF"]
            
            # Počítame sériu od konca
            seria_bez = 0
            for game in reversed(played_games):
                # V NHL API 'periodDescriptor' hovorí, v akej tretine zápas skončil
                # 3 = riadny hrací čas, 4 = OT (predĺženie), 5 = SO (nájazdy)
                period_type = game.get('periodDescriptor', {}).get('number', 3)
                
                if period_type > 3:
                    break # Našli sme predĺženie, stop
                else:
                    seria_bez += 1
            
            nhl_list.append({
                "Tím": team_name,
                "GP": gp,
                "VŠETKY OT/SO": all_ot_so,
                "Séria bez OT": seria_bez,
                "Body": team['points']
            })
        
        return pd.DataFrame(nhl_list)
    except Exception as e:
        st.error(f"Chyba pri sťahovaní dát: {e}")
        return pd.DataFrame()

# Spustenie
with st.spinner('Analyzujem zápasy NHL...'):
    df = get_detailed_nhl_data()

if not df.empty:
    # Zoradenie podľa série (tímy, čo najdlhšie nemali OT, sú navrchu)
    df = df.sort_values(by="Séria bez OT", ascending=False)
    
    # Podfarbenie série 10+ zápasov
    def highlight_long_streak(val):
        return 'background-color: #ffcccc' if val >= 10 else ''

    st.subheader("Tabuľka s presnými sériami")
    st.dataframe(
        df.style.map(highlight_long_streak, subset=['Séria bez OT']),
        use_container_width=True,
        hide_index=True
    )
    
    st.info("💡 Stĺpec 'Séria bez OT' sa počíta analýzou každého jedného zápasu tímu. 10+ zápasov bez OT je červenou.")
else:
    st.warning("Dáta sa nepodarilo spracovať.")
