import streamlit as st
import openai
import csv
import os
from datetime import datetime

st.set_page_config(page_title="ComplyAI", page_icon="🛡️", layout="centered")

st.markdown(
    '''
    <style>
    .stApp { background: linear-gradient(135deg,#f8fafc 0%, #eef2ff 100%); }
    .hero { padding:18px; border-radius:12px; background:linear-gradient(90deg,rgba(99,102,241,0.06), rgba(20,184,166,0.04)); }
    .card { background: white; padding:16px; border-radius:12px; box-shadow: 0 6px 24px rgba(12,15,20,0.04); }
    .muted { color:#6b7280; font-size:13px; }
    .footer { color:#9ca3af; font-size:12px; }
    </style>
    ''', unsafe_allow_html=True
)

col1, col2 = st.columns([3,1])
with col1:
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.markdown("### 🛡️ ComplyAI — AI-Powered Compliance Copilot for Startups")
    st.markdown("Get tailored SOC 2 / ISO 27001 / GDPR checklists and guidance.")
    st.markdown("</div>", unsafe_allow_html=True)
with col2:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=96)
    else:
        st.markdown("**Add logo.png to project root**", unsafe_allow_html=True)

st.write("")

with st.container():
    left, right = st.columns([2,3])
    with left:
        st.markdown("### Input")
        framework = st.selectbox("Framework", ["SOC 2", "ISO 27001", "GDPR"])
        company_size = st.text_input("Company size", value="15")
        cloud = st.selectbox("Cloud provider", ["AWS", "Azure", "GCP", "Other"])
        tech_stack = st.text_area("Tech stack", value="Python, React, PostgreSQL")
        primary_goal = st.selectbox("Primary goal", ["Readiness checklist", "Policy drafts", "Risk prioritization"])
        generate = st.button("Generate recommendations")
        st.markdown('<div class="muted">Tip: keep tech stack short for better output.</div>', unsafe_allow_html=True)
    with right:
        st.markdown("### Output")
        output_box = st.empty()
        output_box.info("Generated recommendations will appear here.")

def build_prompt(framework, company_size, cloud, tech_stack, primary_goal):
    return f'''
You are a pragmatic cybersecurity compliance assistant.
Produce a clear, startup-focused result for: {framework}.
Company size: {company_size} employees.
Cloud: {cloud}
Tech stack: {tech_stack}
Deliverable: {primary_goal}
Format:
- Short executive summary (2 lines)
- Bullet checklist with prioritized next steps
- Example security policy titles (3 items) with 1-line descriptions
'''

if generate:
    api_key = st.secrets.get("OPENAI_API_KEY") if st.secrets else os.environ.get("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key missing. Add OPENAI_API_KEY to .streamlit/secrets.toml or as env var.")
    else:
        openai.api_key = api_key
        prompt = build_prompt(framework, company_size, cloud, tech_stack, primary_goal)
        with st.spinner("Generating..."):
            try:
                resp = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful cybersecurity compliance assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.35,
                    max_tokens=900
                )
                text = resp["choices"][0]["message"]["content"].strip()
                output_box.markdown(text)
                st.download_button("📥 Download (TXT)", data=text, file_name=f"ComplyAI_{framework}.txt")
            except Exception as e:
                st.error(f"AI request failed: {e}")

st.markdown("---")
st.markdown("### Join early access")
with st.form("waitlist_form"):
    wl_email = st.text_input("Work email")
    wl_company = st.text_input("Company (optional)")
    wl_role = st.text_input("Role (optional)")
    wl_submit = st.form_submit_button("Join waitlist")
    if wl_submit:
        if not wl_email:
            st.warning("Enter an email.")
        else:
            os.makedirs("data", exist_ok=True)
            path = os.path.join("data", "waitlist.csv")
            first_write = not os.path.exists(path)
            with open(path, "a", newline="") as f:
                writer = csv.writer(f)
                if first_write:
                    writer.writerow(["email","company","role","timestamp"])
                writer.writerow([wl_email, wl_company, wl_role, datetime.utcnow().isoformat()])
            st.success("Added to waitlist!")

st.markdown("---")
st.markdown('<div class="footer">ComplyAI — Founder: Naveen • Prototype Demo</div>', unsafe_allow_html=True)
