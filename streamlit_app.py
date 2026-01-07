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

if "editing_booking_index" not in st.session_state:
    st.session_state.editing_booking_index = None

if "show_housing_form" not in st.session_state:
    st.session_state.show_housing_form = False

if "editing_housing_index" not in st.session_state:
    st.session_state.editing_housing_index = False

# -----------------------------
# URL inference (simple)
# -----------------------------
def infer_property(url: str):
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = unquote(parsed.path.lower())

    name = ""

    if "airbnb" in host:
        slug = path.split("/")[-1]
        slug = re.sub(r"-?\d+$", "", slug)
        name = slug.replace("-", " ").title()

    elif "booking.com" in host:
        parts = path.split("/")
        if "hotel" in parts:
            idx = parts.index("hotel")
            if idx + 2 < len(parts):
                name = parts[idx + 2].split(".")[0].replace("-", " ").title()

    return name

# -----------------------------
# Layout
# -----------------------------
left, right = st.columns([3, 1])

# -----------------------------
# Left column
# -----------------------------
with left:
    st.title("✈️ Trip Planner")

    # Show "Add Booking" button only if not editing
    if st.session_state.editing_booking_index is None:
        if st.button("➕ Add booking"):
            st.session_state.show_form = True

    # Show form if adding or editing
    if st.session_state.show_form or st.session_state.editing_booking_index is not None:

        # Determine prefilled values
        if st.session_state.editing_booking_index is not None:
            booking = st.session_state.bookings[st.session_state.editing_booking_index]
            pre_type = booking["type"]
            pre_title = booking["title"]
            pre_start_date, pre_end_date = booking["date"].split(" → ") if "→" in booking["date"] else (booking["date"], booking["date"])
            pre_details = booking.get("details", "")
            pre_link = booking.get("link", "")
        else:
            pre_type = "Flight"
            pre_title = ""
            pre_start_date = None
            pre_end_date = None
            pre_details = ""
            pre_link = ""

        with st.form("booking_form", clear_on_submit=False):
            booking_type = st.selectbox(
                "Booking type",
                ["Flight", "Housing", "Train", "Car Rental", "Activity"],
                index=["Flight", "Housing", "Train", "Car Rental", "Activity"].index(pre_type)
            )

            title = st.text_input("Title", value=pre_title)
            start_date = st.date_input("Start date", value=pre_start_date) if pre_start_date else st.date_input("Start date")
            end_date = st.date_input("End date", value=pre_end_date) if pre_end_date else st.date_input("End date")
            details = st.text_input("Extra details", value=pre_details)

            link = ""
            name = ""

            if booking_type == "Housing":
                link = st.text_input("Listing link (Airbnb / Booking.com)", value=pre_link)
                if link:
                    inferred_name = infer_property(link)
                    name = st.text_input("Property name", value=inferred_name or pre_title)
                else:
                    name = st.text_input("Property name", value=pre_title)

            # ---------------- Save + Cancel in same row ----------------
            col_save, col_cancel = st.columns([1, 1])
            with col_save:
                submitted = st.form_submit_button("💾 Save")
            with col_cancel:
                canceled = st.form_submit_button("❌ Cancel")

            # -------- Save booking --------
            if submitted:
                date_str = (
                    start_date.strftime("%Y-%m-%d")
                    if start_date == end_date
                    else f"{start_date} → {end_date}"
                )

                new_booking = {
                    "type": booking_type,
                    "title": name if booking_type == "Housing" else title,
                    "date": date_str,
                    "details": details,
                    "link": link,
                }

                if st.session_state.editing_booking_index is not None:
                    # Update existing booking
                    st.session_state.bookings[st.session_state.editing_booking_index] = new_booking
                    st.session_state.editing_booking_index = None
                else:
                    # Add new booking
                    st.session_state.bookings.append(new_booking)

                st.session_state.show_form = False  # Close form

            # -------- Cancel booking --------
            if canceled:
                st.session_state.show_form = False
                st.session_state.editing_booking_index = None


# -----------------------------
# Right column
# -----------------------------
with right:
    st.markdown("### 📌 House Bookings")

    # Housing bookings only
    housing_bookings = [b for b in st.session_state.bookings if b["type"] == "Housing"]

    # ---------------- Add Housing Booking Button ----------------
    if st.button("➕ Add Housing Booking"):
        st.session_state.show_housing_form = True

    # Initialize flag
    if "show_housing_form" not in st.session_state:
        st.session_state.show_housing_form = False

    # ---------------- Housing Form ----------------
    if st.session_state.show_housing_form:

        # ---- Prefill if editing ----
        if st.session_state.editing_housing_index is not None:
            b = st.session_state.bookings[st.session_state.editing_housing_index]
            pre_link = b.get("link", "")
            pre_title = b.get("title", "")
            pre_details = b.get("details", "")
            pre_price = b.get("price", "")
            if "→" in b["date"]:
                pre_start, pre_end = b["date"].split(" → ")
            else:
                pre_start = pre_end = b["date"]
        else:
            pre_link = pre_title = pre_details = pre_price = ""
            pre_start = pre_end = None

        with st.form("housing_form", clear_on_submit=False):

            link = st.text_input("Listing link (Airbnb / Booking.com)", value=pre_link)

            if link:
                inferred_name = infer_property(link)
                title = st.text_input("Property name", value=inferred_name or pre_title)
            else:
                title = st.text_input("Property name", value=pre_title)

            start_date = st.date_input("Start date", value=pre_start) if pre_start else st.date_input("Start date")
            end_date = st.date_input("End date", value=pre_end) if pre_end else st.date_input("End date")

            price = st.text_input("Price (EUR)", value=pre_price)
            details = st.text_input("Extra details (optional)", value=pre_details)

            col_save, col_cancel = st.columns(2)
            with col_save:
                submitted = st.form_submit_button("💾 Save")
            with col_cancel:
                canceled = st.form_submit_button("❌ Cancel")

            if submitted:
                date_str = (
                    start_date.strftime("%Y-%m-%d")
                    if start_date == end_date
                    else f"{start_date} → {end_date}"
                )

                booking_data = {
                    "type": "Housing",
                    "title": title,
                    "date": date_str,
                    "details": details,
                    "link": link,
                    "price": price,
                }

                if st.session_state.editing_housing_index is not None:
                    # Update existing
                    st.session_state.bookings[st.session_state.editing_housing_index] = booking_data
                else:
                    # Add new
                    st.session_state.bookings.append(booking_data)

                st.session_state.show_housing_form = False
                st.session_state.editing_housing_index = None

            if canceled:
                st.session_state.show_housing_form = False
                st.session_state.editing_housing_index = None


    # ---------------- Display Housing Bookings ----------------
    if not housing_bookings:
        st.caption("No house bookings yet.")
    else:
        for i, b in enumerate(housing_bookings):
            price_text = f" - {b.get('price','')} EUR" if b.get("price") else ""

            col_text, col_buttons = st.columns([5, 2])

            with col_text:
                st.markdown(f"**{b['type']}**: {b['title']}{price_text}")
                st.markdown(f"Dates: {b['date']}")
                if b.get("details"):
                    st.markdown(f"Details: {b['details']}")
                if b.get("link"):
                    st.markdown(f"[🔗 Listing]({b['link']})")

            with col_buttons:
                # Find index in original bookings list
                original_index = st.session_state.bookings.index(b)

                if st.button("🗑", key=f"remove_{original_index}"):
                    st.session_state.bookings.pop(original_index)
                if st.button("✏️", key=f"edit_{original_index}"):
                    st.session_state.editing_housing_index = original_index
                    st.session_state.show_housing_form = True


            st.markdown("---")


