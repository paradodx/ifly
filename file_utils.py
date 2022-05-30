import json


def save_data(file_name, json_flag=False, info='', coding='utf-8'):
    f = open(file_name, 'w', encoding=coding)
    if json_flag:
        f.write(json.dumps(info, ensure_ascii=False))
    else:
        f.write(info)
    f.flush()
    f.close()


def get_data(filename, json_flag=True, strip_flag=False):
    
    datas = []
    with open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            if line.startswith(u'\ufeff'):
                line = line.encode('utf8')[3:].decode('utf8')
            if strip_flag:
                line = line.strip()
            datas.append(json.loads(line) if json_flag else line)
    return ''.join(datas)


def save_datas(file_name, json_flag=False, infos=None):
    f = open(file_name, 'w', encoding='utf-8')
    for info in infos:
        if json_flag:
            try:
                f.write(json.dumps(info, ensure_ascii=False))
            except Exception as e:
                print(f'error: {e} \n txt: {info}')
        else:
            f.write(info)
        f.write('\n')
    f.flush()
    f.close()


def get_datas(filename, json_flag=True, all_flag=False, strip_flag=True):
    datas = []

    if all_flag:
        texts = []
        with open(filename, encoding='UTF-8') as f:
            for line in f.readlines():
                if line.startswith(u'\ufeff'):
                    line = line.encode('utf8')[3:].decode('utf8')
                if strip_flag:
                    line = line.strip()
                texts.append(line.strip() if strip_flag else line)
        data = ''.join(texts)
        datas.append(json.loads(data) if json_flag else data)
        return datas

    with open(filename, encoding='UTF-8') as f:
        for line in f.readlines():
            if line.startswith(u'\ufeff'):
                line = line.encode('utf8')[3:].decode('utf8')
            if strip_flag:
                line = line.strip()
            datas.append(json.loads(line) if json_flag else line)
    return datas

