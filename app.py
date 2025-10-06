import streamlit as st
import openai
import csv
import os
from datetime import datetime

st.set_page_config(page_title="ComplyAI", page_icon="🛡️", layout="wide")

# CSS for modern look
st.markdown("""
<style>
body {
    background: #f9fafb;
    color: #111827;
    font-family: 'Inter', sans-serif;
}
.hero {
    padding: 60px 30px;
    background: linear-gradient(90deg, #6366f1, #10b981);
    color: white;
    border-radius: 12px;
    text-align: center;
}
.card {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.08);
    margin: 10px;
}
.features h3 {
    margin-bottom: 5px;
    color: #111827;
}
.footer {
    text-align: center;
    color: #6b7280;
    font-size: 13px;
    padding: 20px;
}
.button-primary {
    background-color: #6366f1;
    color: white;
    padding: 12px 25px;
    border-radius: 8px;
    text-decoration: none;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown('<div class="hero"><h1>ComplyAI</h1><p>AI-Powered Compliance Copilot for Startups</p></div>', unsafe_allow_html=True)

# Features section
st.markdown("### Why ComplyAI")
cols = st.columns(3)
features = [
    ("✅ Fast SOC 2 Readiness", "Get an actionable checklist in minutes."),
    ("📄 Policy Drafts", "Generate professional policy templates instantly."),
    ("🔍 Risk Prioritization", "Identify and prioritize your top compliance risks."),
]
for col, (title, desc) in zip(cols, features):
    col.markdown(f'<div class="card"><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)

st.markdown("---")

# Input + Output Section
st.markdown("### Generate Compliance Recommendations")
left, right = st.columns([2,3])
with left:
    framework = st.selectbox("Framework", ["SOC 2", "ISO 27001", "GDPR"])
    company_size = st.text_input("Company size", value="15")
    cloud = st.selectbox("Cloud provider", ["AWS", "Azure", "GCP", "Other"])
    tech_stack = st.text_area("Tech stack", value="Python, React, PostgreSQL")
    primary_goal = st.selectbox("Primary goal", ["Readiness checklist", "Policy drafts", "Risk prioritization"])
    generate = st.button("Generate Recommendations")
with right:
    output_box = st.empty()
    output_box.info("Your AI-generated recommendations will appear here.")

# AI generation function
def build_prompt(framework, company_size, cloud, tech_stack, primary_goal):
    return f"""
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
"""

if generate:
    api_key = st.secrets.get("OPENAI_API_KEY") if st.secrets else os.environ.get("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key missing. Add OPENAI_API_KEY to .streamlit/secrets.toml or as env var.")
    else:
        openai.api_key = api_key
        prompt = build_prompt(framework, company_size, cloud, tech_stack, primary_goal)
        with st.spinner("Generating recommendations..."):
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
# Waitlist CTA
st.markdown("### Join Early Access")
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

# Footer
st.markdown('<div class="footer">ComplyAI — Founder: Naveen • Prototype Demo</div>', unsafe_allow_html=True)

