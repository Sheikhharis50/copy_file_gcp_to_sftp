from utils.upload_to_sftp import upload_to_sftp
from utils.download_to_local import download_to_local

FILE_NAME = "<FILE_NAME>" # eg: testing/file.csv
BUCKET_NAME = "<BUCKET_NAME>" # eg: mybucket
REMOTE_PATH = "<REMOTE_PATH>"  # eg: "/home/ubuntu/testing/file.csv"

download_to_local(BUCKET_NAME, FILE_NAME)
upload_to_sftp(FILE_NAME, REMOTE_PATH)
