from __future__ import print_function
import os.path
from time import sleep
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from vidtest import getframes
from time import time

SCOPES = ['https://www.googleapis.com/auth/drive.file']
DOCUMENT_ID = '1HbI9540qtaDd0W13Y9typazBgutqB08j7-E_Zm2OTEQ'

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('docs', 'v1', credentials=creds)

    document = service.documents().get(documentId=DOCUMENT_ID).execute()

    def createdoc():
        title = 'My Document'
        body = {
            'title': title
        }
        doc = service.documents().create(body=body).execute()
        print('Created document with title:', doc.get('title'))

    def createrange():
        # Create range for video
        request = [
            {
                'createNamedRange': {
                    'name': 'main',
                    'range': {
                        'startIndex': 1,
                        'endIndex': 2,
                    }
                }
            },
        ]
        service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': request}).execute()

    def deleteallranges():
        request = [
            {
                'deleteNamedRange': {
                    'name': 'main'
                }
            },
        ]
        service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': request}).execute()
        print('remaining ranges:')
        print(document.get('namedRanges', {}).get('main'))

    createrange()

    request = [
        {
            'replaceNamedRangeContent': {
                'text': 'youshouldntseethis',
                'namedRangeName': 'main'
            }
        },
    ]
    
    frames = getframes('badapple.mp4', 5)

    prev_time = time()

    for frame in frames:
        while time() < prev_time + 1:
            pass
        else:
            request[0]['replaceNamedRangeContent']['text'] = frame
            service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': request}).execute()
            prev_time = time()

    print('DONE.')
    request[0]['replaceNamedRangeContent']['text'] = 'DONE. '
    service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': request}).execute()

    deleteallranges()

if __name__ == '__main__':
    main()
