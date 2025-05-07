import streamlit as st
from lecture4 import process_input
import os

st.set_page_config(page_title="🎓 AI Lecture Summarizer", layout="centered")

st.title("🎓 AI-Powered Lecture Summarizer")
st.markdown("Summarize lectures from 🎙️ mic, 📂 files, or 📺 YouTube using Whisper and Hugging Face models.")

# --- Input source selection ---
source_type = st.radio("Select input source:", ["Mic", "File", "YouTube"])

# --- Export format selection ---
export_format = st.selectbox("Select export format:", ["PDF", "Word", "JSON"])

# --- Input handling based on source ---
if source_type == "Mic":
    duration = st.slider("Select recording duration (in minutes)", 0.5, 10.0, 1.0, 0.5)
    if st.button("🎙️ Record and Summarize"):
        with st.spinner("Recording and processing..."):
            result = process_input(source_type="mic", duration=int(duration * 60), export_format=export_format)
elif source_type == "File":
    file = st.file_uploader("Upload an audio/video file", type=["wav", "mp3", "m4a"])
    if file is not None:
        file_path = os.path.join("uploaded_" + file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())
        if st.button("📂 Process File"):
            with st.spinner("Transcribing and summarizing..."):
                result = process_input(source_type="file", file_path=file_path, export_format=export_format)
            os.remove(file_path)
elif source_type == "YouTube":
    youtube_url = st.text_input("Enter YouTube URL:")
    if st.button("📺 Process YouTube Video"):
        with st.spinner("Downloading, transcribing, and summarizing..."):
            result = process_input(source_type="youtube", youtube_url=youtube_url, export_format=export_format)

# --- Display results ---
if 'result' in locals() and result:
    if "error" in result:
        st.error("❌ Error: " + result["error"])
    else:
        st.success(f"✅ Summary generated and saved as: `{result['output_file']}`")

        with st.expander("📜 Overall Summary"):
            st.write(result["overall_summary"])

        with st.expander("📄 Overview"):
            st.write(result["overview"])

        with st.expander("📌 Key Points"):
            st.write(result["keypoints"])

        with open(result["output_file"], "rb") as f:
            st.download_button(
                label=f"⬇️ Download {export_format}",
                data=f,
                file_name=result["output_file"],
                mime="application/octet-stream"
            )
