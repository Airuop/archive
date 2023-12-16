import os
import requests
import base64
import re
import time
from datetime import datetime

update_path = './countries/ir/'

url = ["https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/countries/ir/mixed",
       "https://raw.githubusercontent.com/Airuop/TelegramV2rayCollector/main/country/IR/base64"]

servers = []

for link in url:
    res = requests.get(link)
    while True:
        res = requests.get(link)
        if res.ok:
            break
        if res.status_code == 404:
            break
              
    if res.status_code != 404:
      print(link)
      print(res.content)
      encoded_str = res.content
      decoded_bytes = base64.b64decode(encoded_str)
      decoded_str = decoded_bytes.decode('utf-8')
      cleaned_str = re.sub(r'[^\x00-\x7F]+', '', decoded_str)
      servers.append(cleaned_str + '\n')
           
    if res.status_code == 404:
        print("WARNING: ERROR 404 _________________________")
        print("WARNING: Not Found_____")
        print("WARNING: Link:")
        print()
        print(url)
        print()

def backup(servers):
  date_dir = datetime.now().strftime("%y%m")
  date_file = datetime.now().strftime("%y%m%d_%H%M")

  try:
    os.makedirs(f"{update_path}/{date_dir}", exist_ok=True)
  except OSError:
    print("Error creating backup directory")
    return

  file_path = f"{update_path}/{date_dir}/{date_file}.txt"

  try:  
    with open(file_path, "w", encoding="utf-8") as f:
            for server in servers:
                  f.write(server)
  except OSError:
    print("Error writing backup file")

backup(servers)
