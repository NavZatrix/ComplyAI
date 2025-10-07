import streamlit as st
import openai
import csv
import os
from datetime import datetime

# --- Page config ---
st.set_page_config(page_title="ComplyAI", page_icon="🛡️", layout="wide")

# --- Content dictionary ---
content = {
    "navbar": {
        "logo": "logo.png",
        "title": "ComplyAI",
        "links": ["Demo", "Features", "Product", "Testimonials", "Waitlist"]
    },
    "hero": {
        "title": "ComplyAI",
        "subtitle": "Your AI-Powered Compliance Copilot for Startups",
        "cta_text": "Try Demo →",
        "cta_link": "#demo"
    },
    "features": [
        {"title": "🚀 Fast SOC 2 Readiness", "desc": "Get an actionable checklist in minutes, tailored for startups."},
        {"title": "📄 Policy Drafts", "desc": "Generate professional policy templates instantly — ready for auditors."},
        {"title": "🔍 Risk Prioritization", "desc": "Identify and prioritize top compliance risks automatically."}
    ],
    "product_preview": {
        "title": "Product Preview",
        "description": "Explore how ComplyAI helps you build trust, pass audits, and stay secure — effortlessly.",
        "images": [
            {"path": "assets/dashboard_mock.png", "caption": "Dashboard Overview"},
            {"path": "assets/feature1.png", "caption": "Policy Generator Example"}
        ]
    },
    "testimonials": [
        {"name": "Alice, CTO", "text": "ComplyAI saved us weeks of compliance work!"},
        {"name": "Bob, Founder", "text": "Finally, a tool that understands startup compliance."},
        {"name": "Carol, Security Lead", "text": "The AI suggestions are actionable and clear."}
    ],
    "waitlist": {
        "title": "Join Early Access",
        "fields": ["Work email", "Company (optional)", "Role (optional)"],
        "button": "Join Waitlist"
    },
    "footer": "ComplyAI • Founded by Naveen • © 2025"
}

# --- CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');

html, body {
    font-family: 'Inter', sans-serif;
    background-color: #f9fafb;
    scroll-behavior: smooth;
}

.navbar {
    width: 100%;
    background: rgba(255, 255, 255, 0.9);
    padding: 16px 60px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    position: sticky;
    top: 0;
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: space-between;
    backdrop-filter: blur(10px);
}

.navbar a {
    color: #111827;
    margin-left: 25px;
    text-decoration: none;
    font-weight: 600;
    transition: color 0.2s;
}

.navbar a:hover {
    color: #6366f1;
}

.nav-logo {
    display: flex;
    align-items: center;
    font-weight: 700;
    font-size: 22px;
    color: #111827;
}

.nav-logo img {
    height: 40px;
    margin-right: 10px;
}

