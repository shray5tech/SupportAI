import streamlit as st
from rag_engine import initialize_bot

# Page config
st.set_page_config(
    page_title="SupportAI",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for chat bubbles
st.markdown("""
    <style>
    .user-bubble {
        background-color: #0084ff;
        color: white;
        padding: 10px 15px;
        border-radius: 18px 18px 4px 18px;
        margin: 5px 0;
        max-width: 75%;
        margin-left: auto;
        text-align: right;
    }
    .bot-bubble {
        background-color: #f0f0f0;
        color: #111;
        padding: 10px 15px;
        border-radius: 18px 18px 18px 4px;
        margin: 5px 0;
        max-width: 75%;
        margin-right: auto;
    }
    .chat-container {
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ─── PASSWORD PROTECTION ───────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🤖 SupportAI")
    st.subheader("Please enter the access code to continue")
    password = st.text_input("Access Code:", type="password")
    if st.button("Enter"):
        if password == "nexus2026":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect access code. Please try again.")
    st.stop()
# ───────────────────────────────────────────────────────────────────

# Header
st.title("🤖 SupportAI")
st.caption("AI-powered customer support agent | Nexus Financial Services")
st.divider()

# Initialize bot (only once per session)
if "chain" not in st.session_state:
    with st.spinner("Loading SupportAI knowledge base..."):
        st.session_state.chain = initialize_bot()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hi! I'm SupportAI, your virtual support assistant for Nexus Financial Services. I can help you with account management, billing, payments, rewards, card services, and technical issues. How can I help you today?"}
    ]

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-container"><div class="user-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-container"><div class="bot-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-container"><div class="user-bubble">{prompt}</div></div>', unsafe_allow_html=True)

    with st.spinner("Thinking..."):
        try:
            response = st.session_state.chain.invoke({"question": prompt})
            answer = response["answer"]
        except Exception as e:
            answer = "I'm having trouble connecting right now. Please try again in a moment."

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.markdown(f'<div class="chat-container"><div class="bot-bubble">{answer}</div></div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📋 What I Can Help With")
    st.markdown("""
    - 🔐 **Account Management** — passwords, contact info, locked accounts
    - 💳 **Billing & Payments** — disputes, late fees, AutoPay setup
    - 🎁 **Rewards** — redeem points, missing points, earn rates
    - 💳 **Card Services** — lost/stolen cards, credit limit, freeze card
    - 🛠️ **Technical Issues** — app problems, OTP issues, 2FA setup
    - 🧑‍💼 **Escalation** — speak to a human agent
    """)
    st.divider()
    st.caption("Built with LangChain + ChromaDB + Gemini 2.5 Flash")
    st.caption("by Shray Bisht | [GitHub](https://github.com/shray5tech)")

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Hi! I'm SupportAI. How can I help you today?"}
        ]
        st.session_state.chain = initialize_bot()
        st.rerun()
