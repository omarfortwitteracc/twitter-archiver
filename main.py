import os
import json
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# تحديد صلاحيات التطبيق
SCOPES = ['https://www.googleapis.com/auth/drive.file']  # صلاحية حفظ الملفات على Google Drive

# دالة للحصول على بيانات الاعتماد (Credentials)
def get_credentials():
    creds = None
    # إذا كان هناك ملف token.pickle، نستخدمه مباشرة لتفادي طلب التصريح كل مرة
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # إذا لم تكن بيانات الاعتماد صالحة أو كانت منتهية، نطلب بيانات جديدة
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # هنا يقوم المستخدم بتسجيل الدخول باستخدام OAuth
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # حفظ البيانات المصرح بها لتجنب إعادة التصريح في المستقبل
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

# دالة لإنشاء خدمة Google Drive
def build_drive_service():
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    return service

# دالة لتحميل الملفات إلى Google Drive
def upload_file_to_drive(service, file_name, file_path):
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, mimetype='application/octet-stream')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'File ID: {file["id"]}')

# دالة رئيسية لتشغيل الكود
def main():
    # إنشاء خدمة Google Drive باستخدام بيانات الاعتماد
    service = build_drive_service()
    
    # تحديد اسم الملف والموقع على الجهاز
    file_name = 'example.txt'  # استبدله باسم الملف الفعلي
    file_path = '/path/to/your/file/example.txt'  # استبدله بالمسار الصحيح للملف

    # تحميل الملف إلى Google Drive
    upload_file_to_drive(service, file_name, file_path)

if __name__ == '__main__':
    main()
