import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hokej OT/SO Tracker", layout="wide")
st.title("🏒 Kompletný Hokejový OT/SO Tracker")
st.markdown("Sledujte tímy s najväčším počtom predĺžení a ich aktuálne série (Dáta k 6. 4. 2026)")

# === DATA AHL ===
ahl_data = [
    {"Tím": "Abbotsford Canucks", "GP": 68, "OT/SO": 12, "Séria bez": 4},
    {"Tím": "Bakersfield Condors", "GP": 68, "OT/SO": 10, "Séria bez": 1},
    {"Tím": "Belleville Senators", "GP": 68, "OT/SO": 15, "Séria bez": 0},
    {"Tím": "Bridgeport Islanders", "GP": 68, "OT/SO": 14, "Séria bez": 2},
    {"Tím": "Calgary Wranglers", "GP": 68, "OT/SO": 24, "Séria bez": 0},
    {"Tím": "Charlotte Checkers", "GP": 68, "OT/SO": 11, "Séria bez": 5},
    {"Tím": "Chicago Wolves", "GP": 66, "OT/SO": 22, "Séria bez": 1},
    {"Tím": "Cleveland Monsters", "GP": 67, "OT/SO": 20, "Séria bez": 3},
    {"Tím": "Coachella Valley Firebirds", "GP": 68, "OT/SO": 13, "Séria bez": 6},
    {"Tím": "Colorado Eagles", "GP": 68, "OT/SO": 9, "Séria bez": 10},
    {"Tím": "Grand Rapids Griffins", "GP": 68, "OT/SO": 16, "Séria bez": 2},
    {"Tím": "Hartford Wolf Pack", "GP": 68, "OT/SO": 18, "Séria bez": 0},
    {"Tím": "Henderson Silver Knights", "GP": 68, "OT/SO": 12, "Séria bez": 4},
    {"Tím": "Hershey Bears", "GP": 68, "OT/SO": 14, "Séria bez": 3},
    {"Tím": "Iowa Wild", "GP": 68, "OT/SO": 11, "Séria bez": 7},
    {"Tím": "Laval Rocket", "GP": 68, "OT/SO": 19, "Séria bez": 0},
    {"Tím": "Lehigh Valley Phantoms", "GP": 68, "OT/SO": 17, "Séria bez": 1},
    {"Tím": "Manitoba Moose", "GP": 68, "OT/SO": 10, "Séria bez": 8},
    {"Tím": "Milwaukee Admirals", "GP": 68, "OT/SO": 12, "Séria bez": 5},
    {"Tím": "Ontario Reign", "GP": 68, "OT/SO": 14, "Séria bez": 2},
    {"Tím": "Providence Bruins", "GP": 68, "OT/SO": 16, "Séria bez": 1},
    {"Tím": "Rochester Americans", "GP": 68, "OT/SO": 21, "Séria bez": 0},
    {"Tím": "Rockford IceHogs", "GP": 68, "OT/SO": 13, "Séria bez": 4},
    {"Tím": "San Diego Gulls", "GP": 68, "OT/SO": 15, "Séria bez": 2},
    {"Tím": "San Jose Barracuda", "GP": 66, "OT/SO": 13, "Séria bez": 19},
    {"Tím": "Springfield Thunderbirds", "GP": 68, "OT/SO": 14, "Séria bez": 3},
    {"Tím": "Syracuse Crunch", "GP": 68, "OT/SO": 18, "Séria bez": 1},
    {"Tím": "Texas Stars", "GP": 68, "OT/SO": 15, "Séria bez": 2},
    {"Tím": "Toronto Marlies", "GP": 68, "OT/SO": 20, "Séria bez": 0},
    {"Tím": "Tucson Roadrunners", "GP": 66, "OT/SO": 21, "Séria bez": 2},
    {"Tím": "Utica Comets", "GP": 68, "OT/SO": 16, "Séria bez": 1},
    {"Tím": "Wilkes-Barre/Scranton Penguins", "GP": 68, "OT/SO": 13, "Séria bez": 4},
]

