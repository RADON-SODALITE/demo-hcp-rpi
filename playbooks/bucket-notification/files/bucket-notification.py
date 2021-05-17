  
from minio import Minio
import requests
from sys import argv

node_ip = argv[1]
access_key_minio = argv[2]
secret_key_minio = argv[3]
bucket_in_name = argv[4]
function_name = argv[5]
event = argv[6]

mc = Minio(node_ip + ':9000', access_key=access_key_minio, secret_key=secret_key_minio, secure=False)

events = mc.listen_bucket_notification(bucket_in_name, events=[event])

for event in events:
    image = event["Records"][0]["s3"]["object"]["key"]
    data = '{"Records": [{"s3": {"bucket": {"name": "' + bucket_in_name + '"},"object": {"key":"' + str(image) + '"}}}]}'
    requests.post(url="http://" + node_ip + ":31112/function/" + function_name, data=data)