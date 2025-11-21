import streamlit as st
import requests
import pandas as pd
import os
import json
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Lead Scoring", layout="wide")

st.title("Lead Scoring")

st.write("Paste LinkedIn profile URLs below (one per line):")

urls_input = st.text_area("LinkedIn URLs", height=200)

# n8n Webhook
n8n_webhook_url = "https://oversolemnly-vanitied-milagro.ngrok-free.dev/webhook/d71f69a1-6e6a-40d8-b510-4be5c02323f6"

# Google Sheet details
SHEET_ID = "1Rb18WIcgrHWEncA_ZMtdUsmXP4VepQ5cPqg88mgtgWI"
SHEET_NAME = "Sheet1"

# ---------------------------
# GOOGLE SHEET AUTH FUNCTION
# ---------------------------
def get_gsheet_client():
    creds_info = os.getenv("GOOGLE_CREDENTIALS")

    if not creds_info:
        st.error("❌ GOOGLE_CREDENTIALS not found in environment variables.")
        return None

    creds_json = json.loads(creds_info)

    creds = Credentials.from_service_account_info(
        creds_json,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    client = gspread.authorize(creds)
    return client

# ---------------------------
# APPEND DATAFRAME TO SHEET
# ---------------------------
def append_to_google_sheet(df):
    client = get_gsheet_client()
    if client is None:
        return

    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

    # Convert DF to rows
    rows = [df.columns.tolist()] + df.values.tolist()

    sheet.append_rows(rows, value_input_option="USER_ENTERED")


# ---------------------------
# MAIN BUTTON ACTION
# ---------------------------
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

                data = response.json()

                # If API returns dict, convert to list
                if isinstance(data, dict):
                    data = [data]

                df = pd.DataFrame(data)

                st.success("Lead Scoring completed!")
                st.dataframe(df)

                append_to_google_sheet(df)

                st.success("✅ Data added to Google Sheet!")

            except Exception as e:
                st.error(f"Error: {e}")
