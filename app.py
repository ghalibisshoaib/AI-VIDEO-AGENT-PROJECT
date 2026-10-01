import streamlit as st
import tempfile
import os

from main import run_pipeline
from core.rag_enging import ask_question


st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# CUSTOM DESIGN
# ---------------------------------------------------------

st.markdown("""
<style>

@import url(
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 20% 10%,
            rgba(99,102,241,.12),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(168,85,247,.10),
            transparent 25%
        ),
        #07070a;
    color: #f5f5f5;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0b0b10;
    border-right: 1px solid rgba(255,255,255,.07);
}

/* Main container */
.block-container {
    max-width: 1400px;
    padding-top: 2rem;
}

/* Hero */
.hero {
    padding: 35px 0 30px 0;
}

.hero-badge {
    display: inline-block;
    padding: 7px 12px;
    border-radius: 999px;
    background: rgba(99,102,241,.12);
    border: 1px solid rgba(99,102,241,.25);
    color: #a5b4fc;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 18px;
}

.hero-title {
    font-size: 48px;
    line-height: 1.05;
    font-weight: 800;
    letter-spacing: -2px;
    margin: 0;
}

.hero-title span {
    background: linear-gradient(
        90deg,
        #818cf8,
        #c084fc,
        #f472b6
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    color: #9ca3af;
    font-size: 17px;
    max-width: 680px;
    margin-top: 18px;
    line-height: 1.7;
}

/* Cards */
.ai-card {
    background: rgba(18,18,25,.82);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 18px;
    box-shadow: 0 15px 50px rgba(0,0,0,.25);
}

.metric-card {
    background: rgba(18,18,25,.8);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 18px;
    padding: 20px;
}

.metric-label {
    color: #8b8b98;
    font-size: 13px;
}

.metric-value {
    font-size: 28px;
    font-weight: 750;
    margin-top: 5px;
}

/* Section headings */
.section-title {
    font-size: 22px;
    font-weight: 750;
    margin: 25px 0 12px 0;
}

.section-description {
    color: #858592;
    font-size: 14px;
}

/* Upload */
[data-testid="stFileUploader"] {
    background: rgba(20,20,28,.7);
    border: 1px dashed rgba(129,140,248,.35);
    border-radius: 18px;
    padding: 15px;
}

/* Buttons */
.stButton > button {
    border-radius: 12px;
    border: 1px solid rgba(129,140,248,.3);
    background: linear-gradient(
        135deg,
        #6366f1,
        #8b5cf6
    );
    color: white;
    font-weight: 650;
    padding: 10px 22px;
    transition: .2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 30px rgba(99,102,241,.25);
}

/* Text input */
.stTextInput input {
    background: #101017 !important;
    border: 1px solid rgba(255,255,255,.08) !important;
    border-radius: 12px !important;
    color: white !important;
}

/* Tabs */
button[data-baseweb="tab"] {
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "results" not in st.session_state:
    st.session_state.results = None

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:22px;
            font-weight:800;
            padding:10px 0 25px 0;
        ">
            ✦ AI Video Assistant
        </div>
        """,
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Analyze",
            "Transcript",
            "AI Chat",
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.caption("AI ENGINE")

    st.markdown(
        """
        <div style="
            padding:12px;
            background:rgba(34,197,94,.08);
            border:1px solid rgba(34,197,94,.15);
            border-radius:12px;
            font-size:13px;
        ">
        🟢 System operational
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.caption("AI Video Assistant")
    st.caption("Transform conversations into actionable intelligence.")


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

if page == "Dashboard":

    st.markdown("""
    <div class="hero">

        <div class="hero-badge">
            ✦ AI-POWERED MEETING INTELLIGENCE
        </div>

        <h1 class="hero-title">
            Turn conversations into
            <span>intelligence.</span>
        </h1>

        <p class="hero-description">
            Upload a meeting, lecture, interview or video and let AI
            transcribe, summarize and extract the most important insights.
        </p>

    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">TRANSCRIPTION</div>
            <div class="metric-value">AI</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">SUMMARY</div>
            <div class="metric-value">✦</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">INSIGHTS</div>
            <div class="metric-value">AI</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">AI Q&A</div>
            <div class="metric-value">24/7</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">How it works</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="ai-card">
        <h3>01 · Upload</h3>
        <p style="color:#999">
        Upload audio/video or provide a supported video URL.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="ai-card">
        <h3>02 · Analyze</h3>
        <p style="color:#999">
        AI transcribes and analyzes the entire conversation.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="ai-card">
        <h3>03 · Understand</h3>
        <p style="color:#999">
        Get summaries, decisions, actions and AI answers.
        </p>
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------
# ANALYZE
# ---------------------------------------------------------

elif page == "Analyze":

    st.markdown("""
    <div class="hero">
        <div class="hero-badge">NEW ANALYSIS</div>

        <h1 class="hero-title">
            Analyze your <span>conversation.</span>
        </h1>

        <p class="hero-description">
            Upload a recording or paste a video URL.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Input source</div>',
        unsafe_allow_html=True
    )

    input_mode = st.radio(
        "Source",
        ["Upload file", "Video URL"],
        horizontal=True,
        label_visibility="collapsed"
    )

    source = None

    if input_mode == "Upload file":

        uploaded_file = st.file_uploader(
            "Drop your media here",
            type=[
                "mp4",
                "mov",
                "avi",
                "mkv",
                "mp3",
                "wav",
                "m4a"
            ]
        )

        if uploaded_file:

            temp_dir = tempfile.mkdtemp()

            source = os.path.join(
                temp_dir,
                uploaded_file.name
            )

            with open(source, "wb") as file:
                file.write(uploaded_file.getbuffer())

            st.success(
                f"Ready: {uploaded_file.name}"
            )

    else:

        source = st.text_input(
            "Video URL",
            placeholder="https://youtube.com/watch?v=..."
        )

    col1, col2 = st.columns(2)

    with col1:

        language = st.selectbox(
            "Spoken language",
            [
                "Auto detect",
                "en",
                "Spanish",
                "French",
                "German",
                "Urdu",
                "Arabic"
            ]
        )

    with col2:

        translate = st.toggle(
            "Translate to English"
        )

    enable_rag = st.toggle(
        "Enable AI Q&A",
        value=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "✦ Analyze with AI",
        use_container_width=True
    ):

        if not source:
            st.warning(
                "Please upload a file or enter a video URL."
            )

        else:

            progress = st.progress(0)
            status = st.empty()

            def update_progress(message, value):
                status.markdown(
                    f"**{message}**"
                )
                progress.progress(value)

            try:

                results = run_pipeline(
                    source=source,
                    language=(
                        None
                        if language == "Auto detect"
                        else language
                    ),
                    translate=translate,
                    include_rag=enable_rag,
                    progress_callback=update_progress,
                )

                st.session_state.results = results

                if "rag_chain" in results:
                    st.session_state.rag_chain = (
                        results["rag_chain"]
                    )

                progress.progress(100)
                status.success(
                    "Analysis completed successfully."
                )

                st.balloons()

            except Exception as error:

                st.error(
                    f"Analysis failed: {error}"
                )


# ---------------------------------------------------------
# RESULTS
# ---------------------------------------------------------

elif page == "Transcript":

    results = st.session_state.results

    if not results:

        st.info(
            "No analysis available yet. Go to Analyze and process a recording."
        )

    else:

        title = results.get(
            "title",
            "Meeting Transcript"
        )

        st.markdown(
            f"""
            <div class="hero">
                <div class="hero-badge">
                    AI ANALYSIS COMPLETE
                </div>

                <h1 class="hero-title">
                    {title}
                </h1>

                <p class="hero-description">
                    AI-generated meeting intelligence.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        transcript = results.get(
            "transcript",
            ""
        )

        words = len(transcript.split())

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Words",
                f"{words:,}"
            )

        with c2:
            st.metric(
                "Characters",
                f"{len(transcript):,}"
            )

        with c3:
            action_items = str(
                results.get(
                    "action_items",
                    ""
                )
            )

            st.metric(
                "Action items",
                len(
                    [
                        x
                        for x in action_items.splitlines()
                        if x.strip()
                    ]
                )
            )

        with c4:

            decisions = str(
                results.get(
                    "key_decisions",
                    ""
                )
            )

            st.metric(
                "Decisions",
                len(
                    [
                        x
                        for x in decisions.splitlines()
                        if x.strip()
                    ]
                )
            )

        tabs = st.tabs(
            [
                "Overview",
                "Action Items",
                "Decisions",
                "Questions",
                "Transcript"
            ]
        )

        with tabs[0]:

            st.markdown(
                '<div class="section-title">Executive Summary</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="ai-card">
                    {str(results.get("summary", "")).replace(chr(10), "<br>")}
                </div>
                """,
                unsafe_allow_html=True
            )

        with tabs[1]:

            st.markdown(
                '<div class="section-title">Action Items</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                str(
                    results.get(
                        "action_items",
                        "No action items found."
                    )
                )
            )

        with tabs[2]:

            st.markdown(
                '<div class="section-title">Key Decisions</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                str(
                    results.get(
                        "key_decisions",
                        "No decisions found."
                    )
                )
            )

        with tabs[3]:

            st.markdown(
                '<div class="section-title">Open Questions</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                str(
                    results.get(
                        "open_questions",
                        "No open questions found."
                    )
                )
            )

        with tabs[4]:

            search = st.text_input(
                "Search transcript",
                placeholder="Search keywords..."
            )

            if search:

                lines = transcript.splitlines()

                filtered = [
                    line
                    for line in lines
                    if search.lower() in line.lower()
                ]

                st.text_area(
                    "Results",
                    "\n".join(filtered),
                    height=500
                )

            else:

                st.text_area(
                    "Full transcript",
                    transcript,
                    height=600
                )

            st.download_button(
                "Download transcript",
                transcript,
                file_name="transcript.txt",
                mime="text/plain"
            )


# ---------------------------------------------------------
# AI CHAT
# ---------------------------------------------------------

elif page == "AI Chat":

    st.markdown("""
    <div class="hero">

        <div class="hero-badge">
            ✦ RAG INTELLIGENCE
        </div>

        <h1 class="hero-title">
            Ask your <span>conversation.</span>
        </h1>

        <p class="hero-description">
            Ask questions and get answers grounded in the analyzed transcript.
        </p>

    </div>
    """, unsafe_allow_html=True)

    rag_chain = st.session_state.rag_chain

    if not rag_chain:

        st.info(
            "Run an analysis with AI Q&A enabled first."
        )

    else:

        question = st.text_input(
            "Ask a question",
            placeholder="What were the biggest decisions?"
        )

        if st.button(
            "Ask AI",
            use_container_width=True
        ):

            if question:

                with st.spinner(
                    "Searching conversation..."
                ):

                    try:

                        answer = ask_question(
                            rag_chain,
                            question
                        )

                        st.markdown(
                            '<div class="section-title">AI Answer</div>',
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"""
                            <div class="ai-card">
                                {answer}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    except Exception as error:

                        st.error(
                            f"Unable to answer: {error}"
                        )