# Copyright (c) Alex Ellis 2017. All rights reserved.
# Copyright (c) OpenFaaS Author(s) 2018. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import sys
import json
import os
from minio import Minio
from function import *
from sys import argv

node_ip = argv[1]
minio_access_key = argv[2]
minio_secret_key = argv[3]
source_bucket = argv[4]
dest_bucket = argv[5]

class MinIO:
    def __init__(self):
        self.client = None

    def create_client(self, *args, **kwargs):
        ip = kwargs.get('ip', "localhost")
        access_key = kwargs.get('access_key', None)
        secret_key = kwargs.get('secret_key', None)
        self.client = Minio(ip + ':9000',
                            access_key=access_key,
                            secret_key=secret_key,
                            secure=False)

    def retrieve_from_bucket(self, source_bucket, file_name):
        try:
            self.client.fget_object(source_bucket, file_name, "/tmp/" + file_name)
        except Exception as e:
            raise Exception("There was an error retrieving object from the bucket: " + str(e))

    def store_to_bucket(self, destination_bucket, file_name, img_path):
        try:
            self.client.fput_object(destination_bucket, file_name, img_path)
        except Exception as e:
            raise Exception("There was an error storing object to the bucket: " + str(e))

def convert_push(source_bucket, dest_bucket, file_name, object_store):
    object_store.retrieve_from_bucket(source_bucket, file_name)
    input_file_path = '/tmp/{}'.format(file_name)
    output_file_path = '/tmp/converted-{}'.format(file_name)

    rpi_function(input_file_path, output_file_path)
    name = file_name.split(".")[0]
    extension = file_name.split(".")[1]
    dest_file_name = name + "-converted." + extension
    object_store.store_to_bucket(dest_bucket, dest_file_name, output_file_path)

def handle(st):
    req = json.loads(st)
    minio_object_storage = MinIO()
    minio_object_storage.create_client(ip=node_ip, access_key=minio_access_key, secret_key=minio_secret_key)

    for obj in req['Records']:
        filename = obj['s3']['object']['key']
        convert_push(source_bucket, dest_bucket, filename, minio_object_storage)

def get_stdin():
    buf = ""
    while (True):
        line = sys.stdin.readline()
        buf += line
        if line == "":
            break
    return buf


if __name__ == "__main__":
    st = get_stdin()
    ret = handle(st)
    if ret is not None:
        print(ret)
