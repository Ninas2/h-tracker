import streamlit as st
from utils import bookings_summary, get_add_booking_dialog

st.set_page_config(page_title="Trip Planner", layout="wide")

if "bookings" not in st.session_state:
    st.session_state.bookings = []

left, right = st.columns([3,1])

with left:
    st.title("✈️ Trip Planner")
    st.write("Track all your trip bookings in one place.")

    if st.button("➕ Add booking"):
        dialog = get_add_booking_dialog()  # returns the dialog function
        dialog()  # call it inside button click

with right:
    bookings_summary(st.session_state.bookings)
