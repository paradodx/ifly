
UNICODE_DICT = {
    'juchaoqu_zhongzhen': '中垾镇',
    'juchaoqu_tongzhen': '烔炀镇',
    'juchaoqu_gaozhen_shancun': '峏山村'
}


def neat_url(url=''):
    return url.replace(':', '').replace('/', '')


def neat_error_unicode(txt='', condition=''):
    res = [v for k, v in UNICODE_DICT.items() if k in condition]
    return res[0] if res else txt


def neat_unknown_gbk_code(txt):
    unknown_gbk_codes = ['\u2022', '\ufeff', '\ufffd', '\xb2', '\xb4', '\xa0', '\u2027', '\xce', '\xe2', '\xd0',
                         '\xc2', '\xcc', '\xef', '\xd5', '\xbc', '\xbe', '\xdd', '\xc9', '\xc4']
    for _code in unknown_gbk_codes:
        txt = txt.replace(_code, '')
    return txt


def neat_unknown_gbk_codes(info=None):
    res = {}
    for k, v in info.items():
        k = neat_unknown_gbk_code(k)
        if isinstance(v, dict):
            res[k] = neat_unknown_gbk_codes(v)
        elif isinstance(v, list):
            if v:
                ele = v[0]
                if isinstance(ele, dict):
                    res[k] = [neat_unknown_gbk_codes(ele) for ele in v]
                elif isinstance(ele, str):
                    res[k] = [neat_unknown_gbk_code(ele) for ele in v]
                else:
                    print(f'not support type: {type(v)}\t{(k, v)}')
                    res[k] = v
            else:
                res[k] = v
        elif isinstance(v, str):
            res[k] = neat_unknown_gbk_code(v)
        else:
            res[k] = v
            print(f'not support type: {type(v)}\t{(k, v)}')
    return res


def neat_area_name(area_name=''):
    return area_name.replace('市', '')


def get_url_pre(url=''):
    return url[:url.rindex('/')+1]


def neat_blank(txt=''):
    return txt.replace('\n', '').replace(' ', '').strip()
