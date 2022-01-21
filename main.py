import datetime
import json
import time
import sys
from datetime import timedelta
from query.query_vulhub import VULHUB
from query.query_nvd import NVD
from query.query_cnnvd import CNNVD

# 所有信息
all_info = []

now = datetime.datetime.now()
# 上周六的日期
this_week_start = (now - timedelta(days=2+now.weekday())).date()
# 到本周五的日期
this_week_end = (now + timedelta(days=4-now.weekday())).date()

# 打印日期,可以按需求注释掉
print("日期：", str(this_week_start), str(this_week_end))
# this_week_start = "2021-10-16"
# this_week_end = "2021-10-22"


vulhub = VULHUB()
nvd = NVD()
# cnnvd = CNNVD()

print("爬取VULHUB...")
vulhub_info = vulhub.get_all_code(this_week_start, this_week_end)
# 打印总数,可以按需求注释掉
print("本周总数：", str(len(vulhub_info)))
# print(vulhub_info)
# print('\n')

txt_file_name = "weekly_infomation{}to{}.txt".format(this_week_start,this_week_end)
with open(txt_file_name, 'w', encoding='utf8') as f:
    f.write('')
print("逐条打印并输出到文件（{}）：".format(txt_file_name))
for vul in vulhub_info:
    vul['cwe'] = nvd.query_cwe(vul['cve'])

    all_info.append(vul)
    # 过滤无效数据
    if not vul["cnnvd"] and vul["cnvd"]:
        pass

    # 打印每一行,可以按需求注释掉
    vul_str = json.dumps(vul, indent=4, ensure_ascii=False)
    print(vul_str)
    with open(txt_file_name, 'a', encoding='utf8') as f:
        f.write(vul_str)
    time.sleep(1)


# # 非格式化打印,可以按需求注释掉
# print('\n')
# print(all_info)

# 格式化打印,可以按需求注释掉
# all_info_str = json.dumps(all_info, indent=4, ensure_ascii=False)
# print('\n')
# print("全部格式化打印：")
# print(all_info_str)
