import os
import io
from datetime import date
import boto3
from botocore.exceptions import ClientError
import pandas as pd
import csv
def upload_file(file_obj, bucket, object_name=None):
	"""Upload a file to an S3 bucket

	:param file_obj: dataframe to upload
	:param bucket: Bucket to upload to
	:param object_name: S3 object name. If not specified then file_name is used
	:return: True if file was uploaded, else False
	"""
		
	# If S3 object_name was not specified, use file_name
	# if object_name is None:
	#	 object_name = os.path.basename(file_name)

	# Upload the file
	s3_client = boto3.client('s3')
	try:
		response = s3_client.put_object(Body=file_obj, Bucket=bucket, Key=object_name)
	except ClientError as e:
		print(e)
		return False
	return True

bucket = 'cfde-drc'

now = str(date.today()).replace("-", "")

def backup_file(df, suffix, include_index=True, quoting=True):
	print("backing up on s3...")
	s_buf = io.StringIO()
	# df.to_csv(s_buf, header=True, sep="\t")
	# print(s_buf.read())
	if include_index:
		df.to_csv(s_buf, header=True, sep="\t")
	elif not quoting:
		df.to_csv(s_buf, header=True, sep="\t", quoting=csv.QUOTE_NONE)
	else:
		df.to_csv(s_buf, header=True, sep="\t",  index=None)
	object_name = "database/files/%s_%s.tsv"%(now, suffix)
	upload_file(s_buf.getvalue(), bucket, object_name)
	object_name = "database/files/current_%s.tsv"%(suffix)
	upload_file(s_buf.getvalue(), bucket, object_name)