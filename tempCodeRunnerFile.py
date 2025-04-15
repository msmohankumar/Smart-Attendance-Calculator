import streamlit as st

st.title("📅 Attendance Calculator")

# User inputs
total_days = st.number_input("Enter total number of working days:", min_value=1, step=1)
present_days = st.number_input("Enter number of days you were present:", min_value=0, step=1)

# Calculate attendance
if total_days > 0:
    attendance_percentage = (present_days / total_days) * 100
    st.success(f"✅ Your attendance percentage is: **{attendance_percentage:.2f}%**")

    # Optional: Show warning if attendance is low
    if attendance_percentage < 75:
        st.warning("⚠️ Your attendance is below 75%.")
else:
    st.error("Please enter a valid number of working days.")
