import os
import requests
import time
from datetime import datetime

update_path = './fail/'

url = 'https://raw.githubusercontent.com/Airuop/vpnfail/refs/heads/main/subscription/plain'
response = requests.get(url)
while True:
      time.sleep(10)
      response = requests.get(url)
      if response.ok:
          break

def backup(response):
  date_dir = datetime.now().strftime("%y%m")
  date_file = datetime.now().strftime("%y%m%d_%H%M") + "C"

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
          f.write(line + '\n')
  except OSError:
    print("Error writing backup file")

backup(response)
