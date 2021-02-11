#-*- coding:utf-8 -*- 

from libraries import Decorator, GoogleDrive

import sys, os, os.path

DEFAULT_FOLDER_ID = "URL에 보이는 /folder/(ID) 해당 ID부분"

#default upload file's path
UPLOAD_FILE_NAME = ''

#client secret 파일 체크.
@Decorator.checkClientSecret
#argument option 체크 //못씀. arg_parse때문에 정해진 값만 사용 가능함.
# @Decorator.argumentCheck
def main():	
	upload_file = []
	with open(os.path.dirname( os.path.abspath( __file__ ) ) + "/files.txt", "r") as f:
		for line in f.readlines():
			upload_file.append(line)
	#UPLOAD_FILE_NAME = UPLOAD_FILE_NAME

	folder_id = DEFAULT_FOLDER_ID

	driveUpload = GoogleDrive.GoogleDrive()
	result = driveUpload.upload(upload_file, folder_id)

	print(result)
	sys.exit

if __name__ == "__main__":
	main()
