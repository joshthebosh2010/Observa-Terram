import streamlit as st
import numpy as np
from PIL import Image

# --- PAGE SETUP ---
st.set_page_config(page_title="Observa Terram", layout="wide")

# Initialize interactive state memory
if "zoom_sar" not in st.session_state:
    st.session_state.zoom_sar = 100
if "zoom_normal" not in st.session_state:
    st.session_state.zoom_normal = 100
if "pan_sar_idx" not in st.session_state:
    st.session_state.pan_sar_idx = 0

# ==============================================================================
# [1: SITE INFO]
# ==============================================================================
PROJECT_NAME = "Observa Terram--Observing the Changing Land"
LAND_AREA = "67 acres +"
LOCATION = "A Piece Of Wild Wasteland, Narsingi, Hyderabad, India"

# ==============================================================================
# [2: 17 SAR IMAGES BY EXACT DATE]
# ==============================================================================
SAR_IMAGES = {
    "19 June 2026":        "19 June 2026.png",
    "20 June 2026":        "20 June 2026.png",
    "01 July 2026":        "1 July 2026.png",
    "02 July 2026":        "2 July 2026.png",
    "13 July 2026":        "13 July 2026.png",
    "14 July 2026":        "14 July 2026.png",
    "26 July 2026":        "26 July 2026.png",
    "18 August 2026":      "18 August 2026'.png",
    "19 August 2026":      "19 August 2026.png",
    "31 August 2026":      "31 August 2026.png",
    "12 September 2026":   "12 September 2026.png",
    "23 September 2026":   "23 September 2026.png",
    "24 September 2026":   "24 September 2026.png",
    "05 October 2026":     "5 October 2026.png",
    "06 October 2026":     "6 October 2026.png",
    "17 October 2026":     "17 October 2026.png",
    "18 October 2026":     "18 October 2026.png",
}

# ==============================================================================
# [3: SINGLE NORMAL OPTICAL VIEW (NO SPECIFIC DATE)]
# ==============================================================================
NORMAL_IMAGE = "Area Of Interest_Lnad.png"

# --- HELPER FUNCTION TO SAFELY DISPLAY SCIENTIFIC & STANDARD IMAGES ---
def render_image_box(image_ref, caption_text="", zoom_percent=None):
    if image_ref.startswith("PLACEHOLDER"):
        st.info(f"🖼️ **[{image_ref}]** {caption_text}")
    else:
        img = Image.open(image_ref)
        if img.mode not in ("RGB", "RGBA", "L"):
            arr = np.nan_to_num(np.array(img, dtype=float))
            low, high = np.percentile(arr, (2, 98))
            arr = np.clip((arr - low) / (high - low + 1e-8) * 255, 0, 255).astype(np.uint8)
            img = Image.fromarray(arr)

        if zoom_percent is not None:
            pixel_width = int(750 * (zoom_percent / 100))
            st.image(img, caption=caption_text, width=pixel_width)
        else:
            st.image(img, caption=caption_text, use_container_width=True)

# --- MAIN LAYOUT: SLIM LEFT PANEL + WIDE VIEWING AREA ---
left_panel, main_panel = st.columns((1, 3.5), gap="large")

# --- LEFT PANEL: SITE INFORMATION & SAR LEGEND ---
with left_panel:
    st.subheader("Site Information & Legend")
    
    with st.container(border=True):
        st.markdown("ℹ️ **Site Info**")
        st.text_input("Project Name", value=PROJECT_NAME, disabled=True, label_visibility="collapsed")
        st.text_input("Land Area", value=LAND_AREA, disabled=True, label_visibility="collapsed")
        st.text_input("Location", value=LOCATION, disabled=True, label_visibility="collapsed")

    with st.container(border=True):
        st.markdown("**SAR Legend**")
        st.markdown(" **Bright** = Rough Surfaces [Higher Backscatter--Buildings,metals,etc]")
        st.markdown(" **Dark** = Smooth Surface [Lower Backscatter--Roads,lakes,etc.] ")
        st.markdown(" **Grey** = Medium [Moderate Backscatter--Vegetation,soil,etc.] ")

