# data_utils.py
import streamlit as st
import pandas as pd
import logging

logger = logging.getLogger(__name__)

@st.cache_data
def load_data(followup_file):
    try:
        df = pd.read_csv(followup_file)
        
        # Standardize columns
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        
        # Drop unused columns
        unused_cols = ["accumulative_absent_percent_80_percent", "current_week_absent_percent"]
        df = df.drop(columns=[col for col in unused_cols if col in df.columns])
        
        # Numeric conversions
        numeric_cols = ["no_of_semester", "balance", "no_of_follow_up", "sr_number", "week"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        
        # Date conversions
        date_cols = ["follow_up_date", "date"]
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
        
        # Fill NA selectively
        object_cols = df.select_dtypes(include=['object']).columns
        df[object_cols] = df[object_cols].fillna("N/A")
        
        logger.info("Data loaded and processed.")
        return df
    except Exception as e:
        logger.error(f"Load data error: {str(e)}")
        raise

@st.cache_data
def apply_filters(df, program_filter, status_filter, reason_filter, week_filter):
    try:
        if program_filter and "program" in df.columns:
            df = df[df["program"].isin(program_filter)]
        if status_filter != "All" and "status" in df.columns:
            df = df[df["status"] == status_filter]
        if reason_filter and "reason" in df.columns:
            df = df[df["reason"].isin(reason_filter)]
        if week_filter and "week" in df.columns:
            df = df[df["week"].isin(week_filter)]
        
        df = df.drop_duplicates()
        logger.info("Filters applied successfully.")
        return df
    except Exception as e:
        logger.error(f"Apply filters error: {str(e)}")
        raise