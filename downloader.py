from request_util import get_html_path
from bs4 import BeautifulSoup
import os
from file_utils import save_datas
from string_utils import *
import re
from collections import OrderedDict


class Downloader(object):
    def __init__(self, url, save_dir='data'):
        self.url = url
        self.save_dir = save_dir
        self.init()

    def init(self):
        if not os.path.exists(self.save_dir):
            os.mkdir(self.save_dir)

    def extract_links(self):
        pass

    def parse_html(self):
        pass

    @staticmethod
    def soup(file_path='', text=''):
        if file_path:
            try:
                return BeautifulSoup(open(file_path, encoding='utf-8'), 'lxml')
            except:
                return BeautifulSoup(open(file_path), 'lxml')

        if text:
            return BeautifulSoup(text)

    def download(self):
        pass


class TCMapDownloader(Downloader):
    """
    http://www.tcmap.com.cn/网站信息爬取
    """
    def __init__(self, url='http://www.tcmap.com.cn/'):
        super().__init__(url)
        self.travel_url = 'http://www.bytravel.cn/'
        self.food_url = 'http://shop.bytravel.cn/'
        self.person_url = 'http://ren.bytravel.cn/'
        self.web = 'tcmap'

    def extract_province_links(self):
        """
        从首页获取省份数据
        :return:
        """
        provinces = []
        ht = self.soup(get_html_path(self.url, web=self.web))
        for ele in ht.select('table')[3].select('td')[1].find_all('a'):
            if 'target' not in ele.attrs and 'world' not in ele['href']:
                provinces.append({neat_blank(ele.text): ele['href']})
            else:
                break
        save_datas(f'{self.save_dir}/area/全国.json', json_flag=True, infos=[provinces])
        return provinces

    def parse_areas(self, area_list=None, area_type=''):
        areas = []
        sub_areas = []
        for area in area_list:
            area_res, sub_area_list = self.parse_area_ht(url=f'{self.url}{list(area.values())[0]}')
            areas.append(area_res)
            sub_areas.extend(sub_area_list)
        save_datas(f'{self.save_dir}/area/{area_type}.json', json_flag=True, infos=areas)
        return sub_areas

    def parse_area_ht(self, url=''):
        """
        解析地区相关信息
        :param url:
        :return:
        """
        area_ht = self.soup(get_html_path(url, web=self.web))

        left = area_ht.find(id='page_left')

        res_dict = {'url': url}

        # 简介解析
        for ele in left.find(style='float:right ').select('td'):
            if ele.find('strong'):
                values = []
                for txt in ele.strings:
                    txt = txt.replace(':', '').replace('\n', '').replace(' ', '').strip()
                    if ':' != txt and txt.strip():
                        values.append(txt)
                if values[0] == '人口密度':
                    values[1] = values[1].replace("km", "平方公里")
                res_dict[values[0]] = values[1]

        # 子区域的信息
        sub_areas = []
        sub_area_elements = left.find_all('table', cellpadding="4")
        if not sub_area_elements:
            sub_area_elements = left.find_all('table', cellpadding="2")
        for ele in sub_area_elements:
            for ele1 in ele.select('tr td strong a'):
                sub_areas.append({neat_error_unicode(ele1.string.strip(), condition=ele1['href']): ele1['href'].strip()})
        res_dict['下级地区'] = sub_areas

        # 介绍信息
        images = {ele['alt']: ele['src'] for ele in left.select('div a img[alt]')}
        res_dict['图片'] = images

        descs = []
        for ele in left.find_all('div', style='margin:5px 10px 1px 10px;')[0].select('p'):
            txts = []
            for txt in ele.strings:
                txt = neat_unknown_gbk_code(txt.replace('\n', '').replace(' ', '').replace('\u3000', '\n'))
                if txt:
                    txts.append(txt)
            descs.append(''.join(txts).strip())
        res_dict['介绍'] = '\n'.join(descs).strip()
        return res_dict, sub_areas

    def parse_area_travels(self, area_list, area_type):
        results = []
        for area in area_list:
            area_name, area_url = tuple(area.items())[0]
            res_dict = self.parse_area_travel_ht(url=f'{self.url}{area_url}', area_name=area_name)
            results.append(res_dict)
        save_datas(f'data/area/{area_type}_travel.json', json_flag=True, infos=results)

    def parse_detail_html(self, url):
        detail_dict = {'url': url}
        detail_ht = self.soup(get_html_path(url, web=self.web))
        left = detail_ht.find(id='page_left')
        images = {ele['alt']: ele['src'] for ele in left.select('div a img[alt]')}
        detail_dict['图片'] = images

        descs = []
        for ele in left.find_all('div', style=re.compile('^margin'))[0].select('p'):
            txts = []
            for txt in ele.strings:
                txt = neat_unknown_gbk_code(txt.replace('\n', '').replace(' ', '').replace('\u3000', '\n'))
                if txt:
                    txts.append(txt)
            descs.append(''.join(txts).strip())
        detail_dict['介绍'] = '\n'.join(descs).strip()

        # TODO: 解析人物间的关系、人物与事件的关系等

        return detail_dict

    def parse_travel_pages(self, travel_more_url='', url_pre=''):
        travel_more_ht = self.soup(get_html_path(travel_more_url, web=self.web))
        travel_page_dict = {'url': travel_more_url}
        travel_page_urls = set([ele['href'] for ele in travel_more_ht.find(id='list-page').select('a[href]')])
        if not travel_page_urls:
            travel_page_urls = {travel_more_url[travel_more_url.rindex('/'):]}

        for travel_page_url in travel_page_urls:
            travel_page_ht = self.soup(get_html_path(f'{get_url_pre(travel_more_url)}{travel_page_url}', web=self.web))
            for travel_ele in travel_page_ht.find_all('div', id=re.compile('tctitle')):
                travel_elea = travel_ele.select('a[href]')[0]
                if not travel_elea.text:
                    continue
                # 景点详情页
                travel_ele_detail_url = f'{url_pre}{travel_elea["href"]}'
                travel_ele_detail_dict = self.parse_detail_html(travel_ele_detail_url)
                travel_ele_detail_dict['name'] = neat_blank(travel_elea.text)

                # 景点标识信息
                flags = []
                travel_ele_span = travel_ele.select('span img')
                if travel_ele_span:
                    for span_ele in travel_ele_span:
                        flags.append(span_ele['alt'] if 'alt' in span_ele.attrs else span_ele['src'])
                travel_ele_span = travel_ele.select('span front')
                if travel_ele_span:
                    for span_ele in travel_ele_span:
                        flags.append(span_ele.text)

                travel_ele_detail_dict['flags'] = flags
                travel_page_dict[neat_blank(travel_elea.text)] = travel_ele_detail_dict
        return travel_page_dict

    def parse_area_travel_ht(self, url='', area_name=''):
        """
        解析地区的景点信息
        :param url:
        :return:
        """

        area_ht = self.soup(get_html_path(url, web=self.web))
        left = area_ht.find(id='page_left')

        res_dict = {'地区url': url, '地区': area_name}

        travel_pres = {
            '文物古迹': self.travel_url,
            '红色旅游': self.travel_url,
            '名人故居': self.travel_url,
            '博物馆': self.travel_url,
            '4A景区': self.travel_url,
            '美食': self.food_url
        }

        for ele in left.find(style='float:right ').select('td[colspan] a'):

            txt = ele.text
            if '旅游' not in txt or (area_name not in txt and neat_area_name(area_name) not in txt):
                continue

            # 地区旅游页面
            travel_init_url = ele['href']
            travel_ht = self.soup(get_html_path(travel_init_url, web=self.web))
            travel_more_ht = travel_ht.find(id='page_left').find(class_='listmore').find('a')
            travel_more_url = travel_more_ht['href'] if travel_more_ht else travel_ht
            travel_more_url = f'{self.travel_url}{travel_more_url}'

            # 获取全部页数的景点信息
            travel_page_dict = self.parse_travel_pages(travel_more_url, self.travel_url)

            # 获取文物古迹|红色旅游|名人故居|博物馆|4A景区|特产|美食
            head_dict = {ele1.text: ele1["href"] for ele1 in travel_ht.find(class_='ht').select('a[href]')}
            for key, value in head_dict.items():
                queries = [(x, travel_pres[x]) for x in travel_pres if x in key]
                if not queries:
                    continue
                if not value.startswith('http://'):
                    value = f'{self.travel_url}{value}'
                res_dict[neat_blank(key)] = self.parse_travel_pages(value, queries[0][1])

            # 特产
            for key, value in head_dict.items():
                if '特产' not in key:
                    continue
                if not value.startswith('http://'):
                    value = f'{self.food_url}{value}'
                tc_ht = self.soup(get_html_path(value, web=self.web))
                tc_more_ht = tc_ht.find(id='page_left').find(class_='listmore').find('a')
                tc_more_url = tc_more_ht['href'] if tc_more_ht else tc_ht
                tc_more_url = f'{get_url_pre(value)}{tc_more_url}'
                res_dict[neat_blank(key)] = self.parse_travel_pages(tc_more_url, self.food_url)

                # 民俗文化
                tc_head_dict = {ele1.text: ele1["href"] for ele1 in tc_ht.find(class_='ht').select('a[href]')}
                for k, v in tc_head_dict.items():
                    if '民俗文化' not in k:
                        continue
                    if not v.startswith('http://'):
                        v = f'{self.food_url}{v}'
                    res_dict[neat_blank(key)] = self.parse_travel_pages(v, self.food_url)

            # 名人
            for key, value in head_dict.items():
                if '名人' not in key or '名人故居' in key:
                    continue
                if not value.startswith('http://'):
                    value = f'{self.person_url}{value}'
                person_ht = self.soup(get_html_path(value, web=self.web))
                person_more_ht = person_ht.find(id='page_left').find(class_='listmore').find('a')
                person_more_url = person_more_ht['href'] if person_more_ht else person_ht
                person_more_url = f'{get_url_pre(value)}{person_more_url}'
                res_dict[neat_blank(key)] = self.parse_travel_pages(person_more_url, self.person_url)

            res_dict['全部景点'] = travel_page_dict
            return res_dict

    def parse_province_hts(self, provinces=None):
        """
        解析整个省份数据
        :param provinces:
        :return:
        """

        # 解析省信息
        cities = self.parse_areas(area_list=[ele for ele in provinces if '安徽' in ele], area_type='province')

        # 解析市信息
        cities = [ele for ele in cities if '合肥市' in ele]
        zones = self.parse_areas(area_list=cities, area_type='city')

        # 解析市旅游信息
        self.parse_area_travels(area_list=cities, area_type='city')

        # 解析区信息
        streets = self.parse_areas(area_list=zones, area_type='zone')

        # 解析区旅游信息
        self.parse_area_travels(area_list=zones, area_type='zone')

        # 解析街道信息
        districts = self.parse_areas(area_list=streets, area_type='street')

        # 解析小区信息
        self.parse_areas(area_list=districts, area_type='district')

    def download(self):
        provinces = self.extract_province_links()
        self.parse_province_hts(provinces=provinces)


