# viz_utils.py
import plotly.express as px
import streamlit as st
import logging
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

@st.cache_data
def display_kpis(df):
    if df.empty:
        return
    try:
        total = len(df)
        avg_balance = f"{df['balance'].mean():,.0f} PKR" if "balance" in df.columns else "N/A"
        total_followups = df['no_of_follow_up'].sum() if "no_of_follow_up" in df.columns else "N/A"
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Students", total)
        col2.metric("Avg Balance", avg_balance)
        col3.metric("Total Follow-ups", total_followups)
        logger.info("KPIs displayed successfully.")
    except Exception as e:
        logger.error(f"Error displaying KPIs: {str(e)}")
        st.error(f"Error displaying KPIs: {str(e)}")

@st.cache_data
def display_distribution_chart(df, column, title, chart_type="pie"):
    if df.empty or column not in df.columns:
        return
    try:
        counts = df[column].value_counts().reset_index(name="count")
        counts["percent"] = (counts["count"] / counts["count"].sum() * 100).round(1)
        counts = counts.sort_values("count", ascending=False)

        if chart_type == "pie":
            fig = px.pie(counts, values="count", names=column, title=title, color_discrete_sequence=px.colors.qualitative.Safe)
            fig.update_traces(textinfo="percent+label")
        else:
            fig = px.bar(counts, x=column, y="count", text="percent", title=title, color_discrete_sequence=px.colors.qualitative.Safe)
            fig.update_traces(texttemplate="%{text}%", textposition="outside")

        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
        logger.info(f"{title} displayed successfully.")
    except Exception as e:
        logger.error(f"Error displaying {title}: {str(e)}")
        st.error(f"Error displaying {title}: {str(e)}")

@st.cache_data
def display_financial_patterns(df):
    if df.empty or "balance" not in df.columns:
        return
    try:
        fig = px.histogram(df, x="balance", nbins=20, title="Balance Distribution", color_discrete_sequence=px.colors.qualitative.Safe)
        fig.update_layout(xaxis_title="Balance (PKR)", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)
        
        avg_by_status = df.groupby("status")["balance"].mean().reset_index() if "status" in df.columns else pd.DataFrame()
        if not avg_by_status.empty:
            fig_status = px.bar(avg_by_status, x="status", y="balance", title="Average Balance by Status")
            st.plotly_chart(fig_status, use_container_width=True)
        
        logger.info("Financial patterns displayed successfully.")
    except Exception as e:
        logger.error(f"Error displaying financial patterns: {str(e)}")
        st.error(f"Error displaying financial patterns: {str(e)}")

@st.cache_data
def display_followup_reasons(df):
    if df.empty or "reason" not in df.columns:
        return
    try:
        display_distribution_chart(df, "reason", "Reasons Distribution", chart_type="bar")
        logger.info("Follow-up reasons displayed successfully.")
    except Exception as e:
        logger.error(f"Error displaying follow-up reasons: {str(e)}")
        st.error(f"Error displaying follow-up reasons: {str(e)}")

@st.cache_data
def display_wordcloud_remarks(df):
    if df.empty or "remarks" not in df.columns:
        return
    try:
        text = " ".join(df["remarks"].dropna().astype(str))
        if text.strip():
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)
        else:
            st.info("No remarks available for word cloud.")
        logger.info("Word cloud displayed successfully.")
    except Exception as e:
        logger.error(f"Error displaying word cloud: {str(e)}")
        st.error(f"Error displaying word cloud: {str(e)}")

@st.cache_data
def display_followup_by_person(df):
    if df.empty or "follow_up_by" not in df.columns:
        return
    try:
        counts = df["follow_up_by"].value_counts().reset_index(name="count")
        fig = px.bar(counts, x="follow_up_by", y="count", title="Follow-ups by Person", color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig, use_container_width=True)
        logger.info("Follow-ups by person displayed successfully.")
    except Exception as e:
        logger.error(f"Error displaying follow-ups by person: {str(e)}")
        st.error(f"Error displaying follow-ups by person: {str(e)}")