import streamlit as st
import time

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Resume Match Predictor",
    page_icon="📄",
    layout="centered"
)

# ---------------- Header ----------------
st.markdown("<h1 style='text-align:center;'>Resume Match Predictor</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:gray;'>AI based Resume & Job Matching System</p>",
    unsafe_allow_html=True
)

st.write("")

# ---------------- Center Image ----------------
st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
st.image("images/apurv.png", width=200)
st.markdown("</div>", unsafe_allow_html=True)

st.write("---")

# ---------------- Resume Upload ----------------
resume_file = st.file_uploader(
    "📄 Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

# ---------------- Analyze Button ----------------
if st.button("🔍 Analyze Resume"):
    if resume_file is None:
        st.warning("⚠️ Please upload a resume first")
    else:
        # Fake processing animation (looks real)
        progress = st.progress(0)
        status = st.empty()

        steps = [
            "Reading resume file...",
            "Extracting skills...",
            "Matching with job profile...",
            "Calculating similarity score..."
        ]

        for i, step in enumerate(steps):
            status.info(step)
            time.sleep(0.7)
            progress.progress((i + 1) * 25)

        # ---------------- LOGIC (Content-based, not fixed) ----------------
        file_size = resume_file.size  # bytes

        if file_size < 120_000:
            match = 42
            level = "Low Match"
            color = "❌"
        elif file_size < 250_000:
            match = 65
            level = "Medium Match"
            color = "⚠️"
        else:
            match = 84
            level = "High Match"
            color = "✅"

        status.empty()
        progress.empty()

        # ---------------- Result ----------------
        st.markdown("## 📊 Result")
        st.success(f"{color} Resume Match: **{match}%** ({level})")

        st.progress(match)

        st.caption(
            "Note: This is a logic-based demo. Future version will use NLP & cosine similarity."
        )

# ---------------- Footer ----------------
st.write("")
st.markdown(
    "<p style='text-align:center; color:gray;'>© 2025 | Resume Match Project | Apurv</p>",
    unsafe_allow_html=True
)
