import streamlit as st
import pandas as pd

st.subheader("Player Recruitment Engine")

st.write("""
Takes a Top Five European Team as input and returns the number of player(s) 
the team has per tactical role.
""")



# 1. Page Configuration
st.set_page_config(page_title="Squad Gap Analysis", layout="wide")

# 2. Hardcoded League Mapping 
league_mapping = {
    # Premier League
    'Arsenal FC': 'Premier League', 'Aston Villa': 'Premier League', 'AFC Bournemouth': 'Premier League',
    'Brentford FC': 'Premier League', 'Brighton & Hove Albion': 'Premier League', 'Chelsea FC': 'Premier League',
    'Crystal Palace': 'Premier League', 'Everton FC': 'Premier League', 'Fulham FC': 'Premier League',
    'Ipswich Town': 'Premier League', 'Leicester City': 'Premier League', 'Liverpool FC': 'Premier League',
    'Manchester City': 'Premier League', 'Manchester United': 'Premier League', 'Newcastle United': 'Premier League',
    'Nottingham Forest': 'Premier League', 'Southampton FC': 'Premier League', 'Tottenham Hotspur': 'Premier League',
    'West Ham United': 'Premier League', 'Wolverhampton Wanderers': 'Premier League',

    # La Liga
    'Athletic Bilbao': 'La Liga', 'Atlético de Madrid': 'La Liga', 'CA Osasuna': 'La Liga',
    'CD Leganés': 'La Liga', 'Celta de Vigo': 'La Liga', 'Deportivo Alavés': 'La Liga',
    'FC Barcelona': 'La Liga', 'Getafe CF': 'La Liga', 'Girona FC': 'La Liga',
    'RCD Espanyol Barcelona': 'La Liga', 'RCD Mallorca': 'La Liga', 'Rayo Vallecano': 'La Liga',
    'Real Betis Balompié': 'La Liga', 'Real Madrid': 'La Liga', 'Real Sociedad': 'La Liga',
    'Real Valladolid CF': 'La Liga', 'Sevilla FC': 'La Liga', 'UD Las Palmas': 'La Liga',
    'Valencia CF': 'La Liga', 'Villarreal CF': 'La Liga',

    # Bundesliga
    '1.FC Union Berlin': 'Bundesliga', '1.FSV Mainz 05': 'Bundesliga', 'Bayer 04 Leverkusen': 'Bundesliga',
    'Bayern Munich': 'Bundesliga', 'Borussia Dortmund': 'Bundesliga', 'Borussia Mönchengladbach': 'Bundesliga',
    'Eintracht Frankfurt': 'Bundesliga', 'FC Augsburg': 'Bundesliga', 'FC St. Pauli': 'Bundesliga',
    'Holstein Kiel': 'Bundesliga', 'RB Leipzig': 'Bundesliga', 'SC Freiburg': 'Bundesliga',
    'TSG 1899 Hoffenheim': 'Bundesliga', 'VfB Stuttgart': 'Bundesliga', 'VfL Bochum': 'Bundesliga',
    'VfL Wolfsburg': 'Bundesliga', 'SV Werder Bremen': 'Bundesliga', '1.FC Heidenheim 1846': 'Bundesliga',

    # Serie A
    'AC Milan': 'Serie A', 'AC Monza': 'Serie A', 'ACF Fiorentina': 'Serie A', 'AS Roma': 'Serie A',
    'Atalanta BC': 'Serie A', 'Bologna FC 1909': 'Serie A', 'Cagliari Calcio': 'Serie A',
    'Como 1907': 'Serie A', 'FC Empoli': 'Serie A', 'Genoa CFC': 'Serie A', 'Hellas Verona': 'Serie A',
    'Inter Milan': 'Serie A', 'Juventus FC': 'Serie A', 'SS Lazio': 'Serie A', 'SSC Napoli': 'Serie A',
    'Torino FC': 'Serie A', 'Udinese Calcio': 'Serie A', 'Venezia FC': 'Serie A', 'Parma Calcio 1913': 'Serie A',
    'US Lecce': 'Serie A',

    # Ligue 1
    'AS Monaco': 'Ligue 1', 'Angers SCO': 'Ligue 1', 'AS Saint-Étienne': 'Ligue 1', 'FC Nantes': 'Ligue 1',
    'FC Toulouse': 'Ligue 1', 'Le Havre AC': 'Ligue 1', 'LOSC Lille': 'Ligue 1', 'Montpellier HSC': 'Ligue 1',
    'OGC Nice': 'Ligue 1', 'Olympique Lyon': 'Ligue 1', 'Olympique Marseille': 'Ligue 1',
    'Paris Saint-Germain': 'Ligue 1', 'RC Lens': 'Ligue 1', 'RC Strasbourg Alsace': 'Ligue 1',
    'Stade Brestois 29': 'Ligue 1', 'Stade Reims': 'Ligue 1', 'Stade Rennais FC': 'Ligue 1', 'AJ Auxerre': 'Ligue 1'
}

