import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload
import io
import sys
from googleapiclient.http import MediaIoBaseDownload
from datetime import datetime

# If modifying these scopes, delete the file token.pickle.
def main(args):
    SCOPES = ['https://www.googleapis.com/auth/drive']

    folder_id = None

    if not (args== "push" or args=="pull"):
        print("Exactly one argument required push/pull")
        exit()




    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(q="mimeType='application/vnd.google-apps.folder'", fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])


    for item in items:
        if item['name'] == "passman":
            print("remote folder already exists...")
            folder_id = item['id']
            break
    else:
        print("creating new folder in gdrive...")
        file_metadata = {
        'name': 'passman',
        'mimeType': 'application/vnd.google-apps.folder'
        }
        file = service.files().create(body=file_metadata, fields='id').execute()
        folder_id = file.get('id')


    #searching file in passman folder

    results = service.files().list(q="mimeType='application/octet-stream' and parents in '{}'".format(folder_id), fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    for item in items:
        if item['name'] == "backup.db.enc":
            print("previous backup found...")
            file_id = item['id']
            if args == "pull":
                request = service.files().get_media(fileId=file_id)
                fh = io.FileIO('passman.db.enc','wb')
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print ("Download %d%%." % int(status.progress() * 100))
            else:
                # update_file(service, file_id, "passman.db.enc", "updated"+str(datetime.now()),"application/octet-stream", "./passman.db.enc", True)
                service.files().delete(fileId = file_id).execute()
                file_push(service, folder_id)
                print("backup successful...")
            break
    else:
        if args == "push":
            file_push(service, folder_id)
            print("file pushed")
        else:
            print("Cannot pull...")

def file_push(service, folder_id):
    file_metadata = {
    'name': 'backup.db.enc',
    'mimeType': 'application/octet-stream',
    'parents': [folder_id]
    }
    media = MediaFileUpload('./passman.db.enc',
                            mimetype='application/octet-stream',
                            resumable=True)
    file = service.files().create(body=file_metadata,media_body=media,fields='id').execute()