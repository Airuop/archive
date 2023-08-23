import os
import requests
from datetime import datetime

update_path = './update/'

url = 'https://raw.githubusercontent.com/shabane/kamaji/master/hub/tested/vless.txt'
response = requests.get(url)


def backup(response):
  date_dir = datetime.now().strftime("%y%m") + "S"
  date_file = datetime.now().strftime("%y%m%d_%H%M")

  try:
    os.makedirs(f"{update_path}/{date_dir}", exist_ok=True)
  except OSError:
    print("Error creating backup directory")
    return

  file_path = f"{update_path}/{date_dir}/{date_file}.txt"

  try:  
    with open(file_path, "w", encoding="utf-8") as f:
      for line in response.text.splitlines():
          line = line.replace('&amp;', '&')
          if 'security=reality' in line:
            f.write(line + '\n')
  except OSError:
    print("Error writing backup file")

backup(response)