.hero {
    padding: 120px 30px 100px 30px;
    background: linear-gradient(135deg, #6366f1 0%, #10b981 100%);
    color: white;
    border-radius: 0 0 80px 80px;
    text-align: center;
    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
}

.hero h1 {
    font-size: 56px;
    font-weight: 700;
    margin-bottom: 12px;
}

.hero p {
    font-size: 20px;
    margin-bottom: 30px;
}

.button-primary {
    background-color: white;
    color: #4f46e5;
    padding: 14px 30px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 16px;
    text-decoration: none;
    transition: all 0.2s ease-in-out;
}

.button-primary:hover {
    background-color: #f0fdf4;
    transform: translateY(-2px);
}

.section-title {
    text-align: center;
    font-size: 34px;
    font-weight: 700;
    margin-top: 80px;
    margin-bottom: 40px;
    color: #111827;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.05);
    margin: 10px;
    text-align: center;
    transition: transform 0.2s ease-in-out;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
}

.footer {
    text-align: center;
    color: #6b7280;
    font-size: 14px;
    padding: 40px 0;
    margin-top: 60px;
    border-top: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# --- Navbar ---
links_html = "".join([f'<a href="#{link.lower()}">{link}</a>' for link in content["navbar"]["links"]])
st.markdown(f"""
<div class="navbar">
    <div class="nav-logo">
        <img src="{content['navbar']['logo']}" alt="{content['navbar']['title']} Logo">
        {content['navbar']['title']}
    </div>
    <div class="nav-links">{links_html}</div>
</div>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown(
    f"""
    <div class="hero" id="hero">
        <h1>{content['hero']['title']}</h1>
        <p>{content['hero']['subtitle']}</p>
        <a class="button-primary" href="{content['hero']['cta_link']}">{content['hero']['cta_text']}</a>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Features Section ---
st.markdown('<div class="section-title" id="features">Why Choose ComplyAI?</div>', unsafe_allow_html=True)
cols = st.columns(3)
for col, feature in zip(cols, content["features"]):
    col.markdown(f'<div class="card"><h3>{feature["title"]}</h3><p>{feature["desc"]}</p></div>', unsafe_allow_html=True)

# --- Demo Section ---
st.markdown('<div class="section-title" id="demo">Live Demo</div>', unsafe_allow_html=True)
left, right = st.columns([2,3])

with left:
    framework = st.selectbox("Framework", ["SOC 2", "ISO 27001", "GDPR"])
    company_size = st.text_input("Company size", value="15")
    cloud = st.selectbox("Cloud provider", ["AWS", "Azure", "GCP", "Other"])
    tech_stack = st.text_area("Tech stack", value="Python, React, PostgreSQL")
    primary_goal = st.selectbox("Primary goal", ["Readiness checklist", "Policy drafts", "Risk prioritization"])
    generate = st.button("✨ Generate Recommendations")

with right:
    output_box = st.empty()
    output_box.info("Your AI-generated recommendations will appear here.")

def build_prompt(framework, company_size, cloud, primary_goal):
    return f"""
You are a pragmatic cybersecurity compliance assistant.
Produce a concise, startup-focused output for: {framework}.
Company size: {company_size} employees.
Cloud: {cloud}
Tech stack: {tech_stack}
Deliverable: {primary_goal}

Format:
- Executive summary (2 lines)
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
        with st.spinner("Thinking..."):
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

# --- Product Section ---
st.markdown(f'<div class="section-title" id="product">{content["product_preview"]["title"]}</div>', unsafe_allow_html=True)
st.markdown(content["product_preview"]["description"])
cols = st.columns(2)
for col, img in zip(cols, content["product_preview"]["images"]):
    if os.path.exists(img["path"]):
        col.image(img["path"], caption=img["caption"], use_column_width=True)
    else:
        col.markdown(f'<div class="card"><p>[Add {img["path"]} in assets/ folder]</p></div>', unsafe_allow_html=True)

# --- Testimonials Section ---
st.markdown('<div class="section-title" id="testimonials">What Founders Say</div>', unsafe_allow_html=True)
cols = st.columns(3)
for col, t in zip(cols, content["testimonials"]):
    col.markdown(f'<div class="card"><p>"{t["text"]}"</p><b>{t["name"]}</b></div>', unsafe_allow_html=True)

# --- Waitlist Section ---
st.markdown(f'<div class="section-title" id="waitlist">{content["waitlist"]["title"]}</div>', unsafe_allow_html=True)
with st.form("waitlist_form"):
    wl_email = st.text_input(content["waitlist"]["fields"][0])
    wl_company = st.text_input(content["waitlist"]["fields"][1])
    wl_role = st.text_input(content["waitlist"]["fields"][2])
    wl_submit = st.form_submit_button(content["waitlist"]["button"])
    if wl_submit:
        if not wl_email:
            st.warning("Please enter your email.")
        else:
            os.makedirs("data", exist_ok=True)
            path = os.path.join("data", "waitlist.csv")
            first_write = not os.path.exists(path)
            with open(path, "a", newline="") as f:
                writer = csv.writer(f)
                if first_write:
                    writer.writerow(["email","company","role","timestamp"])
                writer.writerow([wl_email, wl_company, wl_role, datetime.utcnow().isoformat()])
            st.success("✅ You’re on the waitlist!")

# --- Footer ---
st.markdown(f'<div class="footer">{content["footer"]}</div>', unsafe_allow_html=True)
