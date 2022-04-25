import base64


def image2base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read())
