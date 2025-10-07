import streamlit as st
from openai import OpenAI

# --- Setup ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.set_page_config(page_title="ComplyAI | AI Compliance Copilot", page_icon="💡", layout="wide")

# --- Custom Styles ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background: radial-gradient(circle at 10% 20%, #0f172a 0%, #1e293b 50%, #334155 100%);
        color: #f8fafc;
    }
    .main-container {
        text-align: center;
        padding: 5rem 1rem 2rem;
    }
    .logo {
        width: 100px;
        margin-bottom: 1rem;
    }
    h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    h2 {
        font-size: 1.3rem;
        font-weight: 400;
        color: #cbd5e1;
        margin-bottom: 2.5rem;
    }
    .cta-button {
        background: linear-gradient(90deg, #3b82f6, #2563eb);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.9rem 1.8rem;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .cta-button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #2563eb, #1d4ed8);
    }
    .section {
        padding: 4rem 1rem;
        max-width: 1100px;
        margin: auto;
        text-align: center;
    }
    .card-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 2rem;
        margin-top: 2rem;
    }
    .card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        width: 300px;
        padding: 1.8rem;
        text-align: left;
        transition: transform 0.25s ease;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }
    .card:hover {
        transform: translateY(-6px);
    }
    .chat-section {
        margin-top: 4rem;
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        padding: 2.5rem;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        box-shadow: 0 0 40px rgba(0,0,0,0.3);
    }
    .chat-box {
        background: rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1.2rem;
        margin-top: 1.2rem;
        text-align: left;
        line-height: 1.6;
    }
    footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.9em;
        margin-top: 6rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.image("logo.png", width=100)
st.markdown("<h1>ComplyAI</h1>", unsafe_allow_html=True)
st.markdown("<h2>Your AI-powered Compliance Partner for SOC 2, ISO 27001 & GDPR</h2>", unsafe_allow_html=True)
if st.button("🚀 Try the Demo", key="demo", use_container_width=False):
    st.session_state["show_demo"] = True
st.markdown("</div>", unsafe_allow_html=True)

# --- HOW IT WORKS SECTION ---
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.markdown("<h2>How It Works</h2>", unsafe_allow_html=True)

st.markdown("""
<div class='card-container'>
    <div class='card'>
        <h3>1️⃣ Ask Anything</h3>
        <p>Type your compliance or security question. ComplyAI understands context, frameworks, and policies.</p>
    </div>
    <div class='card'>
        <h3>2️⃣ Instant Expert Insights</h3>
        <p>Receive compliance-grade guidance on SOC 2, ISO 27001, risk management, and privacy obligations.</p>
    </div>
    <div class='card'>
        <h3>3️⃣ Strengthen Your Posture</h3>
        <p>Get tailored recommendations to help your startup stay audit-ready and secure.</p>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- DEMO SECTION ---
if st.session_state.get("show_demo", False):
    st.markdown("<div class='chat-section'>", unsafe_allow_html=True)
    st.markdown("<h2>💬 Chat with ComplyAI</h2>", unsafe_allow_html=True)
    
    query = st.text_input("Ask your question about compliance, security, or frameworks:")
    if st.button("Ask", key="chat"):
        if query.strip():
            with st.spinner("ComplyAI is analyzing your query..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are ComplyAI, a compliance expert specialized in SOC 2, ISO 27001, GDPR, and NIST CSF for startups."},
                            {"role": "user", "content": query},
                        ],
                    )
                    answer = response.choices[0].message.content
                    st.markdown(f"<div class='chat-box'>{answer}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"⚠️ Error: {e}")
        else:
            st.warning("Please type your question first.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<footer>© 2025 ComplyAI | Built with ❤️ using Streamlit</footer>", unsafe_allow_html=True)
