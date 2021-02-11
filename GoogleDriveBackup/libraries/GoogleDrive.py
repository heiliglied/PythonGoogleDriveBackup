#-*- coding:utf-8 -*- 

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload

import os, sys

class GoogleDrive:
	
	def upload(self, upload_file, folder_id):
				
		for file_title in upload_file:
			name_split = file_title.rsplit('/', 1)[1]

			'''
			file_list = self.getFileList(folder_id)
			for file in file_list:
				if file[1] == name_split:
					self.deleteFile(file[0])
			'''
									
			file_metadata = {
				'name': name_split,
				'parents': [folder_id],
			}

			media = MediaFileUpload(file_title)

			file_info = self.getFile(name_split)
			if file_info and file_info[0]['name'] == name_split:
				self.deleteFile(file_info[0]['id'])

			res = self.createFile(file_metadata, media)
			if res:
				return '파일이 업로드 되었습니다.'

	def getFileList(self, folder_id):
		query = f"'{folder_id}' in parents"
		down_service = self.drive_service('download')
		result = []
		page_token = None

		while True:
			response = down_service.files().list(q=query,
												spaces="drive",
												fields="nextPageToken, files(id, name, mimeType)",
												pageToken=page_token).execute()
			for file in response.get("files", []):
				result.append((file['id'], file['name']))
			page_token = response.get('nextPageToken', None)
			if not page_token:
				#다음 페이지 없음.
				break

		return result

	def getFile(self, file_name):
		query = f"name = '{file_name}'"
		down_service = self.drive_service('download')
		page_token = None
		response = down_service.files().list(q=query,
											spaces="drive",
											fields="nextPageToken, files(id, name, mimeType)",
											pageToken=page_token).execute()

		return response.get("files", [])

	def createFile(self, meta_data, media):
		service = self.drive_service('upload')
		return service.files().create(body=meta_data, media_body=media).execute()

	def updateFile(self, file_id, meta_data, media):
		service = self.drive_service('upload')
		return service.files().update(
									fileId=file_id,
									body=meta_data,
									newRevision=new_revision,
									media_body=media).execute()

	def deleteFile(self, file_id):
		service = self.drive_service('upload')
		return service.files().delete(fileId=file_id).execute()

	def drive_service(self, type):
		try:
			import argparse
			flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
		except ImportError:
			flags = None

		if type == 'upload':
			SCOPE = 'https://www.googleapis.com/auth/drive.file'
			CREDENTIAL_FILE_NAME = 'drive-python-upload.json'
		elif type == 'download':
			SCOPE = 'https://www.googleapis.com/auth/drive.readonly'
			CREDENTIAL_FILE_NAME = 'drive-python-download.json'
		elif type == 'all':
			SCOPE = 'https://www.googleapis.com/auth/drive'
			CREDENTIAL_FILE_NAME = 'drive-python-all.json'
		else:
			SCOPE = 'https://www.googleapis.com/auth/drive.metadata.readonly'
			CREDENTIAL_FILE_NAME = 'drive-python-all.json'
		#now_path = os.getcwd()
		now_path = os.path.dirname( os.path.abspath( __file__ ) )
		
		CLIENT_SECRET_FILE = 'client_secret.json'
		
		client_secret = now_path + '/../config/google/' + CLIENT_SECRET_FILE
		credential_file = now_path + '/../config/google/' + CREDENTIAL_FILE_NAME

		store = file.Storage(credential_file)
		credits = store.get()

		if not credits or credits.invalid:
				print("인증에 필요한 파일을 다운로드 합니다.")
				flow = client.flow_from_clientsecrets(client_secret, SCOPE)
				credits = tools.run_flow(flow, store, flags) \
						if flags else tools.run_flow(flow, store)
				sys.exit

		return build('drive', 'v3', http=credits.authorize(Http()))