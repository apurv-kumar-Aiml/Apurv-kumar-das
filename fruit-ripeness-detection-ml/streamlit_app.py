import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Fruit Ripeness Detection",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.main {
    background-color: #f5f5f5;
}

.title {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    color: #ff2e63;
    margin-top: -20px;
}

.subtitle {
    text-align: center;
    font-size: 22px;
    color: #222222;
    font-weight: bold;
    margin-bottom: 30px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 0px 15px rgba(0,0,0,0.2);
    margin-top: 20px;
}

.result {
    font-size: 32px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown(
    '<div class="title">🍎 Fruit Ripeness Detection</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Detect Ripeness & Rotten Areas using Image Processing</div>',
    unsafe_allow_html=True
)

st.write("")

# ---------------- FILE UPLOADER ----------------
file = st.file_uploader(
    "📂 Upload Fruit Image",
    type=["jpg", "jpeg", "png"]
)

# ---------------- PROCESS IMAGE ----------------
if file is not None:

    image = Image.open(file)

    # Loading
    with st.spinner("🔍 Processing Image..."):
        time.sleep(1)

    col1, col2 = st.columns(2)

    # -------- ORIGINAL IMAGE --------
    with col1:
        st.subheader("📸 Original Image")
        st.image(image, use_container_width=True)

    # Convert image
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # ---------------- RIPENESS DETECTION ----------------
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Yellow mask
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([35, 255, 255])

    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Green mask
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])

    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    yellow_ratio = np.sum(yellow_mask) / (img.shape[0] * img.shape[1])
    green_ratio = np.sum(green_mask) / (img.shape[0] * img.shape[1])

    # Prediction
    if yellow_ratio > 0.3:
        ripeness = "Ripe 🟡"
        result_color = "green"

    elif green_ratio > 0.3:
        ripeness = "Unripe 🟢"
        result_color = "orange"

    else:
        ripeness = "Overripe 🔴"
        result_color = "red"

    # ---------------- ROTTEN AREA DETECTION ----------------
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(
        gray,
        50,
        255,
        cv2.THRESH_BINARY_INV
    )

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contours:

        if cv2.contourArea(cnt) > 500:

            x, y, w, h = cv2.boundingRect(cnt)

            cv2.rectangle(
                img,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                3
            )

    # -------- DETECTED IMAGE --------
    with col2:
        st.subheader("🔍 Detected Output")

        st.image(
            cv2.cvtColor(img, cv2.COLOR_BGR2RGB),
            use_container_width=True
        )

    # ---------------- PROGRESS BAR ----------------
    progress = st.progress(0)

    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    # ---------------- RESULT CARD ----------------
    st.markdown(f"""
    <div class="card">
        <div class="result" style="color:{result_color};">
            Prediction: {ripeness}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.success("✅ Detection Completed Successfully")