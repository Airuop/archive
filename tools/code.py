
import os
import re
import natsort

folder = './update/2308/'
output_file_final = f'{folder}/final.txt'

txt_files = [f for f in os.listdir(folder) if f.endswith('.txt')]

lines = []
for txt_file in txt_files:
    with open(os.path.join(folder, txt_file)) as f:
        lines.extend(f.readlines())

keys = []
for line in lines:
    match = re.search(r'@([^:]+):\s*(\S+)', line)
    if match:
        key = match.group(1)
    else:
        key = ''
    keys.append(key)

sorted_lines = [lines[keys.index(key)] for key in natsort.natsorted(keys)]

duplicates = []
seen = set()
regex = r'[@][^?]*[?]'

for line in sorted_lines:
    match = re.search(regex, line)
    if match:
        val = match.group()
        if val in seen:
            duplicates.append(line)
        else:
            seen.add(val)

deduped_lines = []
for line in sorted_lines:
    if line not in deduped_lines:
        deduped_lines.append(line)

final_lines = []

for line in deduped_lines:
    if 'vless://' in line:
        links = line.split('vless://')
        for link in links:
            if link:
                final_lines.append('vless://' + link.strip())
    else:
        final_lines.append(line)

with open(output_file_final, 'w') as outfile:
    for line in final_lines:
        outfile.write(line + '\n')
    print("Server cleanup completed... !"+"\n")