# === DATA NHL ===
nhl_data = [
    {"Tím": "Anaheim Ducks", "GP": 77, "OT/SO": 12, "Séria bez": 5},
    {"Tím": "Boston Bruins", "GP": 77, "OT/SO": 18, "Séria bez": 2},
    {"Tím": "Buffalo Sabres", "GP": 77, "OT/SO": 11, "Séria bez": 4},
    {"Tím": "Calgary Flames", "GP": 77, "OT/SO": 14, "Séria bez": 3},
    {"Tím": "Carolina Hurricanes", "GP": 77, "OT/SO": 19, "Séria bez": 2},
    {"Tím": "Chicago Blackhawks", "GP": 77, "OT/SO": 8, "Séria bez": 12},
    {"Tím": "Colorado Avalanche", "GP": 77, "OT/SO": 15, "Séria bez": 1},
    {"Tím": "Columbus Blue Jackets", "GP": 77, "OT/SO": 16, "Séria bez": 0},
    {"Tím": "Dallas Stars", "GP": 77, "OT/SO": 20, "Séria bez": 1},
    {"Tím": "Detroit Red Wings", "GP": 77, "OT/SO": 17, "Séria bez": 0},
    {"Tím": "Edmonton Oilers", "GP": 77, "OT/SO": 12, "Séria bez": 6},
    {"Tím": "Florida Panthers", "GP": 77, "OT/SO": 14, "Séria bez": 3},
    {"Tím": "Los Angeles Kings", "GP": 76, "OT/SO": 31, "Séria bez": 0},
    {"Tím": "Minnesota Wild", "GP": 77, "OT/SO": 19, "Séria bez": 1},
    {"Tím": "Montreal Canadiens", "GP": 77, "OT/SO": 22, "Séria bez": 0},
    {"Tím": "Nashville Predators", "GP": 77, "OT/SO": 13, "Séria bez": 4},
    {"Tím": "New Jersey Devils", "GP": 77, "OT/SO": 15, "Séria bez": 2},
    {"Tím": "New York Islanders", "GP": 77, "OT/SO": 24, "Séria bez": 0},
    {"Tím": "New York Rangers", "GP": 77, "OT/SO": 12, "Séria bez": 5},
    {"Tím": "Ottawa Senators", "GP": 77, "OT/SO": 11, "Séria bez": 7},
    {"Tím": "Philadelphia Flyers", "GP": 77, "OT/SO": 18, "Séria bez": 1},
    {"Tím": "Pittsburgh Penguins", "GP": 77, "OT/SO": 16, "Séria bez": 2},
    {"Tím": "San Jose Sharks", "GP": 77, "OT/SO": 10, "Séria bez": 9},
    {"Tím": "Seattle Kraken", "GP": 77, "OT/SO": 21, "Séria bez": 0},
    {"Tím": "St. Louis Blues", "GP": 77, "OT/SO": 13, "Séria bez": 3},
    {"Tím": "Tampa Bay Lightning", "GP": 77, "OT/SO": 14, "Séria bez": 4},
    {"Tím": "Toronto Maple Leafs", "GP": 77, "OT/SO": 20, "Séria bez": 1},
    {"Tím": "Utah Hockey Club", "GP": 77, "OT/SO": 15, "Séria bez": 2},
    {"Tím": "Vancouver Canucks", "GP": 77, "OT/SO": 14, "Séria bez": 5},
    {"Tím": "Vegas Golden Knights", "GP": 77, "OT/SO": 16, "Séria bez": 1},
    {"Tím": "Washington Capitals", "GP": 77, "OT/SO": 18, "Séria bez": 0},
    {"Tím": "Winnipeg Jets", "GP": 77, "OT/SO": 11, "Séria bez": 6},
]

# --- Logika apky ---
liga = st.radio("Vyberte súťaž:", ["AHL", "NHL"], horizontal=True)

if liga == "AHL":
    df = pd.DataFrame(ahl_data)
else:
    df = pd.DataFrame(nhl_data)

# Zoradenie
df = df.sort_values(by="OT/SO", ascending=False)

# Opravené farbenie (používa map namiesto applymap)
def highlight_series(val):
    if isinstance(val, int) and val >= 10:
        return 'background-color: #ffcccc'
    return ''

st.subheader(f"Tabuľka {liga}")
# Používame styler len na stĺpec 'Séria bez'
st.dataframe(
    df.style.map(highlight_series, subset=['Séria bez']),
    use_container_width=True,
    hide_index=True
)

# Štatistiky
c1, c2 = st.columns(2)
with c1:
    top_ot = df.iloc[0]
    st.metric("Najviac OT/SO", f"{top_ot['Tím']}", f"{top_ot['OT/SO']}")
with c2:
    top_streak = df.loc[df["Séria bez"].idxmax()]
    st.metric("Najdlhšia séria bez OT", f"{top_streak['Tím']}", f"{top_streak['Séria bez']} záp.")

st.info("💡 Tímy so sériou 10+ zápasov bez predĺženia sú podfarbené červenou.")
