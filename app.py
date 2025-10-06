import streamlit as st
import openai
import csv
import os
from datetime import datetime
from PIL import Image

st.set_page_config(page_title="ComplyAI", page_icon="🛡️", layout="wide")

# --- CSS for styling ---
st.markdown("""
<style>
body { background: #f9fafb; font-family: 'Inter', sans-serif; color: #111827; }
.navbar { width: 100%; background: white; padding: 12px 50px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); position: sticky; top: 0; z-index: 999; display: flex; align-items: center; justify-content: space-between; }
.navbar a { color: #111827; margin-left: 25px; text-decoration: none; font-weight: 600; }
.navbar a:hover { color: #6366f1; }
.nav-logo { display: flex; align-items: center; }
.nav-logo img { height: 40px; margin-right: 12px; }
.hero { padding: 80px 30px; background: linear-gradient(90deg,#6366f1,#10b981); color: white; border-radius: 12px; text-align: center; margin-top:20px; }
.hero h1 { font-size: 48px; margin-bottom: 10px; }
.hero p { font-size: 20px; margin-bottom: 25px; }
.button-primary { background-color: #ffffff; color: #6366f1; padding: 14px 28px; border-radius: 10px; font-weight: bold; text-decoration: none; }
.features h3 { margin-bottom: 5px; color: #111827; }
.card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 6px 24px rgba(0,0,0,0.08); margin: 10px; text-align: center; }
.section-title { text-align: center; padding-top: 60px; padding-bottom: 20px; font-size: 32px; font-weight: bold; }
.footer { text-align: center; color: #6b7280; font-size: 13px; padding: 30px; }
.card img { border-radius: 12px; box-shadow: 0 6px 24px rgba(0,0,0,0.08); margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# --- Navbar ---
st.markdown(f"""
<div class="navbar">
    <div class="nav-logo">
        <img src="logo.png" alt="ComplyAI Logo">
        <span style="font-weight:bold; font-size:20px;">ComplyAI</span>
    </div>
    <div class="nav-links">
        <a href="#demo">Demo</a>
        <a href="#features">Features</a>
        <a href="#product-preview">Product</a>
        <a href="#testimonials">Testimonials</a>
        <a href="#waitlist">Waitlist</a>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar Logo ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=120)
st.sidebar.title("ComplyAI")

# --- Hero Section ---
if os.path.exists("logo.png"):
    logo = Image.open("logo.png")
    st.image(logo, width=120)

st.markdown(
    '<div class="hero"><h1>ComplyAI</h1><p>AI-Powered Compliance Copilot for Startups</p><a class="button-primary" href="#demo">Try Demo →</a></div>',
    unsafe_allow_html=True
)

# --- Features Section ---
st.markdown('<div class="section-title" id="features">Why ComplyAI?</div>', unsafe_allow_html=True)
cols = st.columns(3)
features = [
    ("🚀 Fast SOC 2 Readiness", "Get an actionable checklist in minutes."),
    ("📄 Policy Drafts", "Generate professional policy templates instantly."),
    ("🔍 Risk Prioritization", "Identify and prioritize your top compliance risks."),
]
for col, (title, desc) in zip(cols, features):
    col.markdown(f'<div class="card"><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)

st.markdown("---")

# --- Demo Section ---
st.markdown('<div class="section-title" id="demo">Live Demo</div>', unsafe_allow_html=True)
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

def build_prompt(framework, company_size, cloud, primary_goal):
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
        st.error("OpenAI API key missing. Add OPENAI_API_KEY to .streamlit/secrets.toml or env var.")
    else:
        openai.api_key = api_key
        prompt = build_prompt(framework, company_size, cloud, primary_goal)
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

# --- Product Preview Section ---
st.markdown('<div class="section-title" id="product-preview">Product Preview</div>', unsafe_allow_html=True)
st.markdown("Explore the ComplyAI dashboard and see how recommendations are presented:")
cols = st.columns(2)
mock_dashboard_path = "assets/dashboard_mock.png"
feature1_path = "assets/feature1.png"

if os.path.exists(mock_dashboard_path):
    cols[0].image(mock_dashboard_path, caption="Dashboard Overview", use_column_width=True)
else:
    cols[0].markdown('<div class="card"><p>[Add dashboard_mock.png in assets/ folder]</p></div>', unsafe_allow_html=True)

if os.path.exists(feature1_path):
    cols[1].image(feature1_path, caption="Feature Example", use_column_width=True)
else:
    cols[1].markdown('<div class="card"><p>[Add feature1.png in assets/ folder]</p></div>', unsafe_allow_html=True)

st.markdown("---")

# --- Testimonials Section ---
st.markdown('<div class="section-title" id="testimonials">What Users Say</div>', unsafe_allow_html=True)
cols = st.columns(3)
testimonials = [
    ("Alice, CTO", "ComplyAI saved us weeks of compliance work!"),
    ("Bob, Founder", "Finally a tool that understands startup compliance."),
    ("Carol, Security Lead", "The AI suggestions are actionable and clear."),
]
for col, (name, feedback) in zip(cols, testimonials):
    col.markdown(f'<div class="card"><p>"{feedback}"</p><b>{name}</b></div>', unsafe_allow_html=True)

st.markdown("---")

# --- Waitlist Section ---
st.markdown('<div class="section-title" id="waitlist">Join Early Access</div>', unsafe_allow_html=True)
with st.form("waitlist_form"):
    wl_email = st.text_input("Work email")
    wl_company = st.text_input("Company (optional)")
    wl_role = st.text_input("Role (optional)")
    wl_submit = st.form_submit_button("Join Waitlist")
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

# --- Footer ---
st.markdown('<div class="footer">ComplyAI — Founder: Naveen • Prototype Demo</div>', unsafe_allow_html=True)
