import streamlit as st
import numpy as np
from PIL import Image

st.set_page_config(page_title="Observa Terram", layout="wide")

if "zoom_sar" not in st.session_state:
    st.session_state.zoom_sar = 100
if "zoom_normal" not in st.session_state:
    st.session_state.zoom_normal = 100
if "pan_sar_idx" not in st.session_state:
    st.session_state.pan_sar_idx = 0
if "interp_idx" not in st.session_state:
    st.session_state.interp_idx = 0

PROJECT_NAME = "A Culturable Wasteland Analysis"
LAND_AREA = "67 acres +"
LOCATION = "NISAR"

SAR_IMAGES = {
    "19 June 2026":        "19 June 2026.png",
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

NORMAL_IMAGE = "Area Of Interest_Lnad2.png"

INTERPRETATION_SLIDES = [
    "Slide1.png",
    "Slide2.png",
    "Slide3.png",
    "Slide4.png",
    "Slide5.png",
    "Slide6.png",
    "Slide7.png",
]

def render_image_box(image_ref, caption_text="", zoom_percent=None):
    if image_ref.startswith("Slide"):
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

left_panel, main_panel = st.columns((1, 3.5), gap="large")

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

with main_panel:
    st.subheader("Observa Terram — Time Changes All")

    active_tab = st.radio(
        "Navigation",
        ("SAR-Normal", "Side-by-Side", "SAR Only", "Normal Only", "Pan-SAR Panel", "Interpretation Panel"),
        horizontal=True,
        label_visibility="collapsed"
    )

    sar_dates_list = list(SAR_IMAGES.keys())

    if active_tab == "SAR-Normal":
        col_sar, col_norm = st.columns(2, gap="medium")
        with col_sar:
            st.subheader("SAR View")
            first_sar_key = next(iter(SAR_IMAGES))
            render_image_box(SAR_IMAGES[first_sar_key], "SAR Radar Sensor View")
        with col_norm:
            st.subheader("Normal View")
            render_image_box(NORMAL_IMAGE, "Normal Optical Sensor View")

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
            st.markdown(f"#### 📅 {curr_date}")
            render_image_box(SAR_IMAGES[curr_date], f"Pass {curr_idx + 1}/{total_sar} — {curr_date}")
        with next_btn_col:
            if st.button("▶", key="pan_next", use_container_width=True, help="Next SAR Pass"):
                st.session_state.pan_sar_idx = (curr_idx + 1) % total_sar
                st.rerun()

    elif active_tab == "Interpretation Panel":
        total_slides = len(INTERPRETATION_SLIDES)
        s_idx = st.session_state.interp_idx
        curr_slide = INTERPRETATION_SLIDES[s_idx]

        st.subheader(f"Interpretation Panel (Slide {s_idx + 1} of {total_slides})")
        st.progress((s_idx + 1) / total_slides)

        prev_s_col, slide_col, next_s_col = st.columns((1, 6, 1), vertical_alignment="center")
        with prev_s_col:
            if st.button("◀", key="interp_prev", use_container_width=True, help="Previous Slide"):
                st.session_state.interp_idx = (s_idx - 1) % total_slides
                st.rerun()
        with slide_col:
            render_image_box(curr_slide, f"Slide {s_idx + 1} of {total_slides}")
        with next_s_col:
            if st.button("▶", key="interp_next", use_container_width=True, help="Next Slide"):
                st.session_state.interp_idx = (s_idx + 1) % total_slides
                st.rerun()

    st.write("")
    t_start, t_end = st.columns(2)
    with t_start:
        st.markdown("**June 2026**")
    with t_end:
        st.markdown("<div style='text-align: right; font-weight: bold;'>October 2026</div>", unsafe_allow_html=True)

    st.markdown(
        "<div style='height: 10px; background-color: #38BDF8; border-radius: 5px; margin-top: -10px; margin-bottom: 10px;'></div>",
        unsafe_allow_html=True
    )
