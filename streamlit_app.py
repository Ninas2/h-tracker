import streamlit as st

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
# Bookings summary component
# --------------------------------------------------
def bookings_summary(bookings):
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
