import os
import requests
from datetime import datetime

update_path = './update/'

url = 'https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/reality'
data = requests.get(url).text


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
