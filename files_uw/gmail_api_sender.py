from __future__ import print_function
import base64
from email.message import EmailMessage
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import httplib2
import os
import oauth2client
from oauth2client import client, tools, file
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from private_credits import APPLICATION_NAME, Email_GMAIL, Path_project_google_api
from private_attachments import attachment_name

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CLIENT_SECRET_FILE = 'clientcredit.json'
APPLICATION_NAME = 'ApplicantRobot'

def get_credentials(home_dir_str):
    home_dir = os.path.expanduser(home_dir_str)
    os.chdir(home_dir)
    credential_dir = os.path.join(home_dir, '.credentials')
    #Place le path a l endroit de travail
    
    credentials = None
    
    if os.path.exists('./.credentials/gmail-python-email-send.json'):
        print("Credentials existant")
        credentials = Credentials.from_authorized_user_file('./.credentials/gmail-python-email-send.json', SCOPES)
    #Recupere les credentials si ils ont deja ete stockes
    else:
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
    #Si le dossier .credentials n existe pas il est cree
    
    if not credentials or not credentials.valid:
        print("MaJ credentials API")
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)
        with open('./.credentials/gmail-python-email-send.json', 'w') as token:
            token.write(credentials.to_json())
    return credentials


def gmail_send_message(destinataire, message2send, objet):
    creds = get_credentials(Path_project_google_api)

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message.set_content(message2send)

        message['To'] = destinataire
        message['From'] = Email_GMAIL
        message['Subject'] = objet

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message



def gmail_send_message_with_attachment(destinataire, message2send, objet, attachment):
    creds = get_credentials(Path_project_google_api)

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message.set_content(message2send)
        
        
        #Ajout de attachment --------------
        
        with open(attachment, 'rb') as content_file:
            content = content_file.read()
            message.add_attachment(content, maintype='application', subtype= (attachment.split('.')[1]), filename=attachment)
        
        
        #Ajout de attachment --------------
        
        
        message['To'] = destinataire
        message['From'] = Email_GMAIL
        message['Subject'] = objet

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message



