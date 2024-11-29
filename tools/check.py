import requests
import json
import time

path = './donated/2308'
API_URL = 'https://check-host.net/check-ping'  
RESULTS_URL = 'https://check-host.net/check-result/'

with open(f'{path}/final.txt') as f:
  servers = f.read().splitlines()

servers_added = []
server_counter = 0
print('start for: ',len(servers),'servers.🌿🌿🌿🌿🌿🌿')


for server in servers:
  print('🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻')
  server_counter += 1
  print('server ',server_counter," Checking: ")

  if '@' in server:
    host = server.split('@')[1].split(':')[0]
  else:
    continue

  nodes = [ ##'ir1.node.check-host.net', down
           'ir2.node.check-host.net',
           'ir3.node.check-host.net',
           'ir4.node.check-host.net',
           'ir5.node.check-host.net',
           'ir6.node.check-host.net']

  params = {'host': host, 'node': nodes}
  headers = {'Accept': 'application/json'}

  response = requests.get(API_URL, params=params, headers=headers)

  data = response.json()

  if 'request_id' not in data:
    print(f"No request_id for {server}, skipping") 
    continue

  request_id = data['request_id']

  results_url = RESULTS_URL + request_id

  result_response = requests.get(results_url)
  result = json.loads(result_response.content)

  while None in result.values():
    result_response = requests.get(results_url)
    result = json.loads(result_response.content)

  total_ok = 0
  min_ok_nodes = 2

  for node, node_result in result.items():
    print(node)
    print(node_result)

    if node_result is not None:
      if isinstance(node_result, list) and len(node_result) > 0 and isinstance(node_result[0], list) and len(node_result[0]) > 0:
          if node_result[0][0] is None:
              # Handle the case where the first element is None
              print("The first element is None.")
              continue
      else:
          print("node_result is empty or the first element is empty.")
          continue
    else:
      print("node_result is None.")
      continue
    
    print('➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖')
    for s in node_result[0][0]:
        if s == "OK":
          total_ok += 1

  if total_ok >= min_ok_nodes:
      print('server ',server_counter," res: ✅")
      servers_added.append(server)
  else:
       print('server ',server_counter,"res: ❌")

with open(f'{path}/serversChecked.txt', 'w') as f:
  for server in servers_added:
    f.write(server + '\n')

print(f"{len(servers_added)} servers saved. 🌿🌿🌿🌿🌿🌿")