# --- RIGHT MAIN PANEL: OBSERVA TERRAM ---
with main_panel:
    # Compact Header & Tagline for extra viewing space
    st.markdown("<h2 style='text-align: center; margin-top: -25px; margin-bottom: 0;'>Observa Terram</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 15px; color: #CBD5E1; margin-top: -5px; margin-bottom: 10px;'>Time Changes All</p>", unsafe_allow_html=True)

    active_tab = st.radio(
        "Navigation",
        (
            "SAR-Normal",
            "Side-by-Side",
            "SAR Only",
            "Normal Only",
            "Pan-SAR Panel"
        ),
        horizontal=True,
        label_visibility="collapsed"
    )

    sar_dates_list = list(SAR_IMAGES.keys())

    # TAB 1: SAR-NORMAL (No Dates)
    if active_tab == "SAR-Normal":
        col_sar, col_norm = st.columns(2, gap="medium")
        with col_sar:
            st.subheader("SAR View")
            first_sar_key = next(iter(SAR_IMAGES))
            render_image_box(SAR_IMAGES[first_sar_key], "SAR Radar Sensor View")
        with col_norm:
            st.subheader("Normal View")
            render_image_box(NORMAL_IMAGE, "Normal Optical Sensor View")

    # TAB 2: SIDE-BY-SIDE (Two SAR Views with Independent Date Selectors)
    elif active_tab == "Side-by-Side":
        col_a, col_b = st.columns(2, gap="medium")
        with col_a:
            st.subheader("SAR View A")
            date_a = st.selectbox("Select Date (Left)", options=sar_dates_list, index=0, key="date_a")
            render_image_box(SAR_IMAGES[date_a], f"SAR Radar Pass: {date_a}")
        with col_b:
            st.subheader("SAR View B")
            default_b = len(sar_dates_list) - 1
            date_b = st.selectbox("Select Date (Right)", options=sar_dates_list, index=default_b, key="date_b")
            render_image_box(SAR_IMAGES[date_b], f"SAR Radar Pass: {date_b}")

    # TAB 3: SAR ONLY (Single Large Zoomable SAR Image with Exact Date)
    elif active_tab == "SAR Only":
        head_col, z_in, z_out = st.columns((4, 1, 1))
        with head_col:
            st.subheader("SAR View")
        with z_in:
            if st.button("Zoom In +", key="sar_zoom_in", use_container_width=True):
                st.session_state.zoom_sar = min(200, st.session_state.zoom_sar + 25)
        with z_out:
            if st.button("Zoom Out -", key="sar_zoom_out", use_container_width=True):
                st.session_state.zoom_sar = max(50, st.session_state.zoom_sar - 25)

        sel_sar_date = st.selectbox("Select Exact SAR Date", options=sar_dates_list, key="sar_only_date")
        st.caption(f"Current Zoom: {st.session_state.zoom_sar}%")
        render_image_box(SAR_IMAGES[sel_sar_date], f"SAR Radar Pass: {sel_sar_date}", zoom_percent=st.session_state.zoom_sar)

    # TAB 4: NORMAL ONLY (Single Large Zoomable Normal View, No Date)
    elif active_tab == "Normal Only":
        head_col, z_in, z_out = st.columns((4, 1, 1))
        with head_col:
            st.subheader("Normal View")
        with z_in:
            if st.button("Zoom In +", key="norm_zoom_in", use_container_width=True):
                st.session_state.zoom_normal = min(200, st.session_state.zoom_normal + 25)
        with z_out:
            if st.button("Zoom Out -", key="norm_zoom_out", use_container_width=True):
                st.session_state.zoom_normal = max(50, st.session_state.zoom_normal - 25)

        st.caption(f"Current Zoom: {st.session_state.zoom_normal}%")
        render_image_box(NORMAL_IMAGE, "Normal Optical Sensor View", zoom_percent=st.session_state.zoom_normal)

    # TAB 5: PAN-SAR PANEL (Sideways Shorts-Style Carousel)
    elif active_tab == "Pan-SAR Panel":
        total_sar = len(sar_dates_list)
        curr_idx = st.session_state.pan_sar_idx
        curr_date = sar_dates_list[curr_idx]

        st.subheader(f"Pan-SAR Panel ({curr_idx + 1} of {total_sar})")
        st.progress((curr_idx + 1) / total_sar)

        prev_btn_col, img_col, next_btn_col = st.columns((1, 6, 1), vertical_alignment="center")
        with prev_btn_col:
            if st.button("◀", key="pan_prev", use_container_width=True, help="Previous SAR Pass"):
                st.session_state.pan_sar_idx = (curr_idx - 1) % total_sar
                st.rerun()
        with img_col:
            st.markdown(f"<h4 style='text-align: center;'>📅 {curr_date}</h4>", unsafe_allow_html=True)
            render_image_box(SAR_IMAGES[curr_date], f"Pass {curr_idx + 1}/{total_sar} — {curr_date}")
        with next_btn_col:
            if st.button("▶", key="pan_next", use_container_width=True, help="Next SAR Pass"):
                st.session_state.pan_sar_idx = (curr_idx + 1) % total_sar
                st.rerun()

    st.write("")

    # --- BOTTOM: NON-INTERACTIVE LIGHT BLUE TIME BAR (JUNE 2026 - OCTOBER 2026) ---
    t_start, t_end = st.columns(2)
    with t_start:
        st.markdown("**June 2026**")
    with t_end:
        st.markdown("<p style='text-align: right; font-weight: bold;'>October 2026</p>", unsafe_allow_html=True)

    st.markdown(
        "<div style='height: 10px; background-color: #38BDF8; border-radius: 5px; margin-top: -10px; margin-bottom: 10px;'></div>",
        unsafe_allow_html=True
    )
