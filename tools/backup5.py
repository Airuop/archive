import os
import requests
import base64
import time
import re
from datetime import datetime

update_path = './donated/'

url = "https://api.yebekhe.link/telegramDonated/"
res = requests.get(url)
while True:
      time.sleep(10)
      res = requests.get(url)  
      if res.ok:
          break

encoded_str = res.content
decoded_bytes = base64.b64decode(encoded_str)
decoded_str = decoded_bytes.decode('utf-8') 

# Remove unsupported characters before encoding
cleaned_str = re.sub(r'[^\x00-\x7F]+', '', decoded_str)  

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

backup(cleaned_str)
