import streamlit as st
import pandas as pd
from datetime import datetime
from openai import OpenAI

# ---------- PAGE SETUP ----------
st.set_page_config(
    page_title="ComplyAI - Compliance Copilot for Startups",
    page_icon="logo.png",
    layout="centered",
)

# ---------- HEADER ----------
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.image("logo.png", width=150)
st.markdown(
    """
    <h1 style='text-align: center; color: #0E1117;'>ComplyAI</h1>
    <p style='text-align: center; font-size: 18px; color: #555;'>Your AI-Powered Compliance Copilot for Startups 🚀</p>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# ---------- FEATURE SECTION ----------
st.subheader("✨ What ComplyAI Does")
st.markdown(
    """
    - Helps startups get **SOC 2** and **ISO 27001** ready in record time  
    - Generates **custom security policy templates** in seconds  
    - Offers **AI-based compliance guidance** for founders and small teams  
    - Keeps track of controls, documentation, and evidence automatically  
    """
)

st.markdown("---")

# ---------- AI ASSISTANT ----------
st.subheader("💬 Try ComplyAI in Action")

user_question = st.text_input("Ask me about compliance, security, or audit readiness:")

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
                            "You are ComplyAI, a friendly AI compliance expert. "
                            "You help startups understand SOC 2, ISO 27001, GDPR, and related security frameworks. "
                            "Be concise, confident, and explain in plain English."
                        ),
                    },
                    {"role": "user", "content": user_question},
                ],
            )
            ai_reply = response.choices[0].message.content
            st.success(ai_reply)
        except Exception as e:
            st.error(f"AI request failed:\n\n{e}")

st.markdown("---")

# ---------- WAITLIST SIGNUP ----------
st.subheader("📝 Join the Waitlist")
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
                # Save to data/waitlist.csv
                entry.to_csv("data/waitlist.csv", mode="a", header=False, index=False)
            except:
                entry.to_csv("waitlist.csv", mode="a", header=False, index=False)

            st.success("✅ You're on the waitlist! We'll notify you soon.")

st.markdown("---")

# ---------- FOOTER ----------
st.markdown(
    """
    <p style='text-align: center; font-size: 15px; color: gray;'>
    © 2025 ComplyAI Inc. Built with ❤️ by <b>Naveen</b>
    </p>
    """,
    unsafe_allow_html=True,
)
