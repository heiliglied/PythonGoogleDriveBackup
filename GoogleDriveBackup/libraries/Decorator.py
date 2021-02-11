#-*- coding:utf-8 -*- 

from functools import wraps
import sys, os, os.path

def checkClientSecret(func):
	@wraps(func)
	def decoration(*args, **kwargs):
		#파일 체크 후, 없을 시 exit 시킴.
		#now_path = os.getcwd()
		now_path = os.path.dirname( os.path.abspath( __file__ ) )
		file = now_path + '/../config/google/client_secret.json'
		if os.path.isfile(file):
			func()
		else:
			print('client secret 파일이 없을 시 연결할 수 없습니다.\nconfig/google 폴더에 client_secret.json 파일을 추가해주세요.\nhttps://console.developers.google.com/apis/dashboard 페이지에서 OAuth ID 2.0을 발급받으시면 됩니다.')
			sys.exit
	return decoration

def argumentCheck(func):
	@wraps(func)
	def decoration(*args, **kwargs):
		if len(sys.argv) > 3:
			print('잘못된 입력 값입니다. ex) GoogleDriveBackup.py [filename] [upload folder_id(google)](option)')
			sys.exit
		elif len(sys.argv) < 2:
			print('잘못된 입력 값입니다. ex) GoogleDriveBackup.py [filename] upload folder_id(google)](option)')
			sys.exit
		func()
	return decoration
