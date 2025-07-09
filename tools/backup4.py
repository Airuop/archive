import os
import requests
import base64
import re
from datetime import datetime

update_path = './countries/ir/'

urls = [
    "https://raw.githubusercontent.com/itsyebekhe/PSG/refs/heads/main/subscriptions/location/base64/IR"
]

servers = []

for link in urls:
    while True:
        res = requests.get(link)
        if res.ok:
            break
        if res.status_code == 404:
            break

    if res.status_code != 404:
        print(f"Fetched: {link}")
        encoded_str = res.content
        decoded_bytes = base64.b64decode(encoded_str)
        decoded_str = decoded_bytes.decode('utf-8')

        # Keep Unicode if you want, or remove non-ASCII
        cleaned_str = re.sub(r'[^\x00-\x7F\n]+', '', decoded_str)
        # split into list of lines
        servers.extend(cleaned_str.strip().split('\n'))

    else:
        print("WARNING: ERROR 404 _________________________")
        print(f"WARNING: Not Found: {link}")
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
            for line in servers:
                f.write(line.strip() + "\n")
        print(f"Backup saved to {file_path}")
    except OSError:
        print("Error writing backup file")


print(f"Servers fetched: {len(servers)}")

if servers:  # only backup if there is at least one line
    backup(servers)
else:
    print("No servers to backup.")
