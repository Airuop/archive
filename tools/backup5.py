import os
import requests
import base64
import time
import re
from datetime import datetime

def backup(response):
  date_dir = datetime.now().strftime("%y%m")
  date_file = datetime.now().strftime("%y%m%d_%H%M") + "M"

  try:
    os.makedirs(f"{update_path}/{date_dir}", exist_ok=True)
  except OSError:
    print("Error creating backup directory")
    return

  file_path = f"{update_path}/{date_dir}/{date_file}.txt"

  try:  
    with open(file_path, "w", encoding="utf-8") as f:
            f.write(response)
  except OSError:
    print("Error writing backup file")

print("py code try for get data...")
update_path = './donated/'

MAX_ATTEMPTS = 10
BACKOFF_DELAY = 10  # in seconds

url = "https://api.yebekhe.link/telegramDonated/"

for attempt in range(MAX_ATTEMPTS):
    try:
        res = requests.get(url, timeout=10)  # Set a timeout to avoid hanging
        if res.ok:
            break
    except requests.exceptions.ProxyError as e:
        print(f"Proxy error on attempt {attempt + 1}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request error on attempt {attempt + 1}: {e}")
    print(f"Try {attempt + 1}..... (retrying in {BACKOFF_DELAY} seconds)")
    time.sleep(BACKOFF_DELAY)
else:
    print(f"Failed to retrieve the URL after {MAX_ATTEMPTS} attempts")
    res = 0

if res != 0:      
    encoded_str = res.content
    decoded_bytes = base64.b64decode(encoded_str)
    decoded_str = decoded_bytes.decode('utf-8') 

    # Remove unsupported characters before encoding
    cleaned_str = re.sub(r'[^\x00-\x7F]+', '', decoded_str)  
    backup(cleaned_str)
