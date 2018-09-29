#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/25/025 18:46
# @Author  : K_oul
# @File    : search_word.py
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
        try:
            r = self.session.get(url)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except Exception as e:
            print('请求api出错 : '.format(url), e)

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

    def get_data(self, url, device='0', key='hot'):
        '''
        请求api获取数据
        :param url: api
        :param cate_id: 类目id
        :param device: 终端选择： 所有 '0'， PC端 '1'， 无线端 '2'
        :param key: 热搜 hot 或者 飙升 soar
        :return:包含字典的列表
                key = 'hot'
                searchWord: 关键词,
                seIpvUvHits: 搜索人气,
                p4pRefPrice: 直通车参考价,
                payRate: 支付转化率,
                tmClickRate: 0.6784295432866173,
                soarRank: 0,
                orderNum: 0,
                hotSearchRank: 热搜排名,
                clickRate: 点击率,
                clickHits: 点击人气

                key = 'soar'
                soarRank: 飙升排名,
                seRiseRate: 搜索增长幅度,
                orderNum: 0,
                hotSearchRank: 0,
                p4pRefPrice: 直通车参考价,
                payRate: 支付转化率,
                clickHits: 点击人气,
                clickRate: 点击率,
                searchWord: 关键词,
                seIpvUvHits: 搜索人气
        '''
        cates = self.get_cate()
        if cates:
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
            }
            url += urlencode(params)
            # print(url)
            html = self.get_text(url)
            datas = json.loads(html).get('data')
            if key == 'hot':
                res = datas.get('hotList')
                return res
            elif key == 'soar':
                res = datas.get('soarList')
                return res
            else:
                print('key关键词错误！')
                return None

    def get_search_word(self, device='0', key='hot'):
        '''
        获取搜索词
        :param cate_id: 类目id
        :param device: 所有 '0'， PC端 '1'， 无线端 '2'
        :param key: 热搜 hotList ，飙升
        :return:搜索词列表
        '''
        searchWord_api = 'https://sycm.taobao.com/mc/industry/searchWord.json?'
        return self.get_data(searchWord_api, device=device, key=key)

if __name__ == '__main__':
    spider = Spider()

    print(spider.get_search_word( device='0', key='hot'))
    print(spider.get_search_word( device='0', key='soar'))
