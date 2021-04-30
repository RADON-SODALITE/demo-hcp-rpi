from PIL import Image

THUMBNAIL_SIZES_PX = [200]

def rpi_function(input_file_path, output_file_path):
    with Image.open(input_file_path) as image:
        ratio = max(image.size) / float(THUMBNAIL_SIZES_PX[0])
        image.thumbnail(tuple(int(x / ratio) for x in image.size))
        image.save(output_file_path)