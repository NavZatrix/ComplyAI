import streamlit as st
import pandas as pd
from datetime import datetime
from openai import OpenAI

# ---------- PAGE SETUP ----------
st.set_page_config(
    page_title="ComplyAI - AI Compliance Copilot for Startups",
    page_icon="logo.png",
    layout="centered",
)

# ---------- CUSTOM CSS ----------
st.markdown(
    """
    <style>
        /* Background gradient */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(180deg, #f5f7fa 0%, #e4ecf7 100%);
        }

        /* Center the main content */
        .main {
            text-align: center;
        }

        /* Titles and subtitles */
        h1 {
            font-size: 48px;
            color: #0E1117;
            margin-bottom: 0;
        }

        h3, h2 {
            color: #1E293B;
        }

        p {
            color: #475569;
            font-size: 17px;
        }

        /* Custom button */
        div.stButton > button:first-child {
            background: linear-gradient(90deg, #2563EB, #1E40AF);
            color: white;
            border-radius: 10px;
            height: 3em;
            width: 50%;
            border: none;
            font-size: 16px;
            font-weight: 500;
            transition: 0.3s;
        }

        div.stButton > button:first-child:hover {
            background: linear-gradient(90deg, #1D4ED8, #1E3A8A);
            transform: scale(1.02);
        }

        /* Card-style sections */
        .feature-card {
            background-color: white;
            border-radius: 16px;
            box-shadow: 0px 3px 8px rgba(0,0,0,0.05);
            padding: 20px;
            margin-bottom: 20px;
        }

        footer {
            text-align: center;
            color: gray;
            font-size: 14px;
            margin-top: 2em;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- HEADER ----------
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.image("logo.png", width=120)

st.markdown(
    """
    <h1>ComplyAI</h1>
    <p><b>Your AI-Powered Compliance Copilot for Startups 🚀</b></p>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr>", unsafe_allow_html=True)

# ---------- FEATURE SECTION ----------
st.markdown("<h2>✨ What ComplyAI Does</h2>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="feature-card">
        <p>✅ Helps startups get <b>SOC 2</b> and <b>ISO 27001</b> ready fast</p>
        <p>✅ Generates <b>custom policy templates</b> instantly</p>
        <p>✅ Offers <b>AI-based compliance guidance</b> in plain English</p>
        <p>✅ Tracks <b>controls, documentation, and evidence</b> automatically</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- AI ASSISTANT ----------
st.markdown("<h2>💬 Try ComplyAI in Action</h2>", unsafe_allow_html=True)
user_question = st.text_input("Ask your compliance question:")

if st.button("Get AI Guidance"):
    if not user_question:
        st.warning("Please enter a question.")
    else:
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are ComplyAI, an expert in SOC 2, ISO 27001, and compliance automation. "
                            "Answer clearly, professionally, and make it easy for startup founders to understand."
                        ),
                    },
                    {"role": "user", "content": user_question},
                ],
            )
            ai_reply = response.choices[0].message.content
            st.markdown(
                f"<div class='feature-card'><b>ComplyAI:</b><br>{ai_reply}</div>",
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.error(f"AI request failed:\n\n{e}")

# ---------- WAITLIST SIGNUP ----------
st.markdown("<h2>📝 Join the Waitlist</h2>", unsafe_allow_html=True)
st.markdown("Get early access when we launch ComplyAI!")

with st.form("waitlist_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    company = st.text_input("Company Name (optional)")
    submitted = st.form_submit_button("Join Waitlist")

    if submitted:
        if not email:
            st.error("Please enter your email.")
        else:
            entry = pd.DataFrame(
                [[name, email, company, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]],
                columns=["Name", "Email", "Company", "Timestamp"],
            )
            try:
                entry.to_csv("data/waitlist.csv", mode="a", header=False, index=False)
            except:
                entry.to_csv("waitlist.csv", mode="a", header=False, index=False)
            st.success("✅ You're on the waitlist! We'll notify you soon.")

# ---------- FOOTER ----------
st.markdown(
    """
    <footer>© 2025 ComplyAI Inc. | Built with ❤️ by <b>Naveen</b></footer>
    """,
    unsafe_allow_html=True,
)
