import streamlit as st
from urllib.parse import urlparse, unquote
import re


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
        .booking-city {
            font-size: 0.8rem;
            color: #333;
        }
        .booking-link a {
            font-size: 0.8rem;
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
                    {f"<div class='booking-city'>{b.get('city','')}</div>" if b.get('city') else ''}
                    <div class='booking-date'>{b['date']}</div>
                    <div class='booking-date'>{b.get('details', '')}</div>
                    {f"<div class='booking-link'><a href='{b.get('link')}' target='_blank'>🔗 View listing</a></div>" if b.get('link') else ''}
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# Add booking dialog (modal)
# --------------------------------------------------
@st.dialog("➕ Add a booking")
def add_booking_dialog():
    with st.form("add_booking_form", clear_on_submit=True):
        # ----- Booking type -----
        booking_type = st.selectbox(
            "Booking type",
            ["Flight", "Housing", "Train", "Car Rental", "Activity"]
        )

        # ----- Default fields -----
        title = st.text_input("Title")  # used if not Housing
        start_date = st.date_input("Start date")
        end_date = st.date_input("End date")
        details = st.text_input("Extra details (optional)")

        # ----- Housing-specific: link + inference -----
        link = None
        inferred_name = None
        inferred_city = None

        if booking_type == "Housing":
            link = st.text_input("Listing link (Airbnb / Booking.com)")

            if link:
                from utils import infer_property_from_url
                inferred = infer_property_from_url(link)

                # Pre-fill property name and city if inference worked
                inferred_name = st.text_input(
                    "Property name",
                    value=inferred.get("name") or ""
                )
                inferred_city = st.text_input(
                    "City",
                    value=inferred.get("city") or ""
                )
            else:
                inferred_name = st.text_input("Property name")
                inferred_city = st.text_input("City")

        # ----- Submit button -----
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


def infer_property_from_url(url: str):
    """
    Best-effort inference of property name and city
    from Airbnb / Booking.com URLs.
    """

    try:
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        path = unquote(parsed.path.lower())

        name = None
        city = None

        # -------------------------
        # Airbnb
        # -------------------------
        if "airbnb" in host:
            # Example:
            # /rooms/12345678
            # /rooms/loft-in-paris-centre-12345678
            slug = path.split("/")[-1]

            # Remove trailing numbers
            slug = re.sub(r"-?\d+$", "", slug)

            name = slug.replace("-", " ").title()

        # -------------------------
        # Booking.com
        # -------------------------
        elif "booking.com" in host:
            # Example:
            # /hotel/fr/hotel-name.en-gb.html
            parts = path.split("/")

            if "hotel" in parts:
                idx = parts.index("hotel")
                if idx + 2 < len(parts):
                    city = parts[idx + 1].upper()
                    slug = parts[idx + 2].split(".")[0]
                    name = slug.replace("-", " ").title()

        return {
            "platform": "Airbnb" if "airbnb" in host else "Booking.com",
            "name": name,
            "city": city,
        }

    except Exception:
        return {
            "platform": None,
            "name": None,
            "city": None,
        }
