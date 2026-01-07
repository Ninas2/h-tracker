import streamlit as st
from urllib.parse import urlparse, unquote
import re

st.set_page_config(page_title="Trip Planner", layout="wide")

# -----------------------------
# Initialize session state
# -----------------------------
if "bookings" not in st.session_state:
    st.session_state.bookings = []

# -----------------------------
# Inline helper logic for URL inference
# -----------------------------
def infer_property(url: str):
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
        return {"name": name, "city": city}
    except:
        return {"name": None, "city": None}

# -----------------------------
# Layout
# -----------------------------
left, right = st.columns([3,1])

# ---- Left column: Add booking ----
with left:
    st.title("✈️ Trip Planner")
    st.write("Track all your trip bookings in one place.")

    if st.button("➕ Add booking"):
        with st.form("booking_form", clear_on_submit=True):
            booking_type = st.selectbox("Booking type", ["Flight", "Housing", "Train", "Car Rental", "Activity"])
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
                    inferred = infer_property(link)
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
                    date_str = start_date.strftime("%Y-%m-%d") if start_date == end_date else f"{start_date} → {end_date}"
                    st.session_state.bookings.append({
                        "type": booking_type,
                        "title": inferred_name if booking_type == "Housing" else title,
                        "city": inferred_city if booking_type == "Housing" else "",
                        "date": date_str,
                        "details": details,
                        "link": link if booking_type == "Housing" else "",
                    })
                    st.success("Booking added!")
                    st.experimental_rerun()

# ---- Right column: Bookings summary ----
with right:
    st.markdown("### 📌 Bookings")

    if not st.session_state.bookings:
        st.caption("No bookings added yet.")
    else:
        for i, b in enumerate(st.session_state.bookings):
            city_text = f" ({b['city']})" if b.get("city") else ""

            st.markdown(f"**{b['type']}**: {b['title']}{city_text}")
            st.markdown(f"Dates: {b['date']}")

            if b.get("details"):
                st.markdown(f"Details: {b['details']}")

            if b.get("link"):
                st.markdown(f"[🔗 View listing]({b['link']})")

            # --- Remove button ---
            if st.button("🗑 Remove", key=f"remove_{i}"):
                st.session_state.bookings.pop(i)
                st.rerun()

            st.markdown("---")

