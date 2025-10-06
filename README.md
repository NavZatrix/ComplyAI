# ComplyAI — AI-Powered Compliance Copilot (Prototype)

Lightweight Streamlit prototype generating SOC 2 / ISO 27001 / GDPR readiness checklists.

## Run locally
1. python3 -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. create .streamlit/secrets.toml with OPENAI_API_KEY
5. streamlit run app.py

## Deploy
Push to GitHub + Render or Streamlit Cloud. Add OPENAI_API_KEY as environment variable.
