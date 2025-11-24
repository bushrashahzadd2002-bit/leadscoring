import streamlit as st
import requests
import pandas as pd
import time
import os

st.set_page_config(page_title="Lead Scoring", layout="wide")

st.title("Lead Scoring")

st.write("Paste LinkedIn profile URLs below (one per line):")

urls_input = st.text_area("LinkedIn URLs", height=200)

# n8n webhook URL from Streamlit secrets
n8n_webhook_url = st.secrets["WEBHOOK_URL"]

if st.button("Run Lead Scoring"):
    if not urls_input.strip():
        st.error("Please enter at least one link.")
    else:
        # Convert textarea into Python List
        urls = [u.strip() for u in urls_input.split("\n") if u.strip()]

        with st.spinner("Processing leads..."):
            try:
                # Send request to n8n
                response = requests.post(
                    n8n_webhook_url,
                    json={"urls": urls},  # send multiple URLs list
                    auth=(st.secrets["N8N_USER"], st.secrets["N8N_PASSWORD"])
                )

                # Validate status
                if response.status_code != 200:
                    st.error(f"n8n Error: {response.text}")
                    st.stop()

                data = response.json()

                # n8n may return a single dict or a list → normalize to list
                if isinstance(data, dict):
                    data = [data]

                df = pd.DataFrame(data)

                st.success("Lead Scoring completed! 🎉")
                st.success("✅ Data added to Google Sheet!")

                # Show table
                st.dataframe(df, use_container_width=True)

                # Download CSV
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download Results as CSV",
                    csv,
                    "lead_scoring_results.csv",
                    "text/csv",
                    key="download-csv"
                )

            except Exception as e:
                st.error(f"Error: {e}")
