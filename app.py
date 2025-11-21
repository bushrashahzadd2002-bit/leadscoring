import streamlit as st
import requests
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Lead Scoring", layout="wide")

st.title("Lead Scoring")

st.write("Paste LinkedIn profile URLs below (one per line):")

urls_input = st.text_area("LinkedIn URLs", height=200)

n8n_webhook_url = "https://oversolemnly-vanitied-milagro.ngrok-free.dev/webhook/d71f69a1-6e6a-40d8-b510-4be5c02323f6"

SHEET_ID = "1Rb18WIcgrHWEncA_ZMtdUsmXP4VepQ5cPqg88mgtgWI"
SHEET_NAME = "Sheet1"

def append_to_google_sheet(df):
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("service_account.json", scopes=scopes)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

    rows = [df.columns.tolist()] + df.values.tolist()

    sheet.append_rows(rows, value_input_option="USER_ENTERED")

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
                else:
                    data = response.json()

                    if isinstance(data, dict):
                        data = [data]

                    df = pd.DataFrame(data)

                    st.success("Lead Scoring completed!")
                    st.dataframe(df)

                    append_to_google_sheet(df)
                    st.success("Data added to Google Sheet!")

            except Exception as e:
                st.error(f"Error: {e}")
