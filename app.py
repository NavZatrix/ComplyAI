import streamlit as st
from openai import OpenAI, APIError, RateLimitError, AuthenticationError

# --- Page setup ---
st.set_page_config(page_title="Compliance Copilot", page_icon="⚖️", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Poppins:wght@500&display=swap');

        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
        }
        .main {
            padding: 0 !important;
        }
        .hero {
            text-align: center;
            padding-top: 4rem;
            padding-bottom: 2rem;
        }
        .hero img {
            width: 90px;
            margin-bottom: 1rem;
        }
        .hero h1 {
            font-family: 'Poppins', sans-serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: #111827;
            margin-bottom: 0.5rem;
        }
        .hero p {
            font-size: 1.1rem;
            color: #4b5563;
        }
        .chat-box {
            background: white;
            box-shadow: 0 8px 30px rgba(0,0,0,0.08);
            border-radius: 16px;
            padding: 2rem;
            width: 90%;
            max-width: 720px;
            margin: 2rem auto;
        }
        textarea {
            border-radius: 12px !important;
            border: 1px solid #e5e7eb !important;
            font-size: 1rem !important;
        }
        .stButton > button {
            background-color: #2563eb !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.4rem !important;
            font-size: 1rem !important;
        }
        .response-box {
            background: #f9fafb;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            margin-top: 1rem;
            border-left: 4px solid #2563eb;
        }
        .footer {
            text-align: center;
            color: #6b7280;
            font-size: 0.9rem;
            margin-top: 3rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="hero">
    <img src="app_logo.png" alt="Logo">
    <h1>Compliance Copilot ⚖️</h1>
    <p>Your AI-powered assistant for startup compliance and security tasks.</p>
</div>
""", unsafe_allow_html=True)

# --- Chat UI Box ---
st.markdown('<div class="chat-box">', unsafe_allow_html=True)

st.markdown("### 💬 Ask your compliance question")
user_input = st.text_area("Example: What are SOC 2 requirements for a SaaS company?", height=130)

client = None
try:
    client = OpenAI(api_key=st.secrets["general"]["OPENAI_API_KEY"])
except Exception:
    st.warning("⚠️ Missing or invalid OpenAI API key. Please check your `.streamlit/secrets.toml` file.")

if st.button("Ask Copilot"):
    if not user_input.strip():
        st.warning("Please enter a question before submitting.")
    elif not client:
        st.error("⚠️ Could not initialize OpenAI client. Check your API key setup.")
    else:
        try:
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an expert in startup compliance, cybersecurity, and privacy laws."},
                        {"role": "user", "content": user_input}
                    ],
                )
            answer = response.choices[0].message.content
            st.markdown(f"<div class='response-box'>{answer}</div>", unsafe_allow_html=True)
        except RateLimitError:
            st.error("⚠️ You’ve exceeded your OpenAI quota. Please check billing or use a new key.")
        except AuthenticationError:
            st.error("🔑 Invalid API key. Update your secrets.toml file.")
        except APIError as e:
            st.error(f"🚨 API Error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div class="footer">
    Built by <b>Nav</b> · Powered by <b>OpenAI</b> · © 2025 Compliance Copilot
</div>
""", unsafe_allow_html=True)
