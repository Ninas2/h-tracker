import streamlit as st

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
