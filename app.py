import streamlit as st
import openai
import csv
import os
import base64
from datetime import datetime
from PIL import Image

# --- Page config ---
st.set_page_config(page_title="ComplyAI", page_icon="🛡️", layout="wide")

# --- Helper to embed logo ---
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

encoded_logo = get_base64_image("logo.png")  # ensure logo.png is in same folder

# --- Content dictionary ---
content = {
    "navbar": {
        "title": "ComplyAI",
        "links": ["Demo", "Features", "Product", "Testimonials", "Waitlist"]
    },
    "hero": {
        "title": "ComplyAI",
        "subtitle": "AI-Powered Compliance Copilot for Startups",
        "cta_text": "Try Demo →",
        "cta_link": "#demo"
    },
    "features": [
        {"title": "🚀 Fast SOC 2 Readiness", "desc": "Get an actionable checklist in minutes."},
        {"title": "📄 Policy Drafts", "desc": "Generate professional policy templates instantly."},
        {"title": "🔍 Risk Prioritization", "desc": "Identify and prioritize your top compliance risks."}
    ],
    "product_preview": {
        "title": "Product Preview",
        "description": "Explore how ComplyAI delivers clarity, automation, and structure to compliance tasks.",
        "images": [
            {"path": "assets/dashboard_mock.png", "caption": "Dashboard Overview"},
            {"path": "assets/feature1.png", "caption": "Feature Example"}
        ]
    },
    "testimonials": [
        {"name": "Alice, CTO", "text": "ComplyAI saved us weeks of compliance work!"},
        {"name": "Bob, Founder", "text": "Finally a tool that understands startup compliance."},
        {"name": "Carol, Security Lead", "text": "The AI suggestions are actionable and clear."}
    ],
    "waitlist": {
        "title": "Join Early Access",
        "fields": ["Work email", "Company (optional)", "Role (optional)"],
        "button": "Join Waitlist"
    },
    "footer": "ComplyAI — Founder: Naveen • Prototype Demo"
}

# --- Modern CSS Styling ---
st.markdown("""
<style>
body {
    background: #f9fafb;
    font-family: 'Inter', sans-serif;
    color: #111827;
}
.navbar {
    width: 100%;
    background: white;
    padding: 16px 60px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    position: sticky;
    top: 0;
    z-index: 999;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.navbar a {
    color: #111827;
    margin-left: 28px;
    text-decoration: none;
    font-weight: 600;
}
.navbar a:hover {
    color: #6366f1;
}
.nav-logo {
    display: flex;
    align-items: center;
}
.nav-logo img {
    height: 100px;
    margin-right: 10px;
    border-radius: 6px;
}
.hero {
    padding: 100px 30px;
    background: linear-gradient(90deg, #6366f1, #10b981);
    color: black;
    border-radius: 12px;
    text-align: center;
    margin-top: 30px;
}
.hero h1 {
    font-size: 52px;
    font-weight: 800;
    margin-bottom: 10px;
}
.hero p {
    font-size: 22px;
    margin-bottom: 30px;
}
.button-primary {
    background-color: #ffffff;
    color: #6366f1;
    padding: 14px 32px;
    border-radius: 10px;
    font-weight: bold;
    text-decoration: none;
    transition: all 0.3s ease;
}
.button-primary:hover {
    background-color: #f3f4f6;
}
.section-title {
    text-align: center;
    padding-top: 70px;
    padding-bottom: 20px;
    font-size: 32px;
    font-weight: 800;
}
.card {
    background: white;
    padding: 28px;
    border-radius: 14px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.08);
    margin: 10px;
    text-align: center;
    transition: all 0.2s ease-in-out;
}
.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 28px rgba(0,0,0,0.1);
}
.card img {
    border-radius: 12px;
    margin-bottom: 10px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.08);
}
.footer {
    text-align: center;
    color: #6b7280;
    font-size: 14px;
    padding: 40px 10px;
}
</style>
""", unsafe_allow_html=True)

# --- Navbar ---
links_html = "".join([f'<a href="#{link.lower()}">{link}</a>' for link in content["navbar"]["links"]])
st.markdown(f"""
<div class="navbar">
    <div class="nav-logo">
        <img src="data:image/png;base64,{encoded_logo}" alt="ComplyAI Logo">
        <span style="font-weight:bold; font-size:20px;">{content['navbar']['title']}</span>
    </div>
    <div class="nav-links">{links_html}</div>
</div>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown(
    f'<div class="hero"><h1>{content["hero"]["title"]}</h1>'
    f'<p>{content["hero"]["subtitle"]}</p>'
    f'<a class="button-primary" href="{content["hero"]["cta_link"]}">{content["hero"]["cta_text"]}</a></div>',
    unsafe_allow_html=True
)

# --- Features Section ---
st.markdown('<div class="section-title" id="features">Why ComplyAI?</div>', unsafe_allow_html=True)
cols = st.columns(3)
for col, feature in zip(cols, content["features"]):
    col.markdown(f'<div class="card"><h3>{feature["title"]}</h3><p>{feature["desc"]}</p></div>', unsafe_allow_html=True)

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
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful cybersecurity compliance assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.35,
                    max_tokens=900
                )
                text = response.choices[0].message.content.strip()
                output_box.markdown(text)
                st.download_button("📥 Download (TXT)", data=text, file_name=f"ComplyAI_{framework}.txt")
            except Exception as e:
                st.error(f"AI request failed: {e}")

st.markdown("---")

# --- Product Preview Section ---
st.markdown(f'<div class="section-title" id="product-preview">{content["product_preview"]["title"]}</div>', unsafe_allow_html=True)
st.markdown(content["product_preview"]["description"])
cols = st.columns(2)
for col, img in zip(cols, content["product_preview"]["images"]):
    if os.path.exists(img["path"]):
        col.image(img["path"], caption=img["caption"], use_column_width=True)
    else:
        col.markdown(f'<div class="card"><p>[Add {img["path"]} in assets/ folder]</p></div>', unsafe_allow_html=True)

st.markdown("---")

# --- Testimonials Section ---
st.markdown('<div class="section-title" id="testimonials">What Users Say</div>', unsafe_allow_html=True)
cols = st.columns(3)
for col, testimonial in zip(cols, content["testimonials"]):
    col.markdown(f'<div class="card"><p>"{testimonial["text"]}"</p><b>{testimonial["name"]}</b></div>', unsafe_allow_html=True)

st.markdown("---")

# --- Waitlist Section ---
st.markdown(f'<div class="section-title" id="waitlist">{content["waitlist"]["title"]}</div>', unsafe_allow_html=True)
with st.form("waitlist_form"):
    wl_email = st.text_input(content["waitlist"]["fields"][0])
    wl_company = st.text_input(content["waitlist"]["fields"][1])
    wl_role = st.text_input(content["waitlist"]["fields"][2])
    wl_submit = st.form_submit_button(content["waitlist"]["button"])
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
st.markdown(f'<div class="footer">{content["footer"]}</div>', unsafe_allow_html=True)
