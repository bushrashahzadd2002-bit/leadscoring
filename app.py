import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Lead Scoring", layout="wide")

st.title("Lead Scoring")

st.write("Paste LinkedIn profile URLs below (one per line):")

urls_input = st.text_area("LinkedIn URLs", height=200)

n8n_webhook_url = "https://oversolemnly-vanitied-milagro.ngrok-free.dev/webhook/d71f69a1-6e6a-40d8-b510-4be5c02323f6"

SECRET_KEY = st.secrets["WEBHOOK_SECRET"]


if st.button("Run Lead Scoring"):
    if not urls_input.strip():
        st.error("Please enter at least one link.")
    else:
        urls = [u.strip() for u in urls_input.split("\n") if u.strip()]

        with st.spinner("Processing leads..."):
            try:
                response = requests.post(
                        n8n_webhook_url,
                        json={"urls": urls, "token": SECRET_KEY}
                )

                data = response.json()

                if isinstance(data, dict):
                    data = [data]

                st.success("Lead Scoring completed!")

                st.success("✅ Data added to Google Sheet!")

            except Exception as e:
                st.error(f"Error: {e}")
