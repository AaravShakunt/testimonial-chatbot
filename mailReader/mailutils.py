import base64
import email
import os.path
import re
import json

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.addons.current.action.compose', 'https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.modify']

class gmailUtils:
    # Scopes for Gmail API
    
    def __init__(self):
        self.service = self.get_gmail_service()

    def send_mail(self, mail, query):
        # Compose the email details
        recipient_email = mail
        subject = 'Hello from Gmail API'
        message_text = query

        # Create the Message object
        message = MIMEText(message_text)
        message['to'] = recipient_email
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        send_request = self.service.users().messages().send(userId='me', body={'raw': raw_message})
        response = send_request.execute()

        print('Email sent successfully.')

    def get_gmail_service(self):
        """Authenticate and obtain Gmail API service."""
        creds = None
        # The file token.json stores the user's access and refresh tokens.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('gmail', 'v1', credentials=creds)
        return service



    def parse_email_data(msg):
        """Parse email data to extract subject, sender, recipient, and content."""
        email_data = {}

        payload = msg['payload']
        headers = payload['headers']
        for header in headers:
            name = header['name']
            value = header['value']
            if name.lower() == 'subject':
                email_data['subject'] = value
            elif name.lower() == 'to':
                email_data['recipient'] = value
            elif name.lower() == 'from':
                email_data['sender'] = value

        if 'parts' in payload:
            parts = payload['parts']
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    content = base64.urlsafe_b64decode(data).decode("utf-8")
                    email_data['content'] = content

        return email_data

    def get_unread_emails(self):
        """Get unread emails from Gmail and mark them as read."""
        results = self.service.users().messages().list(userId='me', labelIds=['UNREAD']).execute()
        messages = results.get('messages', [])

        if not messages:
            print('No unread emails found.')
            return []

        emails = []
        for message in messages:
            msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
            email_data = self.parse_email_data(msg)
            # email_data = parse_email_data(msg)
            emails.append(email_data)

            # Mark the email as read
            self.service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()

        return emails

    def process_email_subject(email_subject):
        """Extract the unique <ID> from the email subject if it matches the specified format."""
        pattern = r"Customer Question <(\d+)>"
        match = re.search(pattern, email_subject)
        if match:
            return match.group(1)
        return None

    def process_email_content(email_content):
        """Process the email content to handle acceptance/denial and question-answer pairs."""
        # Check if the email contains ONLY "ACCEPT" or "DENY"
        if re.fullmatch(r"ACCEPT|DENY", email_content.strip()):
            acceptance_status = email_content.strip()
            question = None
            answer = None
        else:
            # Extract question and answer if present in the specified format
            pattern = r"Question:(.*?)(?:\n\nAnswer:(.*))?"
            match = re.search(pattern, email_content, re.DOTALL)
            if match:
                question = match.group(1).strip()
                answer = match.group(2).strip() if match.group(2) else None
                acceptance_status = None
            else:
                acceptance_status = None
                question = email_content.strip()
                answer = None

        return acceptance_status, question, answer


if __name__ == "__main__":
    # Authenticate and obtain Gmail API service
    gmail_Utils = gmailUtils()
    # service = gmail_Utils.get_gmail_service()

    # Get unread emails and extract subject, sender, recipient, and content
    unread_emails = gmail_Utils.get_unread_emails()

    # Print the extracted data
    for email_data in unread_emails:
        email_subject = email_data['subject']
        email_content = email_data['content']

        # Extract <ID> from the email subject
        unique_id = gmail_Utils.process_email_subject(email_subject)
        if unique_id:
            # Process email content for acceptance/denial and question-answer pairs
            acceptance_status, question, answer = gmail_Utils.process_email_content(email_content)
            print(f"ID: {unique_id}")
            print(f"Acceptance/Denial: {acceptance_status}")
            print(f"Question: {question}")
            print(f"Answer: {answer}")
            print("-----------------------")
