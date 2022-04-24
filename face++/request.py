import json
import os

import requests
from tqdm import tqdm

from utils import image2base64

api_key = 'J-6Jp3xZnr1hvGvBkFO8oDIpFZ_V04q7'
api_secret = 'eRjC4kHtLV75dZeNcoWrYnJrGLuWqstD'


def request_face_plus_plus(image_path, outfile):
    try:
        endpoint = "https://api-cn.faceplusplus.com/facepp/v1/face/thousandlandmark"

        image_base64 = image2base64(image_path)
        response = requests.post(endpoint, data={
            "api_key": api_key,
            "api_secret": api_secret,
            "image_base64": image_base64,
            "return_landmark": "all"
        })

        face_landmarks = response.json()
        with open(outfile, "w") as out:
            json.dump(face_landmarks, out, ensure_ascii=False)

    except Exception as e:
        print(f"Failure, {e}")


if __name__ == "__main__":
    root = "../../makeup-crawler/data/images"

    files = []

    with open('not.txt', 'r') as f:
        lines = map(lambda s: s.strip('\n'), f.readlines())
        files.extend(lines)

    print(files[:3])

    for image_file in tqdm(sorted(files), desc="Processing images"):
        path = os.path.join(root, image_file)
        request_face_plus_plus(path, f"response/{image_file}.json")
