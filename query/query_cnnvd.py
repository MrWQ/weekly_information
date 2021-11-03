# -*- coding: utf-8 -*-
# @Time : 2021/11/2 16:23
# @Author : ordar
# @Project : weekly_information
# @File : query_cnnvd.py
# @Python: 3.7.5
# http://cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD=CNNVD-202110-1989
from config import UA,TIMEOUT
import requests
import re


class CNNVD:
    def get_html(self, cnnvd):
        """
        获取cnnvd详情页
        :param cnnvd:
        :return:
        """
        query_url = "http://cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD={}".format(cnnvd)
        try:
            resp = requests.get(url=query_url, headers=UA().get_ua(), timeout=TIMEOUT)
        except TimeoutError:
            self.get_html(cnnvd)
        html = resp.text
        return html

    def parse_level(self, cnnvd_html):
        """
        从漏洞详情页面中解析出cwe，默认只解析出一个，不知道会不会有bug
        :param cnnvd_html:
        :return:
        """
        level = ""
        try:
            level = re.findall(r'<li><span>危害等级：.*?(\w{1}危)\n', cnnvd_html)
            if level:
                level = level[0]
        except:
            pass
        return level

    def parse_type(self, cnnvd_html):
        """
        从漏洞详情页面中解析出cwe，默认只解析出一个，不知道会不会有bug
        :param cnnvd_html:
        :return:
        """
        type = ""
        try:
            # print([cnnvd_html])
            type = re.findall(r'<a style="color:#4095cc;cursor:pointer;"> +\n+\t+(\w+)\n+\t+</a>', cnnvd_html)
            if type:
                type = type[0]
        except:
            pass
        return type

    def query_level(self, cnnvd):
        """
        查询漏洞登记
        :param cnnvd:
        :return:
        """
        return self.parse_level(self.get_html(cnnvd))

    def query_type(self, cnnvd):
        """
        查询漏洞类型
        :param cnnvd:
        :return:
        """
        return self.parse_type(self.get_html(cnnvd))


if __name__ == '__main__':
    cnnvd = "CNNVD-202111-168"
    cnnvd = "CNNVD-202110-2013"
    nvd = CNNVD()
    print(nvd.query_level(cnnvd))
    print(nvd.query_type(cnnvd))
