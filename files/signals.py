from django.dispatch import receiver
from django.db.models.signals import post_save
from files.models import File,Faculty,Module
from google.oauth2.credentials import Credentials, credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = './config.json'

credentials = Credentials.from_authorized_user_file("./config.json")
# Create the Google Drive service
drive_service = build('drive', 'v3', credentials=credentials)

MASTER_FOLDER_ID = "1-Hy1HWGoEfNpKTB-IRq4DPVCPG8O-K77"


@receiver(post_save,sender=File)
def handle_file_accepting(sender,instance,created,**kwargs):
    if instance.accepted:
        file_metadata = {
            'name': instance.file.name,
            'parents':[instance.module.drive_id]
        }
        media = MediaFileUpload(instance.file.path, resumable=True)
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, name, mimeType, webViewLink').execute()
        permission = {
        'role': 'reader',
        'type': 'anyone'
    }
        drive_service.permissions().create(fileId=file['id'], body=permission).execute()
        File.objects.filter(id=instance.id).update(drive_link=file.get("webViewLink"),file=None)
        os.remove(instance.file.path)


@receiver(post_save,sender=Module)
def hanle_Module_Creation(sender,instance,created,**kwargs):
    if instance.drive_id == None :
        body = {
        'name': instance.name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents':[MASTER_FOLDER_ID]
        }
        file = drive_service.files().create(body=body,fields='id').execute()
        instance.drive_id = file.get('id')
        instance.save()


    

