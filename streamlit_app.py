import streamlit as st
from utils import bookings_summary, infer_property_from_url

st.set_page_config(page_title="Trip Planner", layout="wide")

if "bookings" not in st.session_state:
    st.session_state.bookings = []

left, right = st.columns([3,1])

with left:
    st.title("✈️ Trip Planner")
    st.write("Track all your trip bookings in one place.")

    # Button triggers the modal dialog
    if st.button("➕ Add booking"):

        # Dialog is defined here, inside the button click
        @st.dialog("➕ Add a booking")
        def add_booking_dialog():
            with st.form("add_booking_form", clear_on_submit=True):
                booking_type = st.selectbox(
                    "Booking type",
                    ["Flight", "Housing", "Train", "Car Rental", "Activity"]
                )

                title = st.text_input("Title")
                start_date = st.date_input("Start date")
                end_date = st.date_input("End date")
                details = st.text_input("Extra details (optional)")

                link = None
                inferred_name = None
                inferred_city = None

                if booking_type == "Housing":
                    link = st.text_input("Listing link (Airbnb / Booking.com)")
                    if link:
                        inferred = infer_property_from_url(link)
                        inferred_name = st.text_input("Property name", value=inferred.get("name") or "")
                        inferred_city = st.text_input("City", value=inferred.get("city") or "")
                    else:
                        inferred_name = st.text_input("Property name")
                        inferred_city = st.text_input("City")

                submitted = st.form_submit_button("Add booking")

                if submitted:
                    if booking_type != "Housing" and not title:
                        st.error("Title is required")
                        return

                    date_str = (
                        start_date.strftime("%Y-%m-%d")
                        if start_date == end_date
                        else f"{start_date} → {end_date}"
                    )

                    st.session_state.bookings.append(
                        {
                            "type": booking_type,
                            "title": inferred_name if booking_type == "Housing" else title,
                            "city": inferred_city if booking_type == "Housing" else "",
                            "date": date_str,
                            "details": details,
                            "link": link if booking_type == "Housing" else "",
                        }
                    )

                    st.success("Booking added!")
                    st.rerun()

        add_booking_dialog()  # call the modal here

with right:
    bookings_summary(st.session_state.bookings)
