import streamlit as st
from urllib.parse import urlparse, unquote
import re

# -----------------------------
# URL inference
# -----------------------------
def infer_property_from_url(url: str):
    try:
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        path = unquote(parsed.path.lower())
        name = None
        city = None

        if "airbnb" in host:
            slug = path.split("/")[-1]
            slug = re.sub(r"-?\d+$", "", slug)
            name = slug.replace("-", " ").title()

        elif "booking.com" in host:
            parts = path.split("/")
            if "hotel" in parts:
                idx = parts.index("hotel")
                if idx + 2 < len(parts):
                    city = parts[idx + 1].title()
                    slug = parts[idx + 2].split(".")[0]
                    name = slug.replace("-", " ").title()

        return {"platform": "Airbnb" if "airbnb" in host else "Booking.com",
                "name": name, "city": city}
    except Exception:
        return {"platform": None, "name": None, "city": None}


# -----------------------------
# Bookings summary
# -----------------------------
def bookings_summary(bookings):
    st.markdown(
        """
        <style>
        .bookings-box {border: 1px solid #e6e6e6; border-radius: 12px; padding: 14px; background-color: #fafafa;}
        .booking-item {margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1px dashed #ddd;}
        .booking-item:last-child {border-bottom: none; margin-bottom: 0;}
        .booking-type {font-size: 0.7rem; font-weight: 700; color: #6c757d; text-transform: uppercase;}
        .booking-title {font-size: 0.95rem; font-weight: 600;}
        .booking-date {font-size: 0.8rem; color: #555;}
        .booking-city {font-size: 0.8rem; color: #333;}
        .booking-link a {font-size: 0.8rem;}
        </style>
        """, unsafe_allow_html=True
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
                """, unsafe_allow_html=True
            )
    st.markdown("</div>", unsafe_allow_html=True)


