# frontend.py - AI Tutor with PDF Upload

import streamlit as st
from backend import get_ai_response, extract_pdf_text

# Page config
st.set_page_config(
    page_title="Learn With Parikshit's-AI",
    page_icon="👨‍🏫",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 10px;
        margin: 5px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stChatInput input {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid #e94560 !important;
        border-radius: 25px !important;
        color: white !important;
        font-size: 16px !important;
    }
    .main-title {
        text-align: center;
        font-size: 3em;
        font-weight: bold;
        background: linear-gradient(90deg, #e94560, #0f3460, #e94560);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px 0;
    }
    .subtitle {
        text-align: center;
        color: rgba(255,255,255,0.6);
        font-size: 1.1em;
        margin-bottom: 30px;
    }
    .pdf-success {
        background: rgba(0, 255, 100, 0.1);
        border: 1px solid rgba(0, 255, 100, 0.3);
        border-radius: 10px;
        padding: 10px;
        color: #00ff64;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = ""

# Sidebar
with st.sidebar:
    st.markdown('<div class="main-title">🎓 ParikshaAI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your Smart AI Tutor by Parikshit — upload notes & ask anything!</div>', unsafe_allow_html=True)

    # Subject selector
    subject = st.selectbox(
        "📚 Choose a Subject",
        ["General", "Mathematics", "Science", "History",
         "Languages", "Programming", "Geography"]
    )

    st.markdown("---")

    # PDF Upload section
    st.markdown("### 📄 Upload Study Notes")
    uploaded_pdf = st.file_uploader(
        "Upload a PDF file",
        type=["pdf"],
        help="Upload your notes and ask questions about them!"
    )

    if uploaded_pdf:
        if uploaded_pdf.name != st.session_state.pdf_name:
            with st.spinner("📖 Reading PDF..."):
                st.session_state.pdf_text = extract_pdf_text(uploaded_pdf)
                st.session_state.pdf_name = uploaded_pdf.name
        st.markdown(f"""
        <div class="pdf-success">
            ✅ {uploaded_pdf.name}<br>
            📝 Ready to answer questions!
        </div>
        """, unsafe_allow_html=True)

    # Remove PDF button
    if st.session_state.pdf_text:
        if st.button("🗑️ Remove PDF", use_container_width=True):
            st.session_state.pdf_text = ""
            st.session_state.pdf_name = ""
            st.rerun()

    st.markdown("---")

    # Stats
    st.markdown("### 📊 Session Stats")
    msg_count = len(st.session_state.chat_history)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Messages", msg_count)
    with col2:
        st.metric("Topic", subject[:4] + "...")

    # PDF indicator
    if st.session_state.pdf_text:
        st.success(f"📄 PDF loaded!")

    st.markdown("---")

    # Clear chat
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")
    st.markdown("**💡 Tips:**")
    st.markdown("- Upload your notes as PDF")
    st.markdown("- Ask questions about the PDF")
    st.markdown("- Say 'summarize the PDF'")
    st.markdown("- Ask for a quiz from PDF")

# Main area
st.markdown('<div class="main-title">🎓 ParikshaAI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your Smart AI Tutor by Parikshit — upload notes & ask anything!</div>', unsafe_allow_html=True)

# Subject selector visible on main page for mobile
col1, col2, col3 = st.columns([1,2,1])
with col2:
    subject = st.selectbox(
        "📚 Choose a Subject",
        ["General", "Mathematics", "Science", "History",
         "Languages", "Programming", "Geography"],
        key="main_subject"
    )

# Welcome message
if len(st.session_state.chat_history) == 0:
    with st.chat_message("assistant"):
        if st.session_state.pdf_text:
            st.markdown(f"👋 Hello! I've read your PDF **'{st.session_state.pdf_name}'**. Ask me anything about it!")
        else:
            st.markdown(f"👋 Hello! I'm your **AI Tutor** for **{subject}**! Upload a PDF or ask me anything!")

            # PDF upload on main page (visible on mobile too!)
if not st.session_state.pdf_text:
    st.markdown("### 📄 Upload Your Study Notes")
    main_pdf = st.file_uploader(
        "Upload a PDF file here 👇",
        type=["pdf"],
        key="main_uploader",
        help="Upload your notes and ask questions!"
    )
    if main_pdf:
        with st.spinner("📖 Reading your PDF..."):
            st.session_state.pdf_text = extract_pdf_text(main_pdf)
            st.session_state.pdf_name = main_pdf.name
        st.success(f"✅ **{main_pdf.name}** uploaded! Now ask me anything about it!")
        st.rerun()
else:
    st.info(f"📄 Currently loaded: **{st.session_state.pdf_name}**")

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant"):
            st.write(message["content"])

# Chat input
if st.session_state.pdf_text:
    placeholder = "Ask a question about your PDF..."
else:
    placeholder = f"Ask your {subject} question here..."

user_input = st.chat_input(placeholder)

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("🤔 Thinking..."):
        enhanced_message = f"[Subject: {subject}] {user_input}"
        ai_reply = get_ai_response(
            enhanced_message,
            st.session_state.chat_history,
            st.session_state.pdf_text  # Pass PDF content
        )

    with st.chat_message("assistant"):
        st.write(ai_reply)

    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
    st.rerun()