import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hokej OT/SO Tracker", layout="wide")
st.title("🏒 Hokejové ligy – OT/SO štatistiky")
st.markdown("Počet zápasov rozhodnutých v predĺžení/nájazdoch + aktuálna séria bez OT/SO (dáta k 6. 4. 2026)")

# === Dáta AHL (aktuálne k 6.4.2026 – môžeš aktualizovať) ===
ahl_data = [
    {"Tím": "San Jose Barracuda", "GP": 66, "RW": 30, "Reg L": 23, "OT/SO": 13, "Séria bez OT/SO": 19, "Rekord": "39-23-2-2", "Body": 82},
    {"Tím": "Calgary Wranglers", "GP": 68, "RW": 21, "Reg L": 32, "OT/SO": 24, "Séria bez OT/SO": 0, "Rekord": "21-32-10-5", "Body": 57},
    {"Tím": "Chicago Wolves", "GP": 66, "RW": 31, "Reg L": 21, "OT/SO": 22, "Séria bez OT/SO": 1, "Rekord": "31-21-8-6", "Body": 76},
    {"Tím": "Tucson Roadrunners", "GP": 66, "RW": 30, "Reg L": 27, "OT/SO": 21, "Séria bez OT/SO": 2, "Rekord": "30-27-9-0", "Body": 69},
    {"Tím": "Cleveland Monsters", "GP": 67, "RW": 35, "Reg L": 25, "OT/SO": 20, "Séria bez OT/SO": 3, "Rekord": "35-25-6-1", "Body": 77},
    {"Tím": "Laval Rocket", "GP": 68, "RW": 40, "Reg L": 21, "OT/SO": 19, "Séria bez OT/SO": 0, "Rekord": "40-21-2-5", "Body": 87},
    # Pridaj ďalšie tímy podľa potreby (z theahl.com)
]

# === Dáta NHL (príklad – doplň podľa aktuálnych standings) ===
nhl_data = [
    {"Tím": "Los Angeles Kings", "GP": 76, "RW": 19, "Reg L": 26, "OT/SO": 31, "Séria bez OT/SO": 0, "Rekord": "31-26-19", "Body": 81},
    {"Tím": "Carolina Hurricanes", "GP": 77, "RW": 36, "Reg L": 22, "OT/SO": 19, "Séria bez OT/SO": 2, "Rekord": "49-22-6", "Body": 104},
    # ... pridaj ostatné tímy
]

# Výber ligy
liga = st.selectbox("Vyber ligu", ["AHL", "NHL"])

if liga == "AHL":
    df = pd.DataFrame(ahl_data)
else:
    df = pd.DataFrame(nhl_data)

# Zoradenie podľa OT/SO zostupne
df = df.sort_values(by="OT/SO", ascending=False)

# Zobrazenie tabuľky
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "OT/SO": st.column_config.NumberColumn("OT/SO zápasy", format="%d", help="Zápasy, ktoré neboli rozhodnuté v riadnom čase"),
        "Séria bez OT/SO": st.column_config.NumberColumn("Séria bez OT/SO", help="Koľko posledných zápasov sa rozhodlo v regulácii")
    }
)

# Štatistiky
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Tím s najviac OT/SO", df.iloc[0]["Tím"], df.iloc[0]["OT/SO"])
with col2:
    st.metric("Tím s najdlhšou sériou bez OT/SO", df.loc[df["Séria bez OT/SO"].idxmax()]["Tím"], df["Séria bez OT/SO"].max())
with col3:
    st.metric("Priemerný počet OT/SO na tím", round(df["OT/SO"].mean(), 1))

st.caption("Tip: Pre aktualizáciu dát jednoducho uprav zoznamy v kóde. Pre live dáta by bolo potrebné pridať scraping z theahl.com alebo nhl.com.")

# Spustenie
st.markdown("---")
st.info("Spusti aplikáciu príkazom: `streamlit run hokej_otso.py`")