class MaigooDownloader(Downloader):
    def __init__(self, url='https://www.maigoo.com/'):
        super().__init__(url)
        self.web = 'maigoo'
        self.province_url = 'https://www.maigoo.com/maigoo/3074ss_index.html'

    def extract_province_links(self):
        """
        提取省信息
        :return:
        """
        ht = self.soup(get_html_path(self.province_url, web=self.web))
        return [{neat_blank(ele.find('span').text): ele['href']} for ele in ht.find(class_='cat').select('a[class]')]

    def extract_city_links(self, provinces=None):
        cities = []
        for province in provinces:
            ht = self.soup(get_html_path(url=list(province.values())[0], web=self.web))
            [cities.append({neat_blank(ele.find('span').text): ele['href']}) for ele in ht.find(class_='cat').select('a[class]')]
        return cities

    def extract_city_ht(self, url):
        ht = self.soup(get_html_path(url, web=self.web))

        info_dict = OrderedDict()
        # 知识体系
        for ele in ht.find(class_=re.compile('zhishitx')).find_all(class_=re.compile('^item')):
            txt = ele.find(class_=re.compile('^rongyutitle')).text.strip()
            txt = txt[1:txt.index('】')]
            href = ele.find('a')['href']
            info_dict[txt] = href

        # 体系文章
        for ele in ht.find(class_='tixilist').find(class_='midcont').find_all(class_=re.compile('^item')):
            txt = ele.find_all('span')[-1].text.strip()
            txt = txt[1:txt.index('】')]
            href = ele['href']
            info_dict[txt] = href

        # 合肥品牌
        info_dict

    def extract_city_hts(self, cities=None):
        results = []
        for city in cities:
            self.extract_city_ht(url=list(city.values())[0])

    def download(self):
        # 省
        provinces = self.extract_province_links()
        provinces = [ele for ele in provinces if '安徽省' in ele]

        # 市
        cities = self.extract_city_links(provinces)
        cities = [ele for ele in cities if '合肥市' in ele]

        # 知识体系
        self.extract_city_hts(cities)


if __name__ == '__main__':
    downloader = MaigooDownloader()
    downloader.download()
