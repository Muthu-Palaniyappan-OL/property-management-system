import os
import base64
import google.auth
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
# from fpdf import FPDF
import random

# def generate_invoice():
#     num=random.random()
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=15)
#     pdf.cell(200, 10, txt="M4ESTATES Rent Receipt", ln=1, align='J')
#     #Add Property ID, Price and Date here
#     pdf.cell(200, 10, txt="", ln=2, align='J')
#     pdf.output(num)
#     return

# Get credentials using OAuth 2.0 flow
def get_credentials():
    scopes = ['https://www.googleapis.com/auth/gmail.send']
    credentials = None
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', scopes)
    else:
        from google_auth_oauthlib.flow import InstalledAppFlow
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes)
        credentials = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())
    return credentials

# Send email with attachments
def send_email(to, subject, body, pdf_path, credentials):
    try:
        service = build('gmail', 'v1', credentials=credentials)
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        text = MIMEText(body)
        message.attach(text)
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()
            pdf_attachment = MIMEApplication(pdf_data, _subtype='pdf')
            pdf_attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(pdf_path))
            message.attach(pdf_attachment)
        create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        print(f"Message Id: {send_message['id']}")
    except HttpError as error:
        print(f'An error occurred: {error}')
        send_message = None
    return send_message


if os.path.exists('token.json'):
    credentials = Credentials.from_authorized_user_file('token.json')
else:
    pass


#Add the corresponding user mail from db
to = 'jayenths@gmail.com'
subject = 'M4Estates-Rent receipt'
body = 'Hello <<<name>>>,\n\nYour rent payment of <<<price>> is successfully received\n\nThanks and regards,\nAdmin\nM4Estates'
pdf_path = 'dummy.pdf'
# generate_invoice()
# send_email(to, subject, body, pdf_path, credentials)

def send_invoice_mail(to):
    subject = 'M4Estates-Rent receipt'
    body = 'Hello <<<name>>>,\n\nYour rent payment of <<<price>> is successfully received\n\nThanks and regards,\nAdmin\nM4Estates'
    pdf_path = 'receipt.pdf'
    send_email(to, subject, body, pdf_path, credentials)