import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/generative-language.retriever', 'https://www.googleapis.com/auth/generative-language.tuning']
SERVICE_ACCOUNT_FILE = r"C:\Users\rater\Downloads\gen-lang-client-0452583531-b68d13ab9a33.json"

def load_creds():
    # Load service account credentials
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    return creds

