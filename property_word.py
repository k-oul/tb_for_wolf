#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/29/029 9:35
# @Author  : K_oul
# @File    : property_word.py
# @Software: PyCharm


import datetime
import requests
import json
from fake_useragent import UserAgent
from urllib.parse import urlencode
from config import COOKIE, SEARCH_WORD


class Spider:
    def __init__(self):
        '''
        初始化requests配置，添加cookie !!!
        '''
        self.ua = UserAgent()
        self.headers = {
            'user-agent': self.ua.random,
            'cookie': COOKIE
        }
        self.session = requests.session()
        self.session.headers.update(self.headers)

    def get_text(self, url, ):
        '''
        requests请求函数
        :param url:
        :return: Html
        '''
        r = self.session.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text

    def get_cate(self):
        '''
        获取类目id
        :return: 品类id 字典
        '''
        cates = dict()
        cate_api = 'https://sycm.taobao.com/mc/common/getShopCate.json?leaf=true'
        html = self.get_text(cate_api)
        datas = json.loads(html).get('data')
        if datas:
            for data in datas:
                words = data[2].split('/')
                res = {
                    words[0]: data[1],
                }
                cates.update(res)
                if len(words) > 1:
                    for i in range(1,len(words)):
                        cates.update({words[i]: data[1]})
            print(cates)
            return cates
        raise SystemExit('cookie已失效请重新登录')

    def get_yesterday(self):
        '''
        获取昨天的年月日
        :return: 例 2018-09-24
        '''
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        return str(yesterday)

    def get_prop_id(self, cate_id):
        prop_url = 'https://sycm.taobao.com/mc/mq/prop/props.json?cateId={}'.format(cate_id)
        html = self.get_text(prop_url)
        prop_id = json.loads(html).get('data')[0].get('id')
        return prop_id

    def get_data(self, url, device='0', seller='-1'):
        '''
        请求api获取数据
        :param url: api
        :param order_by: 排序规则
        :param cate_id: 类目id
        :param device: 终端选择： 所有 '0'， PC端 '1'， 无线端 '2'
        :param index_code: api请求参数
        :param key: 热搜 hot 或者 飙升 soar
        :return:
        '''
        cates = self.get_cate()
        cate_id = cates.get(SEARCH_WORD)
        if cate_id == None:
            return None
        params = {
            'dateRange': '{0}|{0}'.format(self.get_yesterday()),
            'dateType': 'day',
            'pageSize': '100',
            'page': '1',
            'order': 'desc',
            'cateId': str(cate_id),
            'device': device,
            'propId': self.get_prop_id(cate_id),
            'hotAttrType': '0',
            'seller': seller
        }
        url += urlencode(params)
        print(url)
        html = self.get_text(url)
        datas = json.loads(html).get('data').get('data')
        # res = list()
        # datas = datas.get('hotList')
        # for data in datas:
        #     key_word = data.get('searchWord')
        #     res.append(key_word)
        return datas



    def get_property_word(self):
        '''
        获取品牌词
        :param cate_id: 类目id
        :return: 品牌词
        '''
        propWord_api = 'https://sycm.taobao.com/mc/mq/prop/hotRank.json?'
        return self.get_data(propWord_api)


if __name__ == '__main__':
    spider = Spider()
    print(spider.get_property_word())

