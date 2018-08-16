from __future__ import print_function
import os
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.http import MediaFileUpload

SCOPES = 'https://www.googleapis.com/auth/drive'

# Store authentication information after browser authentication is completed
store = file.Storage('storage.json')

def uploadVideoToGoogleDrive(fileName):
    try:
        # Authentication
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('drive', 'v3', http=creds.authorize(Http()))

        # Upload the selected file to google drive
        file_metadata = {'name': fileName}
        media = MediaFileUpload(fileName,
                                mimetype='video/x-msvideo')
        file = service.files().create(body=file_metadata,
                                            media_body=fileName,
                                            fields='id').execute()
        print('Video upload completed')
    except:
        print('Problems uploading video')
        pass
