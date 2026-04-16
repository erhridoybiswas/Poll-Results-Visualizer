import streamlit as st
import pandas as pd
from src.data_generator import generate_poll_data
from src.data_cleaner import clean_poll_data
from src.analyzer import overall_summary, cross_tab_summary
from src.visualizer import plotly_bar, plotly_pie, plotly_stacked_bar, plotly_trend

st.set_page_config(page_title="Poll Results Visualizer", layout="wide")
st.title("📊 Poll Results Visualizer")
st.markdown("Interactive dashboard for analyzing poll/survey data.")

# Sidebar - data loading
st.sidebar.header("Data Source")
data_option = st.sidebar.radio("Choose input:", ("Use synthetic data", "Upload CSV"))

df = None
if data_option == "Use synthetic data":
    n_rows = st.sidebar.slider("Number of responses", 100, 5000, 1500)
    if st.sidebar.button("Generate Data"):
        df = generate_poll_data(n=n_rows)
        st.success(f"Generated {n_rows} synthetic responses.")
else:
    uploaded_file = st.sidebar.file_uploader("Upload poll CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded.")

if df is not None:
    # Clean data
    df_clean = clean_poll_data(df)
    
    # Show raw data preview
    with st.expander("🔍 View Raw Data"):
        st.dataframe(df_clean.head(100))
    
    # Overall summary
    summary = overall_summary(df_clean)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Overall Results (Counts & %)")
        st.dataframe(summary.style.format({"Percentage": "{:.1f}%"}))
    with col2:
        st.plotly_chart(plotly_pie(summary), use_container_width=True)
    
    st.plotly_chart(plotly_bar(summary), use_container_width=True)
    
    # Demographic filters
    st.subheader("Demographic Breakdown")
    demo_col = st.selectbox("Select demographic variable:", ["Region", "AgeGroup", "Gender"])
    st.plotly_chart(plotly_stacked_bar(df_clean, demo_col), use_container_width=True)
    
    # Trend (if dates present)
    if "Date" in df_clean.columns:
        st.subheader("Response Trend Over Time")
        st.plotly_chart(plotly_trend(df_clean), use_container_width=True)
    
    # Insights
    st.subheader("📌 Key Insights")
    winner = summary.iloc[0]["Option"]
    win_pct = summary.iloc[0]["Percentage"]
    second = summary.iloc[1]["Option"]
    second_pct = summary.iloc[1]["Percentage"]
    st.markdown(f"""
    - **Leading option:** **{winner}** with **{win_pct:.1f}%** of votes.
    - Second place: {second} ({second_pct:.1f}%).
    - Total responses analyzed: {len(df_clean):,}.
    """)
    
    # Additional cross-tab insights
    region_cross = cross_tab_summary(df_clean, "Region")
    top_region = region_cross.idxmax(axis=1).value_counts().idxmax()
    st.markdown(f"- Most common top choice across regions: **{top_region}**.")
    
else:
    st.info("👈 Please generate synthetic data or upload a CSV file to begin.")