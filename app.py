import streamlit as st
from openai import OpenAI, APIError, RateLimitError, AuthenticationError

# --- Page config ---
st.set_page_config(
    page_title="Compliance Copilot",
    page_icon="⚖️",
    layout="wide",
)

# --- Custom CSS for modern UI ---
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #f7f9fb 0%, #eef2f5 100%);
            font-family: 'Inter', sans-serif;
            color: #1e1e1e;
        }
        .main {
            max-width: 900px;
            margin: 0 auto;
            padding: 3rem 2rem;
            background-color: white;
            border-radius: 18px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.05);
        }
        h1 {
            text-align: center;
            color: #1e1e1e;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        h3 {
            text-align: center;
            color: #6b7280;
            font-weight: 400;
            margin-bottom: 2rem;
        }
        textarea {
            border-radius: 12px !important;
        }
        button[kind="primary"] {
            background-color: #2563eb !important;
            color: white !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.2rem !important;
        }
        .footer {
            text-align: center;
            color: #6b7280;
            font-size: 0.9rem;
            margin-top: 3rem;
        }
        .logo {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 90px;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Logo and Header ---
st.markdown('<img src="app_logo.png" class="logo">', unsafe_allow_html=True)
st.title("AI Compliance Copilot ⚖️")
st.markdown("<h3>Your AI assistant for startup compliance and security</h3>", unsafe_allow_html=True)

# --- Initialize OpenAI client ---
try:
    client = OpenAI(api_key=st.secrets["general"]["OPENAI_API_KEY"])
except Exception:
    client = None
    st.error("⚠️ Missing or invalid OpenAI API key. Please check your secrets.toml file.")

# --- Input Area ---
st.markdown("### 💬 Ask your compliance question below")
user_input = st.text_area("Example: *What are GDPR requirements for storing customer data?*", height=130)

# --- Generate Answer ---
if st.button("Ask Copilot"):
    if not user_input.strip():
        st.warning("Please enter a question before submitting.")
    elif not client:
        st.error("⚠️ Could not initialize OpenAI client. Check your API key setup.")
    else:
        try:
            with st.spinner("Analyzing compliance data..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an expert compliance assistant for startups."},
                        {"role": "user", "content": user_input}
                    ],
                )
            answer = response.choices[0].message.content
            st.success("✅ Here’s what I found:")
            st.markdown(f"<div style='padding: 1rem; background: #f9fafb; border-radius: 12px;'>{answer}</div>", unsafe_allow_html=True)

        except RateLimitError:
            st.error("⚠️ You’ve run out of OpenAI credits. Please check your billing or update your API key.")
        except AuthenticationError:
            st.error("🔑 Invalid or missing API key. Please update your `.streamlit/secrets.toml` file.")
        except APIError as e:
            st.error(f"🚨 API Error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

# --- Footer ---
st.markdown("<div class='footer'>Made with ❤️ by Nav | Powered by OpenAI</div>", unsafe_allow_html=True)
