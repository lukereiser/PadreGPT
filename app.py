"""
Padre GPT - Catholic Theology Assistant
A Streamlit web interface for the Padre GPT Assistant.
"""

import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Padre GPT",
    page_icon="✝️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for a more reverent aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;600&family=Inter:wght@400;500&display=swap');
    
    .stApp {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    h1 {
        font-family: 'Crimson Pro', serif !important;
        color: #d4af37 !important;
        text-align: center;
        font-size: 3rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        font-family: 'Crimson Pro', serif;
        color: #c9b896;
        text-align: center;
        font-size: 1.2rem;
        font-style: italic;
        margin-bottom: 2rem;
    }
    
    .stChatMessage {
        background-color: rgba(255,255,255,0.05) !important;
        border-radius: 10px;
        border: 1px solid rgba(212, 175, 55, 0.2);
    }
    
    .stChatInputContainer {
        border-color: #d4af37 !important;
    }
    
    .stSpinner > div {
        border-color: #d4af37 !important;
    }
    
    /* Chat input styling */
    .stChatInput input {
        background-color: rgba(255,255,255,0.1) !important;
        color: white !important;
    }
    
    .footer {
        position: fixed;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        color: rgba(255,255,255,0.3);
        font-size: 0.8rem;
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI client
@st.cache_resource
def get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

client = get_client()
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
FILE_IDS = os.getenv("FILE_IDS", "").split(",") if os.getenv("FILE_IDS") else []

# Header
st.markdown("# ✝️ Padre GPT")
st.markdown('<p class="subtitle">"In all things, charity" — St. Augustine</p>', unsafe_allow_html=True)

# Check for assistant ID
if not ASSISTANT_ID:
    st.error("⚠️ Assistant not configured. Please run `python scripts/create_assistant.py` first.")
    st.stop()

# Initialize session state
if "thread_id" not in st.session_state:
    # Create thread with file attachments
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🙏" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about Catholic theology..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # Send to assistant
    with st.chat_message("assistant", avatar="🙏"):
        with st.spinner("Consulting the sources..."):
            # Add message to thread with file attachments
            attachments = [{"file_id": fid, "tools": [{"type": "file_search"}]} for fid in FILE_IDS if fid]
            
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
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                st.error(f"Error: {run.status}")

# Sidebar
with st.sidebar:
    st.markdown("### 📚 About")
    st.markdown("""
    **Padre GPT** is a Catholic theology assistant powered by AI and grounded in authentic Catholic sources.
    
    **Knowledge Base includes:**
    - Theology for Beginners (Frank Sheed)
    - Catechism of Christian Doctrine
    - Works of St. Thomas Aquinas
    - Papal Encyclicals
    - Church Fathers
    - Ecumenical Councils
    """)
    
    st.markdown("---")
    
    if st.button("🔄 New Conversation"):
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("*Ad Majorem Dei Gloriam*")

# Footer
st.markdown('<p class="footer">Built with faith and code • Not a substitute for spiritual direction</p>', unsafe_allow_html=True)
