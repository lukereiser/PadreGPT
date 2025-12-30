"""
Padre GPT - Catholic Theology Assistant
A Streamlit web interface for the Padre GPT Assistant.

Designed with inspiration from medieval manuscripts, illuminated texts,
and the rich visual tradition of the Catholic Church.
"""

import os
import re
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Padre GPT — Catholic Theology Assistant",
    page_icon="✝️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM CSS — Medieval Manuscript Aesthetic
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    /* Import fonts - EB Garamond for headings, Cormorant for body */
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Cinzel:wght@400;500;600;700&display=swap');
    
    /* ═══ Root Variables ═══ */
    :root {
        --burgundy-deep: #5C1A1B;
        --burgundy: #800020;
        --burgundy-light: #9B2335;
        --gold-dark: #A67C00;
        --gold: #C9A227;
        --gold-light: #D4AF37;
        --gold-pale: #E8D5A3;
        --cream: #FDF8F0;
        --cream-dark: #F5EDE0;
        --parchment: #F8F4E8;
        --ink: #2C2416;
        --ink-light: #4A4033;
        --navy: #1E3A5F;
        --navy-light: #2C5282;
    }
    
    /* ═══ Main App Container ═══ */
    .stApp {
        background: 
            linear-gradient(180deg, 
                rgba(248, 244, 232, 0.97) 0%, 
                rgba(253, 248, 240, 0.98) 50%,
                rgba(245, 237, 224, 0.97) 100%),
            url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23d4af37' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    }
    
    /* ═══ Hide Streamlit Branding ═══ */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ═══ Main Content Area ═══ */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 850px;
    }
    
    /* ═══ Typography ═══ */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'EB Garamond', 'Palatino Linotype', 'Book Antiqua', Palatino, serif !important;
        color: var(--burgundy-deep) !important;
    }
    
    p, li, span, div {
        font-family: 'Cormorant Garamond', 'Palatino Linotype', Georgia, serif !important;
    }
    
    /* ═══ Header Styling ═══ */
    .padre-header {
        text-align: center;
        padding: 1.5rem 1rem 1rem 1rem;
        margin-bottom: 0.5rem;
        position: relative;
    }
    
    .padre-logo {
        font-family: 'Cinzel', 'EB Garamond', serif;
        font-size: 2.8rem;
        font-weight: 600;
        color: var(--burgundy-deep);
        letter-spacing: 0.08em;
        text-shadow: 1px 1px 0 rgba(201, 162, 39, 0.3);
        margin: 0;
        line-height: 1.2;
    }
    
    .padre-cross {
        color: var(--gold);
        font-size: 2.4rem;
        vertical-align: middle;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.15);
        margin-right: 0.3rem;
    }
    
    .padre-subtitle {
        font-family: 'EB Garamond', serif;
        font-size: 1.15rem;
        color: var(--ink-light);
        font-style: italic;
        margin-top: 0.4rem;
        letter-spacing: 0.02em;
    }
    
    .padre-quote {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1rem;
        color: var(--navy);
        font-style: italic;
        margin-top: 0.8rem;
        padding: 0.5rem 1.5rem;
        border-left: 3px solid var(--gold);
        background: linear-gradient(90deg, rgba(201, 162, 39, 0.08) 0%, transparent 100%);
        display: inline-block;
    }
    
    /* ═══ Decorative Divider ═══ */
    .divider {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 1.5rem 0;
        color: var(--gold);
    }
    
    .divider::before,
    .divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid var(--gold-pale);
    }
    
    .divider::before {
        margin-right: 1rem;
    }
    
    .divider::after {
        margin-left: 1rem;
    }
    
    .divider-icon {
        font-size: 1.2rem;
        color: var(--gold);
    }
    
    /* ═══ Welcome Box ═══ */
    .welcome-box {
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,244,232,0.95) 100%);
        border: 1px solid var(--gold-pale);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0 1.5rem 0;
        box-shadow: 
            0 2px 8px rgba(92, 26, 27, 0.06),
            inset 0 1px 0 rgba(255,255,255,0.8);
    }
    
    .welcome-title {
        font-family: 'EB Garamond', serif !important;
        font-size: 1.4rem !important;
        color: var(--burgundy-deep) !important;
        margin-bottom: 0.8rem !important;
        font-weight: 600 !important;
    }
    
    .welcome-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.1rem;
        color: var(--ink);
        line-height: 1.6;
    }
    
    .welcome-text strong {
        color: var(--burgundy);
        font-weight: 600;
    }
    
    /* ═══ Suggestion Chips ═══ */
    .suggestion-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        margin: 1rem 0;
        justify-content: center;
    }
    
    .suggestion-chip {
        font-family: 'Cormorant Garamond', serif;
        font-size: 0.95rem;
        background: linear-gradient(135deg, var(--cream) 0%, #fff 100%);
        border: 1px solid var(--gold-pale);
        border-radius: 20px;
        padding: 0.5rem 1rem;
        color: var(--ink);
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .suggestion-chip:hover {
        background: linear-gradient(135deg, var(--gold-pale) 0%, var(--cream) 100%);
        border-color: var(--gold);
        transform: translateY(-1px);
        box-shadow: 0 3px 8px rgba(201, 162, 39, 0.2);
    }
    
    /* ═══ Chat Messages ═══ */
    .stChatMessage {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 1.1rem !important;
        line-height: 1.7 !important;
        background-color: rgba(255, 255, 255, 0.7) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(201, 162, 39, 0.15) !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 2px 6px rgba(92, 26, 27, 0.04) !important;
    }
    
    /* Assistant messages */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(253,248,240,0.95) 100%) !important;
        border-left: 3px solid var(--gold) !important;
    }
    
    /* User messages */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: linear-gradient(135deg, rgba(92, 26, 27, 0.03) 0%, rgba(255,255,255,0.8) 100%) !important;
        border-left: 3px solid var(--burgundy-light) !important;
    }
    
    /* ═══ Chat Input ═══ */
    .stChatInput {
        border-radius: 25px !important;
    }
    
    .stChatInput > div {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid var(--gold-pale) !important;
        border-radius: 25px !important;
        box-shadow: 0 2px 12px rgba(201, 162, 39, 0.1) !important;
        transition: all 0.2s ease !important;
    }
    
    .stChatInput > div:focus-within {
        border-color: var(--gold) !important;
        box-shadow: 0 4px 20px rgba(201, 162, 39, 0.2) !important;
    }
    
    .stChatInput input, .stChatInput textarea {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 1.1rem !important;
        color: var(--ink) !important;
    }
    
    .stChatInput input::placeholder, .stChatInput textarea::placeholder {
        color: var(--ink-light) !important;
        font-style: italic !important;
    }
    
    /* ═══ Buttons ═══ */
    .stButton > button {
        font-family: 'EB Garamond', serif !important;
        font-size: 1rem !important;
        background: linear-gradient(135deg, var(--burgundy) 0%, var(--burgundy-deep) 100%) !important;
        color: var(--cream) !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1.2rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 6px rgba(92, 26, 27, 0.2) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--burgundy-light) 0%, var(--burgundy) 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(92, 26, 27, 0.3) !important;
    }
    
    /* ═══ Sidebar ═══ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--parchment) 0%, var(--cream-dark) 100%);
        border-right: 2px solid var(--gold-pale);
    }
    
    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--burgundy-deep) !important;
        font-family: 'EB Garamond', serif !important;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li {
        color: var(--ink) !important;
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 1.05rem !important;
    }
    
    /* ═══ Expander (for citations) ═══ */
    .streamlit-expanderHeader {
        font-family: 'EB Garamond', serif !important;
        font-size: 1rem !important;
        color: var(--navy) !important;
        background: rgba(201, 162, 39, 0.08) !important;
        border-radius: 6px !important;
    }
    
    .streamlit-expanderContent {
        font-family: 'Cormorant Garamond', serif !important;
        background: rgba(255, 255, 255, 0.6) !important;
        border: 1px solid var(--gold-pale) !important;
        border-top: none !important;
        border-radius: 0 0 6px 6px !important;
    }
    
    /* ═══ Spinner ═══ */
    .stSpinner > div {
        border-color: var(--gold) !important;
    }
    
    /* ═══ Disclaimer Footer ═══ */
    .disclaimer {
        text-align: center;
        font-family: 'Cormorant Garamond', serif;
        font-size: 0.9rem;
        color: var(--ink-light);
        font-style: italic;
        padding: 1.5rem 1rem;
        margin-top: 2rem;
        border-top: 1px solid var(--gold-pale);
    }
    
    .disclaimer a {
        color: var(--navy);
        text-decoration: none;
    }
    
    .disclaimer a:hover {
        text-decoration: underline;
    }
    
    /* ═══ Source Citation Box ═══ */
    .citation-box {
        background: linear-gradient(135deg, rgba(30, 58, 95, 0.05) 0%, rgba(255,255,255,0.8) 100%);
        border: 1px solid rgba(30, 58, 95, 0.2);
        border-left: 3px solid var(--navy);
        border-radius: 6px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        font-size: 0.95rem;
    }
    
    .citation-title {
        font-family: 'EB Garamond', serif;
        font-weight: 600;
        color: var(--navy);
    }
    
    /* ═══ About Section Styling ═══ */
    .about-section {
        background: rgba(255,255,255,0.8);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid var(--gold-pale);
    }
    
    .source-list {
        list-style-type: none;
        padding-left: 0;
    }
    
    .source-list li {
        padding: 0.4rem 0;
        padding-left: 1.5rem;
        position: relative;
    }
    
    .source-list li::before {
        content: "📜";
        position: absolute;
        left: 0;
    }
    
    /* ═══ Loading Message ═══ */
    .loading-message {
        font-family: 'Cormorant Garamond', serif;
        font-style: italic;
        color: var(--ink-light);
        text-align: center;
        padding: 1rem;
    }
    
    /* ═══ Mobile Responsiveness ═══ */
    @media (max-width: 768px) {
        .padre-logo {
            font-size: 2rem;
        }
        
        .padre-subtitle {
            font-size: 1rem;
        }
        
        .padre-quote {
            font-size: 0.9rem;
            padding: 0.4rem 1rem;
        }
        
        .suggestion-chip {
            font-size: 0.85rem;
            padding: 0.4rem 0.8rem;
        }
        
        .welcome-box {
            padding: 1rem;
        }
        
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
    
    /* ═══ Tabs Styling ═══ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'EB Garamond', serif !important;
        font-size: 1.1rem !important;
        color: var(--ink) !important;
        background-color: rgba(255,255,255,0.6) !important;
        border: 1px solid var(--gold-pale) !important;
        border-radius: 6px 6px 0 0 !important;
        padding: 0.5rem 1.5rem !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(255,255,255,0.95) !important;
        border-bottom-color: transparent !important;
        color: var(--burgundy-deep) !important;
        font-weight: 600 !important;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        background-color: rgba(255,255,255,0.7);
        border: 1px solid var(--gold-pale);
        border-top: none;
        border-radius: 0 0 8px 8px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# INITIALIZE CLIENT & STATE
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_resource
def get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

client = get_client()
ASSISTANT_ID = os.getenv("ASSISTANT_ID") or os.getenv("OPENAI_ASSISTANT_ID")
FILE_IDS = os.getenv("FILE_IDS", "").split(",") if os.getenv("FILE_IDS") else []

# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def extract_citations(text):
    """
    Extract citation references from the response and format them.
    OpenAI Assistants API uses 【number†source】 format for citations.
    """
    # Pattern to match citation markers like 【4:0†source】
    citation_pattern = r'【(\d+):?\d*†([^】]+)】'
    
    citations = []
    matches = re.findall(citation_pattern, text)
    
    for idx, source in matches:
        citations.append({
            'index': idx,
            'source': source.strip()
        })
    
    # Clean the text by removing or simplifying citation markers
    clean_text = re.sub(citation_pattern, lambda m: f' [{m.group(1)}]', text)
    
    return clean_text, citations

def format_response_with_citations(response_text):
    """Format the response and display any citations in an expandable section."""
    clean_text, citations = extract_citations(response_text)
    
    st.markdown(clean_text)
    
    if citations:
        with st.expander("📚 Sources & References", expanded=False):
            st.markdown("*The following sources were consulted for this response:*")
            unique_sources = list(set(c['source'] for c in citations))
            for source in unique_sources:
                st.markdown(f"""
                <div class="citation-box">
                    <span class="citation-title">📖 {source}</span>
                </div>
                """, unsafe_allow_html=True)

# List of suggestion prompts
SUGGESTIONS = [
    "What are the seven sacraments?",
    "Explain the Holy Trinity",
    "Who was St. Thomas Aquinas?",
    "What is the Immaculate Conception?",
    "How do I pray the Rosary?",
    "What are the works of mercy?",
    "Explain papal infallibility",
    "What is the Real Presence?",
]

LOADING_MESSAGES = [
    "Consulting the sources...",
    "Searching the wisdom of the ages...",
    "Prayerfully considering your question...",
    "Turning to the Fathers of the Church...",
]

import random

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="padre-header">
    <h1 class="padre-logo">
        <span class="padre-cross">☧</span> PADRE GPT
    </h1>
    <p class="padre-subtitle">Your Guide to Catholic Theology & Tradition</p>
    <p class="padre-quote">"In all things, charity." — St. Augustine</p>
</div>
<div class="divider"><span class="divider-icon">✝</span></div>
""", unsafe_allow_html=True)

# Check for assistant ID
if not ASSISTANT_ID:
    st.error("⚠️ Assistant not configured. Please set ASSISTANT_ID or OPENAI_ASSISTANT_ID in environment variables.")
    st.info("Run `python scripts/create_assistant.py` to create the assistant, then update your .env file.")
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN TABS
# ═══════════════════════════════════════════════════════════════════════════════

tab_chat, tab_about = st.tabs(["💬 Ask Padre GPT", "📖 About & Sources"])

with tab_about:
    st.markdown("""
    ### What is Padre GPT?
    
    **Padre GPT** is an AI assistant designed to help you explore and understand 
    Catholic theology, tradition, and spirituality. Drawing from centuries of Church 
    teaching, it provides thoughtful responses grounded in authentic Catholic sources.
    
    ---
    
    ### 📚 Source Library
    
    Padre GPT has access to a rich library of theological texts, including:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Catechetical Works**
        - Catechism of the Catholic Church
        - Catechism of Christian Doctrine (1951)
        - Theology for Beginners — Frank Sheed
        
        **Sacred Scripture**
        - Douay-Rheims Bible (Complete)
        
        **St. Thomas Aquinas**
        - Summa Theologica (Complete)
        - Contra Errores Graecorum
        - How to Study
        """)
    
    with col2:
        st.markdown("""
        **Church Fathers**
        - St. Justin Martyr's Apologies
        - First Seven Ecumenical Councils
        
        **Papal Documents**
        - Papal Encyclicals (1958-1981)
        - Practice of Humility — Leo XIII
        
        **Spiritual Classics**
        - Uniformity with God's Will — St. Alphonsus
        """)
    
    st.markdown("""
    ---
    
    ### ⚠️ Important Disclaimer
    
    While Padre GPT strives for accuracy and fidelity to Church teaching, please remember:
    
    - **This is an AI tool**, not a substitute for authentic Church teaching authority
    - **Always verify** important doctrinal matters with official Church sources
    - **Consult a priest** for spiritual direction and sacramental matters
    - AI can make mistakes or misinterpret complex theological questions
    
    *"The teaching office is not above the word of God, but serves it."* — Dei Verbum
    
    ---
    
    ### 🙏 How to Use
    
    1. **Ask a question** about Catholic faith, doctrine, or spirituality
    2. **Read the response** — sources may be cited for verification
    3. **Explore further** using the suggestion prompts
    4. **Start fresh** anytime using the sidebar's "New Conversation" button
    """)

with tab_chat:
    # Initialize session state
    if "thread_id" not in st.session_state:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "selected_suggestion" not in st.session_state:
        st.session_state.selected_suggestion = None
    
    # Welcome message for new conversations
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div class="welcome-box">
            <h4 class="welcome-title">🕊️ Welcome, Seeker of Truth</h4>
            <p class="welcome-text">
                I am <strong>Padre GPT</strong>, your guide to the rich treasures of Catholic theology and tradition. 
                Drawing from the Summa Theologica, the Church Fathers, papal encyclicals, and more, I'm here to help 
                you explore the depths of our faith.
            </p>
            <p class="welcome-text">
                Ask me about doctrine, the sacraments, the saints, Scripture, or any matter of faith and morals. 
                I'll do my best to provide responses grounded in authentic Catholic teaching.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Suggestion chips
        st.markdown("**Try asking about:**")
        
        # Create clickable buttons for suggestions
        cols = st.columns(4)
        for i, suggestion in enumerate(SUGGESTIONS[:8]):
            with cols[i % 4]:
                if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                    st.session_state.selected_suggestion = suggestion
                    st.rerun()
    
    # Display chat messages
    for message in st.session_state.messages:
        avatar = "🙏" if message["role"] == "assistant" else "👤"
        with st.chat_message(message["role"], avatar=avatar):
            if message["role"] == "assistant":
                format_response_with_citations(message["content"])
            else:
                st.markdown(message["content"])
    
    # Handle suggestion click
    if st.session_state.selected_suggestion:
        prompt = st.session_state.selected_suggestion
        st.session_state.selected_suggestion = None
    else:
        prompt = st.chat_input("What would you like to know about the Catholic faith?")
    
    # Chat input handling
    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Send to assistant
        with st.chat_message("assistant", avatar="🙏"):
            loading_msg = random.choice(LOADING_MESSAGES)
            with st.spinner(loading_msg):
                try:
                    # Add message to thread with file attachments
                    attachments = [
                        {"file_id": fid.strip(), "tools": [{"type": "file_search"}]} 
                        for fid in FILE_IDS if fid and fid.strip()
                    ]
                    
                    client.beta.threads.messages.create(
                        thread_id=st.session_state.thread_id,
                        role="user",
                        content=prompt,
                        attachments=attachments if attachments else None
                    )
                    
                    # Run the assistant
                    run = client.beta.threads.runs.create_and_poll(
                        thread_id=st.session_state.thread_id,
                        assistant_id=ASSISTANT_ID
                    )
                    
                    # Get the response
                    if run.status == "completed":
                        messages = client.beta.threads.messages.list(
                            thread_id=st.session_state.thread_id
                        )
                        # Get the latest assistant message
                        response = ""
                        for msg in messages.data:
                            if msg.role == "assistant":
                                for content in msg.content:
                                    if hasattr(content, 'text'):
                                        response = content.text.value
                                        break
                                break
                        
                        format_response_with_citations(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    else:
                        st.error(f"I apologize, but I encountered an issue: {run.status}")
                        if hasattr(run, 'last_error') and run.last_error:
                            st.caption(f"Details: {run.last_error.message}")
                            
                except Exception as e:
                    st.error("I apologize, but something went wrong. Please try again.")
                    st.caption(f"Error: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <span style="font-size: 3rem;">☧</span>
        <h2 style="font-family: 'Cinzel', serif; margin: 0.5rem 0;">Padre GPT</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🔄 New Conversation", use_container_width=True):
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📖 Quick Topics")
    quick_topics = [
        "The Eucharist",
        "Mary & the Saints",
        "Prayer & Devotions",
        "Moral Theology",
        "Church History",
        "Scripture Study"
    ]
    
    for topic in quick_topics:
        if st.button(f"📌 {topic}", key=f"topic_{topic}", use_container_width=True):
            st.session_state.selected_suggestion = f"Tell me about {topic.lower()} in Catholic teaching"
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; font-style: italic; color: #5C1A1B; font-family: 'EB Garamond', serif;">
        <p>✝️</p>
        <p style="font-size: 0.95rem;">Ad Majorem<br/>Dei Gloriam</p>
        <p style="font-size: 0.8rem; color: #666; margin-top: 1rem;">
            For the Greater Glory of God
        </p>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER DISCLAIMER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="disclaimer">
    <p>✝️ Built with faith and code</p>
    <p>This AI assistant is not a substitute for the Magisterium, spiritual direction, or the sacraments.<br/>
    Always consult official Church teaching for matters of doctrine and faith.</p>
</div>
""", unsafe_allow_html=True)