role_names = {
    -1: 'Hybrid Players',
     0: 'Goals Scorers / Finishers',
     1: 'Traditional Centre Backs / Blockers',
     2: 'Creators / Deep Lying Playmakers / Tempo Dictators',
     3: 'Ball Winners / Enforcers / Press Specialists',
     4: 'Wingers / Ball Carriers',
     5: 'Fullback / Wingbacks / Overlappers',
     6: 'Box-box / All rounder'
}

# 3. Data Loading Engine
@st.cache_data
def load_data():
    df = pd.read_csv("dataset_hdbscan_clusters_5.csv")
    # Apply mapping
    df['primary_league'] = df['current_club'].map(league_mapping).fillna('Other')
    # Filter out trash rows
    df = df[~df['current_club'].isin(['---', 'Disqualification', 'Without Club'])]
    # Case-insensitive helper
    df['current_club_upper'] = df['current_club'].str.upper()
    return df

dataset = load_data()

# 4. UI Header
st.title("🧩 Squad Gap Analysis Tool")
st.write("Analyze squad depth across tactical roles using 2024/25 performance data.")

# 5. Cascading Dropdowns (Stacked Vertically)
leagues = ['Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1', 'Other']
selected_league = st.selectbox("Step 1: Select a League", leagues)

filtered_teams = sorted(dataset[dataset['primary_league'] == selected_league]['current_club'].unique())
selected_team = st.selectbox("Step 2: Select a Team", filtered_teams)

# 6. The Analysis Logic
def run_analysis(team_name):
    # Filter to specific club
    team_players = dataset[dataset['current_club_upper'] == team_name.upper()].copy()
    
    # Map roles
    team_players['Tactical_Role'] = team_players['tactical_roles_hdbscan'].map(role_names)
    
    # Count players per role
    role_counts = team_players['Tactical_Role'].value_counts().reset_index()
    role_counts.columns = ['Tactical_Role', 'Player_Count']
    
    # Merge with ALL roles to identify gaps (0 counts)
    all_roles_df = pd.DataFrame({'Tactical_Role': list(role_names.values())})
    final_counts = all_roles_df.merge(role_counts, on='Tactical_Role', how='left').fillna(0)
    final_counts['Player_Count'] = final_counts['Player_Count'].astype(int)
    
    return final_counts.sort_values('Player_Count', ascending=False).reset_index(drop=True)

# 7. Display Results
if selected_team:
    results = run_analysis(selected_team)
    total = results['Player_Count'].sum()
    
    st.divider()
    st.subheader(f"📊 Squad Profile: {selected_team}")
    st.metric("Total Active Players (Stats Found)", total)
    
    # Clean up the table display
    st.table(results)

# 8. Footer Navigation
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("🏠 Back to Home"):
        st.switch_page("Home.py")
with col2:
    if st.button("🔍 Find Similar Players"):
        st.switch_page("pages/2_Similar_Players_Recruitment.py")