# app.py
import streamlit as st
import pandas as pd
import logging
import math
from data_utils import load_data, apply_filters
from viz_utils import display_kpis, display_distribution_chart, display_financial_patterns, display_followup_reasons, display_wordcloud_remarks, display_followup_by_person

# Setup logging
logging.basicConfig(filename='dashboard.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(page_title="Student Follow-up Dashboard", layout="wide")
st.title("📞 Student Follow-up Analysis Dashboard")

# Custom CSS
st.markdown("""
    <style>
    .stSidebar .stRadio > label { font-size: 16px; }
    .stMetric { font-size: 18px; }
    .stDataFrame { border: 1px solid #ddd; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# Theme toggle
theme = st.sidebar.radio("Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown('<style>section[data-testid="stSidebar"] {background-color: #333;} .stApp {background-color: #222; color: #fff;}</style>', unsafe_allow_html=True)

# Sidebar Upload
st.sidebar.header("📂 Upload Data File")
followup_file = st.sidebar.file_uploader("Upload Follow-up Data (.csv)", type=["csv"])

if followup_file:
    try:
        followup_df = load_data(followup_file)
        logger.info("Data loaded successfully.")
        st.success("✅ File uploaded and loaded successfully!")
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        logger.error(f"Data load error: {str(e)}")
        st.stop()
else:
    st.warning("⚠️ Please upload the CSV file.")
    st.stop()

# Sidebar Filters
st.sidebar.title("Filters")

# Searchable multiselect helper
def searchable_multiselect(label, options):
    search = st.sidebar.text_input(f"Search {label}", "")
    filtered_options = [opt for opt in options if search.lower() in str(opt).lower()]
    return st.sidebar.multiselect(label, filtered_options, default=filtered_options)

programs = sorted(followup_df["program"].dropna().unique())
statuses = followup_df["status"].dropna().unique()
reasons = sorted(followup_df["reason"].dropna().unique())
weeks = sorted(followup_df["week"].dropna().unique())

program_filter = searchable_multiselect("Select Program", programs)
status_filter = st.sidebar.radio("Status", ["All"] + list(statuses))
reason_filter = searchable_multiselect("Select Reason", reasons)
week_filter = searchable_multiselect("Select Week", weeks)

# Apply filters
try:
    filtered = apply_filters(followup_df, program_filter, status_filter, reason_filter, week_filter)
    if filtered.empty:
        st.warning("No data matches filters. Adjust to see results.")
        logger.warning("Filtered data is empty.")
    else:
        # Download
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button("Download Filtered Data", csv, "filtered_data.csv")

        # Data Table View
        with st.expander("View Filtered Data"):
            try:
                st.dataframe(
                    filtered.style.format({
                        "balance": "{:,.0f}",
                        "no_of_semester": "{:.0f}",
                        "no_of_follow_up": "{:.0f}",
                    }),
                    height=400
                )
            except Exception as e:
                st.error(f"Error rendering dataframe: {str(e)}. Try downloading the CSV for full analysis.")
                logger.error(f"Dataframe render error: {str(e)}")

        # Display content in main page
        display_kpis(filtered)
        
        st.header("Distributions")
        
        st.subheader("Reasons Distribution")
        display_distribution_chart(filtered, "reason", "Reasons Distribution")
                
        st.subheader("Follow-up Reasons Details")
        display_followup_reasons(filtered)
        
        st.subheader("Programs")
        display_distribution_chart(filtered, "program", "Programs Distribution")
        
        st.subheader("Status Distribution")
        display_distribution_chart(filtered, "status", "Statuses Distribution")
        
        st.subheader("Follow-up by Week")
        display_distribution_chart(filtered, "week", "Follow-ups by Week", chart_type="bar")
        
        st.subheader("Financial Patterns")
        display_financial_patterns(filtered)
        
        st.subheader("Remarks Analysis")
        display_wordcloud_remarks(filtered)
        
        st.subheader("Follow-ups by Person")
        display_followup_by_person(filtered)
except Exception as e:
    st.error(f"Error applying filters or rendering: {str(e)}")
    logger.error(f"Filter/render error: {str(e)}")