import streamlit as st
import pandas as pd
import calendar
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image

st.set_page_config(page_title="Attendance App", layout="wide")

# Title and Branding
col1, col2 = st.columns([4, 1])
with col1:
    st.title("📅 Attendance Tracker")
    st.markdown("**Made by M S Mohan Kumar**")
    st.markdown("ℹ️ _This tool is for internal use only_")
with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/942/942748.png", width=80)

# Load saved data
csv_file = "attendance_records.csv"
if "attendance_data" not in st.session_state:
    try:
        st.session_state.attendance_data = pd.read_csv(csv_file)
    except FileNotFoundError:
        st.session_state.attendance_data = pd.DataFrame(columns=[
            "Month", "Expected Days", "Work from Office Days", "Work from Home Days",
            "Total Present", "Attendance %", "Work from Office %", "Work from Home %"
        ])

# Select Month and Input
st.header("📥 Monthly Attendance Entry")
selected_month = st.selectbox("Select a Month:", list(calendar.month_name)[1:])
expected_days = st.number_input("Enter total expected working days:", min_value=1, step=1)
wfo_days = st.number_input("Enter number of Work from Office days:", min_value=0, step=1)

# Save Entry
if st.button("➕ Add Month Record"):
    if expected_days < wfo_days:
        st.error("🚫 Work from Office days cannot be greater than total expected days.")
    else:
        # Calculations
        work_from_home_days = expected_days - wfo_days
        total_present = wfo_days + work_from_home_days
        attendance_percent = (total_present / expected_days) * 100
        wfo_percent = (wfo_days / expected_days) * 100
        wfh_percent = (work_from_home_days / expected_days) * 100

        # Remove old record if month already exists
        st.session_state.attendance_data = st.session_state.attendance_data[
            st.session_state.attendance_data["Month"] != selected_month
        ]

        # Append new row
        new_row = {
            "Month": selected_month,
            "Expected Days": expected_days,
            "Work from Office Days": wfo_days,
            "Work from Home Days": work_from_home_days,
            "Total Present": total_present,
            "Attendance %": round(attendance_percent, 2),
            "Work from Office %": round(wfo_percent, 2),
            "Work from Home %": round(wfh_percent, 2)
        }
        st.session_state.attendance_data = pd.concat(
            [st.session_state.attendance_data, pd.DataFrame([new_row])],
            ignore_index=True
        )

        # Save to CSV
        st.session_state.attendance_data.to_csv(csv_file, index=False)
        st.success(f"✅ Your data for {selected_month} has been saved successfully!")

# Display Data
st.header("📊 Attendance Summary")
df = st.session_state.attendance_data
st.dataframe(df)

# Warnings
for _, row in df.iterrows():
    if row["Attendance %"] < 60:
        st.error(f"❌ Critical: Attendance in **{row['Month']}** is below 60%!")
    elif row["Attendance %"] < 75:
        st.warning(f"⚠️ Low Attendance in **{row['Month']}**")

    if row["Work from Office %"] < 60:
        st.warning(f"🚨 Warning: Your Work from Office percentage is below 60% in **{row['Month']}**.")

    if row["Work from Home %"] > 60:
        st.warning(
            f"🔔 Warning: Your Work from Home percentage is above 60% in **{row['Month']}**. "
            f"Consider balancing with Work from Office days."
        )

# Charts
st.subheader("📈 Visual Trends")
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.bar_chart(df.set_index("Month")[["Work from Home Days", "Work from Office Days"]])

with col_chart2:
    st.line_chart(df.set_index("Month")["Attendance %"])

# Optional Calculator
with st.sidebar:
    st.header("🧮 Quick Calculator")
    cal_total = st.number_input("🔢 Total Working Days", min_value=1, key="calc_total")
    cal_present = st.number_input("🎯 Days Present", min_value=0, key="calc_present")
    if cal_total > 0:
        percent = (cal_present / cal_total) * 100
        st.info(f"📌 Attendance: **{percent:.2f}%**")
