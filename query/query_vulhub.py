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
import json
from config import UA,TIMEOUT


class VULHUB:
    def __init__(self):
        self.vhn_list = []
        self.all_code = []
        self.cve_list = []
        self.cnnvd_list = []
        self.cnvd_list = []
        self.all_data = []
        self.cwe_list = self.load_cwe()

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
        parse_date = re.findall(r"<td class='hidden-xs hidden-sm'>(\d+-\d+-\d+)</td>", html)
        parse_level = re.findall(r"""data-placement="bottom" title='(\w+)'""", html)
        self.vhn_list.extend(parse_vhn)
        for i in range(len(parse_vhn)):
            temp = {}
            temp["vhn"] = parse_vhn[i]
            temp['date'] = parse_date[i]
            temp['level'] = parse_level[i]
            self.all_data.append(temp)
        return self.all_data

    def get_all_vhn(self, start_date, end_date):
        """
        指定时间范围，获得所有vhn编号
        :param start_date:
        :param end_date:
        :return:
        """
        pages = self.query_pages(start_date, end_date)
        for page in range(1, 1 + int(pages)):
            self.parse_query_html(self.query_html_by_date(start_date, end_date, page))
        # self.vhn_list = list(set(self.vhn_list))
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
        从VHN漏洞详情页面中提取CNNVD编号
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

    def parse_cnvd(self, vhn_html):
        """
        从VHN漏洞详情页面中提取CNVD编号
        :param vhn_html: VHN漏洞详情页面
        :return:
        """
        cnnvd = ""
        try:
            cnnvd = re.findall(r'<meta name="keywords" content=".*?(CNVD-\d+-\d+).*?" />', vhn_html)
            if cnnvd:
                cnnvd = cnnvd[0]
        except:
            pass
        return cnnvd

    def parse_description(self, vhn_html):
        """
        从VHN漏洞详情页面中提取描述
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
        从VHN漏洞详情页面中提取日期
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

    def get_all_data(self, start_date, end_date):
        """
        指定时间范围，获得所有VULHUB 上数据
        :param start_date:
        :param end_date:
        :return:
        """
        # if self.cve_list:
        #     return self.cve_list
        if not self.vhn_list:
            self.get_all_vhn(start_date, end_date)
        for item in self.all_data:
            query_url = "http://vulhub.org.cn/vuln/{}".format(item["vhn"])
            resp = requests.get(url=query_url, headers=UA().get_ua(), timeout=TIMEOUT)
            html = resp.text
            cve = self.parse_cve(html)
            cnnvd = self.parse_cnnvd(html)
            cnvd = self.parse_cnvd(html)
            description = self.parse_description(html)
            date = self.parse_date(html)

            self.cve_list.append(cve)
            self.cnnvd_list.append(cnnvd)
            self.cnvd_list.append(cnvd)
            item.update({"cve":cve,"cnvd":cnvd,"cnnvd":cnnvd,"description":description,"refer":query_url})
        # self.cve_list = list(set(self.cve_list))
        return self.all_data

    def get_all_code(self, start_date, end_date):
        if self.all_data:
            return self.all_data
        self.get_all_data(start_date, end_date)
        return self.all_data

    def load_cwe(self):
        """
        从json文件加载cwe
        :return:
        """
        with open("enum_cwe.json", 'r', encoding='utf8') as f:
            cwe_json = json.load(f)
        cwe_list = cwe_json["RECORDS"]
        return cwe_list

    def get_cwe_description(self, cwe_id):
        """
        获取cwe描述
        :param cwe_id:
        :return:
        """
        cwe_id = str(cwe_id).upper()
        for i in self.cwe_list:
            if i["_id"] == cwe_id:
                return i["title_zh"]


if __name__ == '__main__':
    vulhub =VULHUB()
    start_date = "2022-02-16"
    end_date = "2022-02-17"
    # all_html = vulhub.get_all_vhn(start_date, end_date)
    # vulhub.parse_query_html(all_html)
    # print(vulhub.vhn_list)
    # print(vulhub.get_all_vhn(start_date, end_date))
    # print(vulhub.get_all_cve(start_date, end_date))
    # print(vulhub.get_all_cnnvd(start_date, end_date))

    print(vulhub.get_all_code(start_date, end_date))
    print(vulhub.get_cwe_description("cwe-200"))