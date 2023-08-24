import requests
import json
import time

path = './update/2308'
API_URL = 'https://check-host.net/check-ping'
RESULTS_URL = 'https://check-host.net/check-result/'

with open(f'{path}/final.txt') as f:
    servers = f.read().splitlines()

servers_added = set()

for server in servers:

    if '@' in server:
        host = server.split('@')[1].split(':')[0]
    else:
        # No '@' found, skip this server
        continue

    nodes = ['ir4.node.check-host.net',
             'ir3.node.check-host.net', 'ir1.node.check-host.net']

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

    all_ok = True

    for node, node_result in result.items():

        for inner_list in node_result:

            status = inner_list[0][0]

            if status != "OK":
                all_ok = False
                break

    if all_ok:
        servers_added.add(server)

with open(f'{path}/serversChecked.txt', 'w') as f:
    for server in servers_added:
        f.write(server + '\n')

print(f"{len(servers_added)} servers saved")
