import streamlit as st
import pandas as pd
import calendar

# ------------------- Page Config -------------------
st.set_page_config(
    page_title="Attendance Tracker | M S Mohan Kumar",
    layout="wide"
)

# ------------------- Header & Info -------------------
st.markdown("<h1 style='text-align: center;'>📅 Attendance Tracker App</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>✨ Made by <span style='color: teal;'>M S Mohan Kumar</span></h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>🔐 For internal use only | Track monthly WFO, WFH, and attendance percentages</p>", unsafe_allow_html=True)
st.markdown("---")

# Optional image (uncomment if you want to use your own)
# st.image("https://www.example.com/banner_image.jpg", use_column_width=True)

# ------------------- Session Init -------------------
months = list(calendar.month_name)[1:]
if 'attendance_data' not in st.session_state:
    st.session_state.attendance_data = pd.DataFrame(columns=[
        "Month", "Expected Days", "WFO Days", "WFH Days", "Total Present", "Attendance %", "WFO %"
    ])

# ------------------- Layout: Split into columns -------------------
left_col, right_col = st.columns([2, 1])

# ------------- Left Side: Attendance Input ---------------
with left_col:
    st.header("🗓️ Monthly Attendance Entry")

    selected_month = st.selectbox("📌 Select Month", months)
    expected_days = st.number_input("Total Working Days in the Month", min_value=1, max_value=31, step=1)
    wfo_days = st.number_input("Days Worked from Office", min_value=0, max_value=31, step=1)

    if st.button("💾 Save Attendance"):
        if wfo_days > expected_days:
            st.error("❌ WFO days cannot be more than expected working days.")
        else:
            wfh_days = expected_days - wfo_days
            total_present = wfo_days + wfh_days
            attendance_percent = (total_present / expected_days) * 100
            wfo_percent = (wfo_days / expected_days) * 100

            # Remove previous entry for this month
            st.session_state.attendance_data = st.session_state.attendance_data[
                st.session_state.attendance_data["Month"] != selected_month
            ]

            new_row = {
                "Month": selected_month,
                "Expected Days": expected_days,
                "WFO Days": wfo_days,
                "WFH Days": wfh_days,
                "Total Present": total_present,
                "Attendance %": round(attendance_percent, 2),
                "WFO %": round(wfo_percent, 2)
            }

            st.session_state.attendance_data = pd.concat(
                [st.session_state.attendance_data, pd.DataFrame([new_row])],
                ignore_index=True
            )

            st.success(f"✅ Attendance for {selected_month} saved successfully!")

# ------------- Right Side: Calculator ---------------
with right_col:
    st.markdown("### 🧮 WFO Attendance Calculator")
    st.markdown("Check your WFO percentage on the go! 🕵️‍♂️")

    calc_expected_days = st.number_input("📆 Total Working Days", min_value=1, step=1, key="calc1")
    calc_wfo_days = st.number_input("🏢 Worked from Office", min_value=0, step=1, key="calc2")

    if calc_expected_days > 0:
        calc_pct = (calc_wfo_days / calc_expected_days) * 100
        st.success(f"🎯 WFO Attendance: **{calc_pct:.2f}%**")

        if calc_pct < 60:
            st.error("🚨 Warning: WFO is below 60%!")
        elif calc_pct < 75:
            st.warning("⚠️ Your WFO percentage is below 75%")
    else:
        st.info("Please enter valid working days.")

# ------------------- Summary Table -------------------
st.markdown("---")
st.header("📋 Yearly Attendance Summary")

if not st.session_state.attendance_data.empty:
    df = st.session_state.attendance_data.sort_values(by="Month")
    st.dataframe(df, use_container_width=True)

    # Warnings
    for _, row in df.iterrows():
        if row["Attendance %"] < 60:
            st.error(f"❌ Critical: Attendance in **{row['Month']}** is below 60%!")
        elif row["Attendance %"] < 75:
            st.warning(f"⚠️ Low Attendance in **{row['Month']}**")

        if row["WFO %"] < 60:
            st.warning(f"🚨 WFO below 60% in **{row['Month']}**")

    # Charts
    st.subheader("📊 WFO vs WFH Distribution")
    st.bar_chart(df.set_index("Month")[["WFH Days", "WFO Days"]])

    st.subheader("📈 Attendance % Over Months")
    st.line_chart(df.set_index("Month")["Attendance %"])

else:
    st.info("👈 Use the left section to add monthly attendance records.")
