import os
import requests
import time
from datetime import datetime

update_path = './update/'

url = 'https://raw.githubusercontent.com/Airuop/TelegramV2rayCollector/dev/sub/normal/reality'
data = requests.get(url).text
while True:
      time.sleep(10)
      data = requests.get(url).text
      if requests.get(url).ok:
          break

def backup(data):
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
      f.write(data)
  except OSError:
    print("Error writing backup file")

backup(data)
