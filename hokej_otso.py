import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="NHL OT/SO Tracker", layout="wide")
st.title("🏒 Profesionálny NHL OT/SO Tracker")
st.markdown("Dáta sú ťahané priamo z oficiálneho systému NHL.")

@st.cache_data(ttl=600)
def get_nhl_data():
    try:
        # Použijeme najstabilnejší endpoint
        url = "https://api-web.nhle.com/v1/standings/now"
        r = requests.get(url, timeout=10)
        data = r.json()
        
        nhl_list = []
        for team in data['standings']:
            # Výpočty
            gp = team.get('gamesPlayed', 0)
            rw = team.get('regulationWins', 0)
            l_reg = team.get('losses', 0)
            
            # Všetky OT/SO = Zápasy - Výhry v riadnom čase - Prehry v riadnom čase
            total_ot_so = gp - rw - l_reg
            
            # Séria bez OT/SO
            # Ak je streakCode 'OT', tak je séria bez OT rovná 0.
            # Inak NHL udáva dĺžku aktuálnej série výhier/prehier v riadnom čase.
            s_code = team.get('streakCode', '')
            s_count = team.get('streakCount', 0)
            seria = 0 if 'OT' in s_code else s_count

            nhl_list.append({
                "Tím": team['teamName']['default'],
                "Zápasy": gp,
                "Všetky OT/SO": total_ot_so,
                "Séria bez OT": seria,
                "Divízia": team.get('divisionName', ''),
                "Body": team.get('points', 0)
            })
        return pd.DataFrame(nhl_list)
    except Exception as e:
        st.error(f"Chyba: {e}")
        return pd.DataFrame()

df = get_nhl_data()

if not df.empty:
    # Zoradenie podľa série (najdlhšie série navrchu)
    df = df.sort_values(by="Séria bez OT", ascending=False)
    
    # Štatistické okno pre top tím
    top_streak = df.iloc[0]
    st.warning(f"⚠️ Najdlhšia séria bez OT: **{top_streak['Tím']}** ({top_streak['Séria bez OT']} zápasov)")

    # Tabuľka
    # Použijeme štýl, aby sme zvýraznili vysoké série
    def highlight_rows(row):
        if row['Séria bez OT'] >= 10:
            return ['background-color: #ffcccc'] * len(row)
        return [''] * len(row)

    st.dataframe(
        df.style.apply(highlight_rows, axis=1),
        use_container_width=True,
        hide_index=True
    )
    
    st.info("💡 Legenda: 'Všetky OT/SO' (Výhry aj Prehry v predĺžení). 'Séria bez OT' (Počet zápasov v rade ukončených v riadnom čase).")

else:
    st.error("Nepodarilo sa načítať dáta z NHL. Skúste obnoviť stránku (Refresh).")
