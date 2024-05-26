import os
# import re
# import natsort


# paths = ['./countries/ir/', './update/', './donated/', './selected/']
paths = ['./donated/']

def chunk_file(file_path, chunk_size=90*1024*1024):
    print("chunk_file state")

    counter = 1

    with open(file_path, 'rb') as f:
        chunk = f.read(chunk_size)

        while chunk:
            chunk_name = f'{file_path.removesuffix(".txt")}-part{counter}.txt'

            with open(chunk_name, 'wb') as chunk_file:
                chunk_file.write(chunk)

            counter += 1
            chunk = f.read(chunk_size)

    os.remove(file_path)  # remove original file after chunking


def changeName(name, path):
    print("changeName state")
    chunked_files = []
    for file in os.listdir(path):
        if name in file:
            chunked_files.append(file)

            if len(chunked_files) == 1:
                new_name = file.replace('-part1', '')
                os.rename(os.path.join(path, file),
                          os.path.join(path, new_name))


def get_all_paths(path):
    print("get_all_paths state")
    all_files = []
    for root, dirs, files in os.walk(path, topdown=False):
        # print('root=%s , files=%s' %(root, files))
        for file_name in files:
            all_files.append(os.path.join(root, file_name))
            # print(all_files)
    return all_files


def merge_files(all_files, output_file):
    print("merge_files state")
    with open(output_file, 'a') as fout:
        for file in all_files:
            if file.endswith(".txt"):
                with open(file) as fin:
                    fout.write(fin.read())
                    fout.write('\n')


for path in paths:

  output_file = f'{path}/integrated.txt'
  output_file_ss = f'{path}/shadowsocks.txt'
  output_file_vless = f'{path}/vless.txt'
  output_file_vmess = f'{path}/vmess.txt'
  output_file_others = f'{path}/others.txt'
  # Remove old final and integrated files

  for file in os.listdir(path):
          if 'integrated' in file or 'ss' in file or 'shadowsocks' in file or 'others' in file  or 'final' in file:
              file_path = os.path.join(path, file)
              os.remove(file_path)

  all_files = get_all_paths(path)
  merge_files(all_files, output_file)

  with open(output_file) as f:
      lines = f.readlines()


  # keys = []
  # for line in lines:
  #   print(line)
  #   match = re.search(r'@([^?]+)?\s*(\S+)', line)
  #   if match:
  #     key = match.group(1)
  #   else:
  #     key = '0'
  #   keys.append(key)
  # #print('key = %s , keys=%s' %(key, keys))
  # sorted_lines = [lines[keys.index(key)] for key in natsort.natsorted(keys)]


  deduped_lines = []
  # replace sorted_lines with lines
  for line in lines:
      if line not in deduped_lines:
          deduped_lines.append(line)

  ssLi = []
  vlessLi = []
  vmessLi = []
  othersLi = []

  for line in deduped_lines:
      protocol = line.split("://")[0]
      if protocol == 'ss':
          ssLi.append(line)
      elif protocol == 'vless':
          vlessLi.append(line)
      elif protocol == 'vmess':
          vmessLi.append(line)
      else:
          othersLi.append(line)

  with open(output_file_ss, 'w') as outfile:
      for line in ssLi:
          outfile.write(line)

  with open(output_file_vless, 'w') as outfile:
      for line in vlessLi:
          outfile.write(line)

  with open(output_file_vmess, 'w') as outfile:
      for line in vmessLi:
          outfile.write(line)

  with open(output_file_others, 'w') as outfile:
      for line in othersLi:
          outfile.write(line)

  chunk_file(output_file)
  chunk_file(output_file_ss)
  chunk_file(output_file_vless)
  chunk_file(output_file_vmess)
  chunk_file(output_file_others)
    
  changeName('shadowsocks', path)
  changeName('vless', path)
  changeName('vmess', path)
  changeName('others', path)
  changeName('integrated', path)
