# -*- coding: utf-8 -*-
# @Time : 2021/11/2 16:22
# @Author : ordar
# @Project : weekly_information
# @File : query_nvd.py
# @Python: 3.7.5
# https://nvd.nist.gov/vuln/detail/CVE-2021-34754
from config import UA,TIMEOUT
import requests
import re


class NVD:
    def get_html(self, cve):
        """
        获取cve详情页
        :param cve:
        :return:
        """
        query_url = "https://nvd.nist.gov/vuln/detail/{}".format(cve)
        try:
            resp = requests.get(url=query_url, headers=UA().get_ua(), timeout=TIMEOUT)
        except ConnectionError:
            self.get_html(cve)
        except TimeoutError:
            self.get_html(cve)
        except BaseException:
            self.get_html(cve)
        html = resp.text
        return html

    def parse_cwe(self, cve_html):
        """
        从漏洞详情页面中解析出cwe，默认只解析出一个，不知道会不会有bug
        :param cve_html:
        :return:
        """
        cwe = ""
        try:
            cwe = re.findall(r'">(CWE-\d+)</a>', cve_html)
            if cwe:
                cwe = cwe[0]
        except:
            pass
        return cwe

    def query_cwe(self, cve):
        """
        查询CWE编号
        :param cve:
        :return:
        """
        return self.parse_cwe(self.get_html(cve))


if __name__ == '__main__':
    cve = "CVE-2021-34754"
    nvd = NVD()
    print(nvd.query_cwe(cve))
