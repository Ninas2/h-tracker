import streamlit as st
from urllib.parse import urlparse, unquote
import re

st.set_page_config(page_title="Trip Planner", layout="wide")

if "bookings" not in st.session_state:
    st.session_state.bookings = []

# -----------------------------
# Helpers
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
        return {"platform": "Airbnb" if "airbnb" in host else "Booking.com", "name": name, "city": city}
    except Exception:
        return {"platform": None, "name": None, "city": None}


def bookings_summary(bookings):
    st.markdown("<h3>📌 Bookings</h3>", unsafe_allow_html=True)
    if not bookings:
        st.caption("No bookings added yet.")
        return
    for b in bookings:
        city_text = f"({b.get('city','')})" if b.get('city') else ''
        st.markdown(f"**{b['type']}**: {b['title']} {city_text}")
        st.markdown(f"Dates: {b['date']}")
        if b.get('details'):
            st.markdown(f"Details: {b['details']}")
        if b.get('link'):
            st.markdown(f"[🔗 View listing]({b['link']})")
        st.markdown("---")


# -----------------------------
# Layout
# -----------------------------
left, right = st.columns([3,1])

with left:
    st.title("✈️ Trip Planner")
    st.write("Track all your trip bookings in one place.")

    # Use a form instead of dialog
    show_form = st.button("➕ Add booking")

    if show_form:
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

            submitted = st.form_submit_button("Add Booking")
            if submitted:
                if booking_type != "Housing" and not title:
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
                            "title": inferred_name if booking_type == "Housing" else title,
                            "city": inferred_city if booking_type == "Housing" else "",
                            "date": date_str,
                            "details": details,
                            "link": link if booking_type == "Housing" else "",
                        }
                    )
                    st.success("Booking added!")
                    st.experimental_rerun()

with right:
    bookings_summary(st.session_state.bookings)
