import streamlit as st

def bookings_summary(bookings):
    """
    Renders the bookings summary panel.
    """

    st.markdown(
        """
        <style>
        .bookings-box {
            border: 1px solid #e6e6e6;
            border-radius: 12px;
            padding: 14px;
            background-color: #fafafa;
        }
        .booking-item {
            margin-bottom: 12px;
            padding-bottom: 10px;
            border-bottom: 1px dashed #ddd;
        }
        .booking-item:last-child {
            border-bottom: none;
            margin-bottom: 0;
        }
        .booking-type {
            font-size: 0.7rem;
            font-weight: 700;
            color: #6c757d;
            text-transform: uppercase;
        }
        .booking-title {
            font-size: 0.95rem;
            font-weight: 600;
        }
        .booking-date {
            font-size: 0.8rem;
            color: #555;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='bookings-box'>", unsafe_allow_html=True)
    st.markdown("### 📌 Bookings")

    if not bookings:
        st.caption("No bookings added yet.")
    else:
        for b in bookings:
            st.markdown(
                f"""
                <div class='booking-item'>
                    <div class='booking-type'>{b['type']}</div>
                    <div class='booking-title'>{b['title']}</div>
                    <div class='booking-date'>{b['date']}</div>
                    <div class='booking-date'>{b.get('details', '')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)


def add_booking_dialog():
    """
    Modal dialog for adding a booking.
    Appends the booking to st.session_state.bookings.
    """

    @st.dialog("➕ Add a booking")
    def _dialog():
        with st.form("add_booking_form", clear_on_submit=True):
            booking_type = st.selectbox(
                "Booking type",
                ["Flight", "Hotel", "Train", "Car Rental", "Activity"]
            )

            title = st.text_input("Title")
            start_date = st.date_input("Start date")
            end_date = st.date_input("End date")
            details = st.text_input("Extra details (optional)")

            submitted = st.form_submit_button("Add booking")

            if submitted:
                if not title:
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
                        "title": title,
                        "date": date_str,
                        "details": details,
                    }
                )

                st.success("Booking added!")
                st.rerun()

    _dialog()
