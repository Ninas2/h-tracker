import streamlit as st
from urllib.parse import urlparse, unquote
import re

st.set_page_config(page_title="Trip Planner", layout="wide")

# -----------------------------
# Session state
# -----------------------------
if "bookings" not in st.session_state:
    st.session_state.bookings = []

if "show_form" not in st.session_state:
    st.session_state.show_form = False

# -----------------------------
# URL inference (simple)
# -----------------------------
def infer_property(url: str):
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = unquote(parsed.path.lower())

    name, city = "", ""

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
                name = parts[idx + 2].split(".")[0].replace("-", " ").title()

    return name, city

# -----------------------------
# Layout
# -----------------------------
left, right = st.columns([3, 1])

# -----------------------------
# Left column
# -----------------------------
with left:
    st.title("✈️ Trip Planner")

    if st.button("➕ Add booking"):
        st.session_state.show_form = True

    if st.session_state.show_form:
        with st.form("booking_form"):
            booking_type = st.selectbox(
                "Booking type",
                ["Flight", "Housing", "Train", "Car Rental", "Activity"]
            )

            title = st.text_input("Title")
            start_date = st.date_input("Start date")
            end_date = st.date_input("End date")
            details = st.text_input("Extra details")

            link = ""
            name = ""
            city = ""

            if booking_type == "Housing":
                link = st.text_input("Listing link (Airbnb / Booking.com)")
                if link:
                    name, city = infer_property(link)

                name = st.text_input("Property name", value=name)
                city = st.text_input("City", value=city)

            submitted = st.form_submit_button("Add")

            if submitted:
                date_str = (
                    start_date.strftime("%Y-%m-%d")
                    if start_date == end_date
                    else f"{start_date} → {end_date}"
                )

                st.session_state.bookings.append({
                    "type": booking_type,
                    "title": name if booking_type == "Housing" else title,
                    "city": city,
                    "date": date_str,
                    "details": details,
                    "link": link,
                })

                st.session_state.show_form = False
                st.rerun()

# -----------------------------
# Right column
# -----------------------------
with right:
    st.markdown("### 📌 Bookings")

    if not st.session_state.bookings:
        st.caption("No bookings yet.")
    else:
        for i, b in enumerate(st.session_state.bookings):
            city_text = f" ({b['city']})" if b["city"] else ""

            st.markdown(f"**{b['type']}**: {b['title']}{city_text}")
            st.markdown(f"Dates: {b['date']}")

            if b["details"]:
                st.markdown(f"Details: {b['details']}")

            if b["link"]:
                st.markdown(f"[🔗 Listing]({b['link']})")

            if st.button("🗑 Remove", key=f"remove_{i}"):
                st.session_state.bookings.pop(i)
                st.rerun()

            st.markdown("---")
