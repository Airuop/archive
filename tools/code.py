import os
import re
import natsort


paths = ['./countries/ir/2311', './update/2311', './donated/2311']

def chunk_file(file_path, chunk_size=90*1024*1024):
  print(file_path)

  counter = 1

  with open(file_path, 'rb') as f:
    chunk = f.read(chunk_size)

    while chunk:
      chunk_name = f'{file_path.removesuffix(".txt")}-part{counter}.txt'

      with open(chunk_name, 'wb') as chunk_file:
        chunk_file.write(chunk)

      counter += 1
      chunk = f.read(chunk_size)

  os.remove(file_path) #remove original file after chunking

def changeName(name, path):
  chunked_files = []
  for file in os.listdir(path):
    if name in file:
      chunked_files.append(file)

      if len(chunked_files) == 1:
        new_name = file.replace('-part1', '')
        os.rename(os.path.join(path, file), os.path.join(path, new_name))

def get_all_paths(path):
    all_files = []
    for root, dirs, files in os.walk(path, topdown=False):
      #print('root=%s , files=%s' %(root, files))
      for file_name in files:
        all_files.append(os.path.join(root, file_name))
        #print(all_files)
    return all_files

def merge_files(all_files, output_file):
    with open(output_file, 'a') as fout:
      for file in all_files:
        if file.endswith(".txt"):
          with open(file) as fin:
            fout.write(fin.read())
            fout.write('\n')
    

for path in paths:
  
  output_file = f'{path}/integrated.txt'
  output_file_final = f'{path}/final.txt'
  # Remove old final and integrated files
  for file in os.listdir(path):
    if 'integrated' in file or 'final' in file:
      file_path = os.path.join(path, file)
      os.remove(file_path)

  all_files = get_all_paths(path)
  merge_files(all_files, output_file)

  with open(output_file) as f:
    lines = f.readlines()
    
  chunk_file(output_file)

  keys = []
  for line in lines:
    print(line)
    match = re.search(r'@([^?]+)?\s*(\S+)', line)
    if match:
      key = match.group(1)
    else:
      key = '0'
    keys.append(key)
  #print('key = %s , keys=%s' %(key, keys))
  sorted_lines = [lines[keys.index(key)] for key in natsort.natsorted(keys)]


  deduped_lines = []
  for line in sorted_lines:
    if line not in deduped_lines:
      deduped_lines.append(line)

  final_lines = []
  for line in deduped_lines:
    protocols = ['vless://']
    for protocol in protocols:
      regex = re.compile(f"^{protocol}(.*)")
      match = regex.match(line)
      if match:
        final_lines.append(match.group())

  with open(output_file_final, 'w') as outfile:
    for line in final_lines:
      outfile.write(line + '\n')

  chunk_file(output_file_final)
  changeName('final',path)
  changeName('integrated',path)
  print(f"Server cleanup completed for {path}... !")
