import streamlit as st
from utils import bookings_summary, add_booking_dialog

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Trip Planner",
    layout="wide",
)

# -----------------------------
# Session state
# -----------------------------
if "bookings" not in st.session_state:
    st.session_state.bookings = []

# -----------------------------
# Layout
# -----------------------------
left, right = st.columns([3, 1])

# -----------------------------
# Main content
# -----------------------------
with left:
    st.title("✈️ Trip Planner")
    st.write("Track all your trip bookings in one place.")

    # Button to open modal dialog
    if st.button("➕ Add booking"):
        add_booking_dialog()   # ✅ opens modal

# -----------------------------
# Bookings summary panel
# -----------------------------
with right:
    bookings_summary(st.session_state.bookings)
