import re
import time
import os

update_path = './Js/'
input_file = './out.txt'

def backup(file):
    try:
        t = time.localtime()
        date = time.strftime('%y%m', t)
        date_day = time.strftime('%y%m%d', t)

        file_eternity = open(file, 'r', encoding='utf-8')
        sub_content = file_eternity.read()
        file_eternity.close()

        try:
            os.mkdir(f'{update_path}{date}')
        except FileExistsError:
            pass
        txt_dir = update_path + date + '/' + date_day + '.txt'  # 生成$MM$DD.txt文件名
        file = open(txt_dir, 'w', encoding='utf-8')
        file.write(sub_content)
        file.close()
    except Exception as e:
        print("Error While backup")


backup(input_file)
