import streamlit as st

st.title("Using Machine Learning For Squad Gap and Recruitment")

st.subheader("Based on Data from the 2024/25 Football season for Top five European Leagues")

st.write("""
This research is able to identify and name seven distinct playing roles using 
Machine Learning algorithms along with football domain knowledge. These roles are: 
Goal Scorers, Blockers, Deep-Lying Playmakers, Box-to-Box, Press Specialists, Wingers, and Wingbacks.
""")

st.info("This research covers a single season (2024/25) only. Analysis across multiple seasons data would produce more stable role assignments.")

st.caption("Please note that this project is only for educational purposes only.")

st.image("streamlit_hdb_clusters.png", caption="Plot of the Tactical Role Clusters",
         width='stretch')


    
#Footer Navigation
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("🧩 Squad Gap Analysis Tool"):
        st.switch_page("pages/1_Squad_Gap_Analysis.py")
with col2:
    if st.button("🔍 Find Similar Players"):
        st.switch_page("pages/2_Similar_Players_Recruitment.py")
