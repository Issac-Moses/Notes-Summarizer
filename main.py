import streamlit as st
from lecture4 import process_input
import os
import time
from datetime import datetime
import json
import base64


def load_enhanced_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title=" AI Lecture Summarizer Pro",
    page_icon="⚜",
    layout="wide",
    initial_sidebar_state="expanded"
)


load_enhanced_css()

logo_path = "silvy_logo.png"
if os.path.exists(logo_path):
    with open(logo_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
        st.markdown(f"""
        <div style='text-align: center; margin-top: -2rem; margin-bottom: 1rem;'>
            <img src="data:image/png;base64,{encoded}" style='height: 80px;' />
        </div>
        """, unsafe_allow_html=True)


if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_result' not in st.session_state:
    st.session_state.current_result = None

st.markdown("""
<div class="main-header fade-in">
    <div class="main-title">𓅃 AI Lecture Summarizer Pro</div>
    <div class="subtitle">Transform your audio content into intelligent summaries</div>
    <div style="margin-top: 1rem;">
        <span style="background: rgba(76,175,80,0.2); padding: 0.25rem 0.75rem; border-radius: 15px; color: white; font-size: 0.9rem;">
            💀 Powered by Silvy AI
        </span>
    </div>
</div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("""
    <div class="glass-container">
        <h2 style="color: white; text-align: center; margin-bottom: 1rem;">⚙️ Settings</h2>
    </div>
    """, unsafe_allow_html=True)

    theme = st.selectbox(
        " .✯. Theme",
        ["Dark Gradient", "Ocean Blue", "Sunset Orange", "Forest Green"],
        index=0
    )

    st.markdown("### ֍  Quality Settings")
    transcription_quality = st.select_slider(
        "Transcription Quality",
        options=["Fast", "Medium", "High"],
        value="Medium"
    )

    summary_length = st.select_slider(
        "Summary Length",
        options=["Brief", "Medium", "Detailed"],
        value="Medium"
    )

    st.markdown("---")
    st.markdown("### ☯ Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Summaries", len(st.session_state.history))
    with col2:
        st.metric("Success Rate", "98%")

    st.markdown("---")
    st.markdown("""
    <div class="glass-container">
        <h3 style="color: white; margin-bottom: 1rem;">✉ About</h3>
        <p style="color: rgba(255,255,255,0.8); line-height: 1.6;">
            This AI-powered tool transforms your audio content into comprehensive summaries using advanced machine learning.
        </p>
        <div style="margin-top: 1rem;">
            <span style="color: #4CAF50;">✓</span> Real-time transcription<br>
            <span style="color: #4CAF50;">✓</span> Smart summarization<br>
            <span style="color: #4CAF50;">✓</span> Multiple export formats<br>
            <span style="color: #4CAF50;">✓</span> YouTube integration
        </div>
    </div>
    """, unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs(["❄ Summarize", "✠ History", "∞ Analytics"])


with tab1:
    st.markdown("### ✧ Choose Your Input Method")
    col1, col2, col3 = st.columns(3)

    with col1:
        mic_clicked = st.button("♬ Microphone", key="mic_btn", use_container_width=True)
        if mic_clicked:
            st.session_state.input_method = "mic"
    with col2:
        file_clicked = st.button("𓆰 File Upload", key="file_btn", use_container_width=True)
        if file_clicked:
            st.session_state.input_method = "file"
    with col3:
        youtube_clicked = st.button("⚘ YouTube", key="youtube_btn", use_container_width=True)
        if youtube_clicked:
            st.session_state.input_method = "youtube"

    if 'input_method' in st.session_state:
        st.markdown(f"<div class='glass-container fade-in'>", unsafe_allow_html=True)
        if st.session_state.input_method == "mic":
            st.markdown("### ♨ Microphone Recording")
            duration = st.slider("Recording Duration (minutes)", 0.5, 30.0, 5.0, 0.5)
            if st.button("❃ Start Recording"):
                st.session_state.processing = True
                with st.spinner("Recording..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        progress_bar.progress(i + 1)
                        time.sleep(duration * 60 / 100)
                    result = process_input(source_type="mic", duration=int(duration * 60), export_format="PDF")
                    st.session_state.current_result = result
                    st.session_state.processing = False

        elif st.session_state.input_method == "file":
            st.markdown("### ✉ File Upload")
            uploaded_file = st.file_uploader("Upload Audio/Video", type=["wav", "mp3", "m4a", "mp4", "avi", "mov"])
            if uploaded_file:
                st.markdown("### ☏ File Preview")
                st.info(f"File: {uploaded_file.name}")
                if uploaded_file.type.startswith('audio'):
                    st.audio(uploaded_file)
                elif uploaded_file.type.startswith('video'):
                    st.video(uploaded_file)

                if st.button("✈ Process File"):
                    st.session_state.processing = True
                    file_path = f"temp_{uploaded_file.name}"
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    with st.spinner("Processing file..."):
                        result = process_input(source_type="file", file_path=file_path, export_format="PDF")
                        st.session_state.current_result = result
                        st.session_state.processing = False
                    if os.path.exists(file_path): os.remove(file_path)

        elif st.session_state.input_method == "youtube":
            st.markdown("### ✂︎ YouTube Video Processing")
            youtube_url = st.text_input("Enter YouTube URL")
            if youtube_url:
                if "youtube.com" in youtube_url or "youtu.be" in youtube_url:
                    st.success("✗ Valid YouTube URL")
                    if st.button("⛱︎ Process Video"):
                        st.session_state.processing = True
                        with st.spinner("Processing video..."):
                            result = process_input(source_type="youtube", youtube_url=youtube_url, export_format="PDF")
                            st.session_state.current_result = result
                            st.session_state.processing = False
                else:
                    st.error("𒉽 Invalid YouTube URL")
        st.markdown("</div>", unsafe_allow_html=True)


    st.markdown("### ♘ Export Options")
    col1, col2, col3 = st.columns(3)
    with col1: st.button("𓅃 PDF", use_container_width=True)
    with col2: st.button("𓆰 Word", use_container_width=True)
    with col3: st.button("❃ JSON", use_container_width=True)


if st.session_state.current_result:
    result = st.session_state.current_result
    if "error" in result:
        st.error(f"✘ Error: {result['error']}")
    else:
        st.markdown("""
        <div class="results-header fade-in">
            <div class="results-title">√ Summary Generated Successfully!</div>
            <div style="color: rgba(255,255,255,0.8);">Your content has been processed and summarized</div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(" Overall Summary", expanded=True):
            st.markdown(f"<div class='glass-container'><p>{result['overall_summary']}</p></div>", unsafe_allow_html=True)
        with st.expander(" Detailed Overview"):
            st.markdown(f"<div class='glass-container'><p>{result['overview']}</p></div>", unsafe_allow_html=True)
        with st.expander("☂ Key Points"):
            st.markdown(f"<div class='glass-container'><p>{result['keypoints']}</p></div>", unsafe_allow_html=True)

        if result["output_file"] and os.path.exists(result["output_file"]):
            with open(result["output_file"], "rb") as f:
                st.download_button("💀 Download Summary", f.read(), file_name=result["output_file"], mime="application/octet-stream")

        if result not in st.session_state.history:
            st.session_state.history.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "result": result,
                "type": st.session_state.get('input_method', 'unknown')
            })


with tab2:
    st.markdown("### ☂ Summary History")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"⌨ Summary {len(st.session_state.history) - i} - {item['timestamp']}"):
                st.markdown(f"**Input Type:** {item['type'].title()}")
                st.markdown(f"**Summary:** {item['result']['overall_summary'][:200]}...")
    else:
        st.info("No summaries yet. Start with a new one!")


with tab3:
    st.markdown("### √ Analytics Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Summaries", len(st.session_state.history), "2")
    with col2: st.metric("Avg. Processing Time", "45s", "-5s")
    with col3: st.metric("Success Rate", "98%", "1%")
    with col4: st.metric("Total Audio Hours", "12.5h", "2.3h")
    st.info("✩ Advanced analytics coming soon!")


st.markdown("""
<div class="custom-footer">
    <p><strong>𓅃 AI Lecture Summarizer Pro</strong> • v2.0</p>
    <p>Empowering education through intelligent automation</p>
    <p style="font-size: 0.9rem; margin-top: 0.5rem;">
        Built with ♡ using Streamlit • © 2025 Issac Moses & Thirumalai Nambi
    </p>
</div>
""", unsafe_allow_html=True)
