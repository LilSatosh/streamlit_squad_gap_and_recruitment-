
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

# 1. Page Configuration
st.set_page_config(page_title="Player Recruitment Tool", layout="wide")

# 2. Role Names Mapping
role_names = {
    0: 'Goals Scorers / Finishers',
    1: 'Traditional Centre Backs / Blockers',
    2: 'Creators / Deep Lying Playmakers / Tempo Dictators',
    3: 'Ball Winners / Enforcers / Press Specialists',
    4: 'Wingers / Ball Carriers',
    5: 'Fullback / Wingbacks / Overlappers',
    6: 'Box-box / All rounder',
    -1: 'Hybrid Players'
}

# 3. Currency Formatter
def format_currency(value):
    if value >= 1_000_000:
        return f"€{value / 1_000_000:.1f}M"
    elif value >= 1_000:
        return f"€{value / 1_000:.0f}K"
    else:
        return f"€{value}"

# 4. Feature Selection & Data Loading
features = [
    'Non_Penalty_Goals_Per_90', 'Expected_Goals_Per_90',
    'Assists_Per_90', 'Exp_Assisted_Goals_Per_90',
    'Progressive_Passes_Per_90', 'Progressive_Carries_Per_90',
    'Progressive_Passes_Received_Per_90', 'Tackles_Won_Per_90',
    'Interceptions_Per_90', 'Passes_Blocked_Per_90',
    'Clearances_Per_90', 'Shots_Blocked_Per_90',
    'Dribblers_Tackled_Per_90', 'Dribbles_Challenged_Per_90',
    'Errors_Leading_To_Shot_Per_90', 'Challenges_Lost_Per_90', 'Age'
]

@st.cache_data
def load_and_scale_data():
    df = pd.read_csv("dataset_hdbscan_clusters_5.csv")
    
    # Scale only the requested features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[features])
    
    return df, X_scaled

dataset, X_scaled = load_and_scale_data()

# 5. The Similarity Logic Function
def find_similar_players(player_name, top_n=10):
    dataset_sim = dataset.reset_index(drop=True)
    player_name_upper = player_name.upper()
    
    if player_name_upper not in dataset_sim['name_key_1'].values:
        return None, None
        
    target_idx = dataset_sim[dataset_sim['name_key_1'] == player_name_upper].index[0]
    target_cluster = dataset_sim.loc[target_idx, 'tactical_roles_hdbscan']
    target_stats = X_scaled[target_idx].reshape(1, -1)
    
    # Calculate Similarity
    similarities = cosine_similarity(target_stats, X_scaled).flatten()
    dataset_sim['Similarity_Score'] = (similarities * 100).round(2)
    
    # Filter to same role, exclude target player
    recommendations = dataset_sim[
        (dataset_sim['name_key_1'] != player_name_upper) & 
        (dataset_sim['tactical_roles_hdbscan'] == target_cluster)
    ].sort_values('Similarity_Score', ascending=False).head(top_n).copy()
    
    recommendations['Tactical_Role_1'] = recommendations['tactical_roles_hdbscan'].map(role_names)
    recommendations['Market_Value'] = recommendations['player_market_value_euro'].apply(format_currency)
    
    target_role = role_names.get(target_cluster, "Unknown")
    
    return recommendations[['Player', 'current_club', 'Age', 'Market_Value', 
                         'Similarity_Score']], target_role

# 6. UI Header
st.title("🔍 Player Recruitment Tool")
st.write("""
This is a player recommendation tool that takes a player's name as 
input and returns the ten most statistically similar players from 
the same tactical cluster or role.
""")
# 7. Search Interface
search_list = sorted(dataset['name_key_1'].unique())
target_player = st.selectbox("Search for a Player:", 
                             search_list,
                             index=None,
                             placeholder="Search a name...")

if target_player:
    results, role = find_similar_players(target_player)
    
    if results is not None:
        st.success(f"Player: **{target_player}**")
        st.markdown(f"### Most Statistically Similar Players to {target_player} based on Playing Style")
        
        st.dataframe(
            results,
            column_config={
                "Similarity_Score": st.column_config.ProgressColumn(
                    "Similarity (%)",
                    format="%.2f",
                    min_value=0,
                    max_value=100,
                ),
            },
            use_container_width=True,
            hide_index=True
        )




#Footer Navigation
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("🏠 Back to Home"):
        st.switch_page("Home.py")
with col2:
    if st.button("🧩 Squad Gap Analysis Tool"):
        st.switch_page("pages/1_Squad_Gap_Analysis.py")