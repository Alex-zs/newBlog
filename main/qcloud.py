from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

class QcloudCos(object):
	#基本配置
	secret_id = '******'
	secret_key = '******'
	token = ''
	region = 'ap-beijing'
	scheme = 'https'
	config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
	client = CosS3Client(config)

	#删除文件
	def delete(self, file_name):
		self.client.delete_object(
			Bucket = 'alex-1256236352',
			Key = file_name,
		)

	#上传文件
	def put(self, file_path, file_name):
		with open(file_path,'rb') as fp:
			self.client.put_object(
				Bucket = '******',
				Body = fp,
				Key = file_name,
				StorageClass = 'STANDARD',
				ContentType='text/html; charset=utf-8'
			)


		

