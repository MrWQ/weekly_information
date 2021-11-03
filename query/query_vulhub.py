# -*- coding: utf-8 -*-
# @Time : 2021/11/2 16:22
# @Author : ordar
# @Project : weekly_information
# @File : query_vulhub.py
# @Python: 3.7.5
# http://vulhub.org.cn/vuln/VHN-397978
# http://vulhub.org.cn/vulns?search_type=t_id&keyword=&cvss_floor=&cvss_ceil=&pubtime_floor=2021-10-30&pubtime_ceil=2021-11-26
import requests
import re
import math
from config import UA,TIMEOUT


class VULHUB:
    def __init__(self):
        self.vhn_list = []
        self.all_code = []
        self.cve_list = []
        self.cnnvd_list = []

    def query_html_by_date(self, start_date, end_date, pages=1):
        """
        返回按日期查询结果的指定页码的页面的html。默认返回第一页
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param pages: 页码
        :return:
        """
        query_url = "http://vulhub.org.cn/vulns/{}?search_type=t_id&keyword=&cvss_floor=&cvss_ceil=&pubtime_floor={}&pubtime_ceil={}".format(pages, start_date, end_date)
        resp = requests.get(url=query_url, headers=UA().get_ua(), timeout=TIMEOUT)
        html = resp.text
        return html

    def query_pages(self, start_date, end_date):
        """
        查询总页码数
        :param start_date:
        :param end_date:
        :return:
        """
        html = self.query_html_by_date(start_date,end_date)
        vhn_items = 0
        try:
            vhn_items = re.findall(r'\[共 +(\d+) +条\]', html)
            if vhn_items:
                vhn_items = vhn_items[0]
        except:
            pass
        # 漏洞条数
        # print(vhn_items)
        a = int(vhn_items)/10
        pages = math.ceil(a)
        return pages

    def parse_query_html(self, html):
        """
        解析查询结果html，提取vhn编号
        :param html:
        :return:
        """
        parse_vhn = re.findall(r'<a href="/vuln/(VHN-\d+)">', html)
        return parse_vhn

    def get_all_vhn(self, start_date, end_date):
        """
        指定时间范围，获得所有vhn编号
        :param start_date:
        :param end_date:
        :return:
        """
        pages = self.query_pages(start_date, end_date)
        for page in range(1, 1 + int(pages)):
            self.vhn_list.extend(self.parse_query_html(self.query_html_by_date(start_date, end_date, page)))
        self.vhn_list = list(set(self.vhn_list))
        return self.vhn_list

    def parse_cve(self, vhn_html):
        """
        从VHN漏洞详情页面中提取cve编号
        :param vhn_html: VHN漏洞详情页面
        :return:
        """
        cve = ""
        try:
            cve = re.findall(r'<meta name="keywords" content=".*?(CVE-\d{4}-\d+).*?" />', vhn_html)
            if cve:
                cve = cve[0]
        except:
            pass
        return cve

    def parse_cnnvd(self, vhn_html):
        """
        从VHN漏洞详情页面中提取cve编号
        :param vhn_html: VHN漏洞详情页面
        :return:
        """
        cnnvd = ""
        try:
            cnnvd = re.findall(r'<meta name="keywords" content=".*?(CNNVD-\d+-\d+).*?" />', vhn_html)
            if cnnvd:
                cnnvd = cnnvd[0]
        except:
            pass
        return cnnvd

    def parse_description(self, vhn_html):
        """
        从VHN漏洞详情页面中提取cve编号
        :param vhn_html: VHN漏洞详情页面
        :return:
        """
        description = ""
        try:
            description = re.findall(r'<meta name="description" content="(.*?)" />', vhn_html)
            if description:
                description = description[0]
        except:
            pass
        return description

    def parse_date(self, vhn_html):
        """
        从VHN漏洞详情页面中提取cve编号
        :param vhn_html: VHN漏洞详情页面
        :return:
        """
        date = ""
        try:
            date = re.findall(r'<span>(\d{4}-\d+-\d+)</span>', vhn_html)
            if date:
                date = date[0]
        except:
            pass
        return date

    def get_all_cve(self, start_date, end_date):
        """
        指定时间范围，获得所有cve编号
        :param start_date:
        :param end_date:
        :return:
        """
        if self.cve_list:
            return self.cve_list
        if not self.vhn_list:
            self.get_all_vhn(start_date, end_date)
        for vhn in self.vhn_list:
            query_url = "http://vulhub.org.cn/vuln/{}".format(vhn)
            resp = requests.get(url=query_url, headers=UA().get_ua(), timeout=TIMEOUT)
            html = resp.text
            cve = self.parse_cve(html)
            cnnvd = self.parse_cnnvd(html)
            description = self.parse_description(html)
            date = self.parse_date(html)

            self.cve_list.append(cve)
            self.cnnvd_list.append(cnnvd)
            self.all_code.append({"date":date,"vhn":vhn,"cve":cve,"cnnvd":cnnvd,"description":description,"refer":query_url})
        self.cve_list = list(set(self.cve_list))
        return self.cve_list

    # def get_all_cnnvd(self, start_date, end_date):
    #     """
    #     指定时间范围，获得所有cnnvd编号
    #     :param start_date:
    #     :param end_date:
    #     :return:
    #     """
    #     if self.cnnvd_list:
    #         return self.cnnvd_list
    #     if not self.vhn_list:
    #         self.get_all_vhn(start_date, end_date)
    #     for vhn in self.vhn_list:
    #         query_url = "http://vulhub.org.cn/vuln/{}".format(vhn)
    #         resp = requests.get(url=query_url, headers=UA().get_ua(), timeout=TIMEOUT)
    #         html = resp.text
    #         cve = self.parse_cve(html)
    #         cnnvd = self.parse_cnnvd(html)
    #         self.cve_list.append(cve)
    #         self.cnnvd_list.append(cnnvd)
    #         self.all_code.append({"vhn":vhn,"cve":cve,"cnnvd":cnnvd})
    #     self.cnnvd_list = list(set(self.cnnvd_list))
    #     return self.cnnvd_list

    def get_all_code(self, start_date, end_date):
        if self.all_code:
            return self.all_code
        self.get_all_cve(start_date, end_date)
        return self.all_code


if __name__ == '__main__':
    vulhub =VULHUB()
    start_date = "2021-10-30"
    end_date = "2021-11-05"
    # all_html = vulhub.get_all_vhn(start_date, end_date)
    # vulhub.parse_query_html(all_html)
    # print(vulhub.vhn_list)
    # print(vulhub.get_all_vhn(start_date, end_date))
    # print(vulhub.get_all_cve(start_date, end_date))
    # print(vulhub.get_all_cnnvd(start_date, end_date))
    print(vulhub.get_all_code(start_date, end_date))