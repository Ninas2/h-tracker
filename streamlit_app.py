import streamlit as st
from utils import (
    bookings_summary,
    add_booking_dialog,
)

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(page_title="Trip Planner", layout="wide")

if "bookings" not in st.session_state:
    st.session_state.bookings = []

left, right = st.columns([3, 1])

with left:
    st.title("✈️ Trip Planner")

    if st.button("➕ Add booking"):
        add_booking_dialog()

with right:
    bookings_summary(st.session_state.bookings)