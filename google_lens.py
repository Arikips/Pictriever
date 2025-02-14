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
        fake_chromium_config = {
            'viewport': (1920, 1080),
            'major_version': '109',
            'version': '109.0.5414.87',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.87 Safari/537.36'
        }

        url = 'https://lens.google.com/v3/upload'
        files = {'encoded_image': ('image.png', self._preprocess(img), 'image/png')}
        params = {
            'ep': 'ccm', #EntryPoint
            're': 'dcsp', #RenderingEnvironment - DesktopChromeSurfaceProto
            's': '4', #SurfaceProtoValue - Surface.CHROMIUM
            'st': str(int(time.time() * 1000)),
            'sideimagesearch': '1',
            'vpw': str(fake_chromium_config['viewport'][0]),
            'vph': str(fake_chromium_config['viewport'][1])
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://lens.google.com',
            'Referer': 'https://lens.google.com/',
            'Sec-Ch-Ua': f'"Not A(Brand";v="99", "Google Chrome";v="{fake_chromium_config["major_version"]}", "Chromium";v="{fake_chromium_config["major_version"]}"',
            'Sec-Ch-Ua-Arch': '"x86"',
            'Sec-Ch-Ua-Bitness': '"64"',
            'Sec-Ch-Ua-Full-Version': f'"{fake_chromium_config["version"]}"',
            'Sec-Ch-Ua-Full-Version-List': f'"Not A(Brand";v="99.0.0.0", "Google Chrome";v="{fake_chromium_config["major_version"]}", "Chromium";v="{fake_chromium_config["major_version"]}"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Model': '""',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Ch-Ua-Platform-Version': '"15.0.0"',
            'Sec-Ch-Ua-Wow64': '?0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': fake_chromium_config['user_agent'],
            'X-Client-Data': 'CIW2yQEIorbJAQipncoBCIH+ygEIkqHLAQiKo8sBCPWYzQEIhaDNAQji0M4BCLPTzgEI19TOAQjy1c4BCJLYzgEIwNjOAQjM2M4BGM7VzgE='
        }
        cookies = {'SOCS': 'CAESEwgDEgk0ODE3Nzk3MjQaAmVuIAEaBgiA_LyaBg'}

        try:
            start_time = time.time()
            res = requests.post(url, files=files, params=params, headers=headers, cookies=cookies, timeout=20)
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
