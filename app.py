import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Lead Scoring", layout="wide")

st.title("Lead Scoring")

st.write("Paste LinkedIn profile URLs below (one per line):")

urls_input = st.text_area("LinkedIn URLs", height=200)

n8n_webhook_url = "https://oversolemnly-vanitied-milagro.ngrok-free.dev/webhook/d71f69a1-6e6a-40d8-b510-4be5c02323f6"

if st.button("Run Lead Scoring"):
    if not urls_input.strip():
        st.error("Please enter at least one link.")
    else:
        urls = [u.strip() for u in urls_input.split("\n") if u.strip()]

        with st.spinner("Processing leads..."):
            try:
                response = requests.post(n8n_webhook_url, json={"urls": urls})
                
                if response.status_code != 200:
                    st.error(f"n8n Error: {response.text}")
                    st.stop()

                raw_data = response.json()

                if isinstance(raw_data, dict) and raw_data.get("message") == "Workflow has started":
                    st.error("n8n did not return lead data. Check your workflow.")
                    st.stop()

                # Ensure data is a list
                if isinstance(raw_data, dict):
                    data = [raw_data]
                else:
                    data = raw_data

                df = pd.DataFrame(data)

                st.success("Lead Scoring completed!")
                st.dataframe(df)

                st.success("✅ Data added to Google Sheet!")

            except Exception as e:
                st.error(f"Error: {e}")
