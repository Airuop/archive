import requests
import json
import time

path = './update/2308'
API_URL = 'https://check-host.net/check-ping'
RESULTS_URL = 'https://check-host.net/check-result/'  

with open(f'{path}/final.txt') as f:
  servers = f.read().splitlines()

servers_added = [] # Use list instead of set

for server in servers:

  if '@' in server:
    host = server.split('@')[1].split(':')[0]
  else:
    continue

  nodes = ['ir4.node.check-host.net',
           'ir3.node.check-host.net',  
           'ir1.node.check-host.net']

  params = {'host': host, 'node': nodes}
  headers = {'Accept': 'application/json'}

  response = requests.get(API_URL, params=params, headers=headers)

  data = response.json()
  request_id = data['request_id']

  results_url = RESULTS_URL + request_id

  result_response = requests.get(results_url)
  result = json.loads(result_response.content)

  while None in result.values():
    print("Waiting for results...")
    time.sleep(2)
    result_response = requests.get(results_url)
    result = json.loads(result_response.content)

  print(result)

  total_ok = 0
  min_ok_nodes = 2

  for node, node_result in result.items():
    for status in node_result[0][0]:
      if status == "OK":
         total_ok += 1

  if total_ok >= min_ok_nodes: # Check threshold
    servers_added.append(server) # Add to list

with open(f'{path}/serversChecked.txt', 'w') as f:
  for server in servers_added:
    f.write(server + '\n') 

print(f"{len(servers_added)} servers saved")
