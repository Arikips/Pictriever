import time
import requests
import pyjson5
from PIL import Image
from io import BytesIO
import re

class GoogleLens:
    def __init__(self):
        self.regex = re.compile(r">AF_initDataCallback\(({key: 'ds:1'.*?)\);</script>")

    def __call__(self, img):
        timestamp = int(time.time() * 1000)
        url = f'https://lens.google.com/v3/upload?stcs={timestamp}'
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 13; RMX3771) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.144 Mobile Safari/537.36'}
        cookies = {'SOCS': 'CAESEwgDEgk0ODE3Nzk3MjQaAmVuIAEaBgiA_LyaBg'}
        files = {'encoded_image': ('image.png', self._preprocess(img), 'image/png')}

        try:
            start_time = time.time()
            res = requests.post(url, files=files, headers=headers, cookies=cookies, timeout=20)
            res.raise_for_status()
            end_time = time.time()
        except requests.exceptions.RequestException as e:
            return (False, str(e), 0)

        match = self.regex.search(res.text)
        if not match:
            return (False, 'Regex error!', 0)

        lens_object = pyjson5.loads(match.group(1))
        if 'errorHasStatus' in lens_object:
            return (False, 'Unknown Lens error!', 0)

        text_data = lens_object['data'][3][4][0]
        extracted_text = '\n'.join(text_data[0]) if text_data else ''
        time_taken = end_time - start_time

        return (True, extracted_text, time_taken)

    def _preprocess(self, img):
        # Convert to grayscale
        img = img.convert('L')

        # Resize to a maximum of 500x500 pixels, maintaining aspect ratio
        max_size = (500, 500)
        img.thumbnail(max_size, Image.LANCZOS)

        output = BytesIO()
        img.save(output, format='PNG')
        return output.getvalue()
