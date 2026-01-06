import streamlit as st
from utils import (
    bookings_summary,
)

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Trip Bookings Tracker",
    layout="wide",
)

# --------------------------------------------------
# Session state init
# --------------------------------------------------
if "bookings" not in st.session_state:
    st.session_state.bookings = []

# --------------------------------------------------
# Layout
# --------------------------------------------------
left, right = st.columns([3, 1])

# --------------------------------------------------
# Main content (left)
# --------------------------------------------------
with left:
    st.title("✈️ Trip Planner")

    st.write(
        "Add your trip bookings below. "
        "They will automatically appear in the summary panel on the right."
    )

    with st.form("add_booking_form", clear_on_submit=True):
        st.subheader("➕ Add a booking")

        booking_type = st.selectbox(
            "Booking type",
            ["Flight", "Hotel", "Train", "Car Rental", "Activity"]
        )

        title = st.text_input("Title (e.g. NYC → Paris, Hotel Name)")
        start_date = st.date_input("Start date")
        end_date = st.date_input("End date")
        details = st.text_input("Extra details (optional)")

        submitted = st.form_submit_button("Add booking")

        if submitted:
            if not title:
                st.error("Title is required")
            else:
                date_str = (
                    start_date.strftime("%Y-%m-%d")
                    if start_date == end_date
                    else f"{start_date} → {end_date}"
                )

                st.session_state.bookings.append(
                    {
                        "type": booking_type,
                        "title": title,
                        "date": date_str,
                        "details": details,
                    }
                )

                st.success("Booking added!")

# --------------------------------------------------
# Sidebar / right panel
# --------------------------------------------------
with right:
    bookings_summary(st.session_state.bookings)
