import streamlit as st
import pandas as pd

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
selected_league = st.selectbox(label = "Select League",
                               options = leagues,
                                index=None, 
                                placeholder="Select a league...",
                                label_visibility = "collapsed")

st.write("")  
st.write("")

filtered_teams = sorted(dataset[dataset['primary_league'] == selected_league]['current_club'].unique())
selected_team = st.selectbox(label = "Select a team",
                               options = filtered_teams,
                                index=None, 
                                placeholder="Select a team...",
                                label_visibility = "collapsed")

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
    
    # Using columns to keep the metric and a small note aligned
    col_metric, col_note = st.columns([1, 2])
    with col_metric:
        st.metric("Total Players", total)
    with col_note:
        st.caption("Note: This count only includes players with at least 450 minutes played during the 2024/25 Season.")

    # 8. High-Level Summary Table
    st.markdown("### Role Distribution Summary")
    st.table(results)

    # 9. Detailed Player Breakdown (Option 1: Expanders)
    st.write("") # Padding
    st.markdown("### 👥 Squad Members by Tactical Role")
    st.info("Click a role below to see the specific players in that role.")

    # Filter the main dataset once for the selected team to save performance
    team_data = dataset[dataset['current_club_upper'] == selected_team.upper()]

    # Iterate through the role_names dict to keep the order consistent
    for role_id, role_name in role_names.items():
        # Get list of player names for this specific cluster
        players_in_role = team_data[team_data['tactical_roles_hdbscan'] == role_id]['Player'].tolist()
        
        # Only show the expander if there are actually players in that role
        if players_in_role:
            # Sort names alphabetically for a professional look
            players_in_role.sort()
            
            with st.expander(f"{role_name} ({len(players_in_role)})"):
                # Join names with a bullet point or a clean comma
                st.write(", ".join(players_in_role))
        else:
            # Optional: Show a "ghost" expander for empty roles to highlight the "Gap"
            st.write(f"🔘 *No players identified as {role_name}*")

# 10. Footer Navigation
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("🏠 Back to Home"):
        st.switch_page("Home.py")
with col2:
    if st.button("🔍 Find Similar Players"):
        st.switch_page("pages/2_Similar_Players_Recruitment.py")
