import os
import datetime
import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# إعداد Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

# إنشاء مجلد اليوم
today = datetime.datetime.now().strftime('%Y-%m-%d')
folder_metadata = {
    'name': today,
    'mimeType': 'application/vnd.google-apps.folder'
}
folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
folder_id = folder.get('id')

# تغريدة وهمية (مكان ما تربط مع تويتر لاحقاً)
tweet_text = "تغريدة تجريبية"
with open('tweet.txt', 'w', encoding='utf-8') as f:
    f.write(tweet_text)

file_metadata = {
    'name': 'tweet.txt',
    'parents': [folder_id]
}
media = MediaFileUpload('tweet.txt', mimetype='text/plain')
drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
