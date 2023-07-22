
from dataIngester import index
from sentence_transformers import SentenceTransformer
import pinecone
import openai
import streamlit as st
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

# Load credentials from JSON file
with open('token.json') as json_file:
    credentials = json.load(json_file)

oauth_credentials = Credentials.from_authorized_user_info(credentials)

service = build('gmail', 'v1', credentials=oauth_credentials)

openai.api_key = ""
model = SentenceTransformer('all-MiniLM-L6-v2')

pinecone.init(api_key='', environment='us-east4-gcp')
index = pinecone.Index('langchain-chatbot')

def send_mail(mail, query):
    # Compose the email details
    recipient_email = mail
    subject = 'Hello from Gmail API'
    message_text = query

    # Create the Message object
    message = MIMEText(message_text)
    message['to'] = recipient_email
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    send_request = service.users().messages().send(userId='me', body={'raw': raw_message})
    response = send_request.execute()

    print('Email sent successfully.')

def find_match(input):
    input_em = model.encode(input).tolist()
    result = index.query(input_em, top_k=2, includeMetadata=True)
    return result['matches'][0]['metadata']['text']+"\n"+result['matches'][1]['metadata']['text']

def getResponse(query):
    return "hello"+query




# docs = split_docs(documents)
# print(len(docs))