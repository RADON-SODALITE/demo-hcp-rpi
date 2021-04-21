import json
from PIL import Image
from .minio_handler import MinIO
import os

THUMBNAIL_SIZES_PX = [100, 160, 200]

node_ip = "192.0.2.0"
minio_access_key = "AKIAIOSFODNN7EXAMPLE"
minio_secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"


def convert_push(source_bucket, dest_bucket, file_name, object_store):
    object_store.retrieve_from_bucket(source_bucket, file_name)
    original_img = '/tmp/{}'.format(file_name)
    temp_img = '/tmp/resize-{}'.format(file_name)

    for size_px in THUMBNAIL_SIZES_PX:
        resize_image(original_img, temp_img, size_px)
        dest_file_name = file_name.replace(".jpg", "") + "-resized-" + str(size_px)
        object_store.store_to_bucket(dest_bucket, dest_file_name, temp_img)


def resize_image(original_img_path, resized_img_path, new_size_px):
    with Image.open(original_img_path) as image:
        ratio = max(image.size) / float(new_size_px)
        image.thumbnail(tuple(int(x / ratio) for x in image.size))
        image.save(resized_img_path)


def handle(st):
    req = json.loads(st)
    minio_object_storage = MinIO()
    minio_object_storage.create_client(ip=node_ip, access_key=minio_access_key, secret_key=minio_secret_key)

    source_bucket = "original"
    dest_bucket = "resized"

    for obj in req['Records']:
        filename = obj['s3']['object']['key']
        convert_push(source_bucket, dest_bucket, filename, minio_object_storage)
