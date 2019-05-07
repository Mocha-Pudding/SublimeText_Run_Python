# encoding:utf-8

import requests
from lxml import etree
import time
import random
import json
import csv
import os
import logging

START_PAGE = 1       # 开始的页数
END_PAGE =   2       # 结束的页数
ROWS_PERPAGE = 10    # 每页的条数

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        "Referer": "https://www.itu.int/search",
        # "Content-Type":"application/json"   # 构建headers一定要添加"Content-Type":"application/json"
        "Content-Type": "application/json;charset=UTF-8",
        "Host": "www.itu.int",
        "Origin": "https://www.itu.int",
        "Cookie": '_ga=GA1.2.558787849.1555401995; __atuvc=12%7C16; ISAWPLB{48B3F00B-7A0C-46F1-96E5-E0D45B3E0248}={095A8CA5-E521-42A1-B4E4-EC9870128F09}; _gid=GA1.2.656308599.1555893422; WT_FPC=id=156.106.249.68-2212468144.30733361:lv=1555868221850:ss=1555868221850; WSS_FullScreenMode=false; GSCookie=QueryId=1621638&CookieId=9GkwUjF2kk2puYjTNPxxXLqLwLxQ5ptbXk2CZj5ntEb9W+ra6/6RRWETzPfLFPrHk8vURiRFwz+ulkU8xcJ+FA=='
    }

# ip pool
PROXIES = [
    "211.152.33.24", "139.199.117.41", "163.204.242.164", "180.118.247.225", "125.123.138.248", "47.94.136.5",
    "221.7.211.246", "114.119.116.92", "119.145.2.98", "118.190.73.168", "110.52.235.133", "116.209.55.16",
    "111.177.191.164", "163.204.243.226", "183.129.207.91", "121.204.150.131", "116.226.30.99", "183.147.208.201",
    "163.204.245.55", "163.204.243.171", "111.177.168.98", "211.147.239.101", "175.42.168.212", "163.125.31.155",
    "163.204.242.14", "125.123.141.92", "61.164.39.68", "114.234.82.144", "119.101.113.57", "119.57.108.109"
]

logging.basicConfig(
    level=logging.INFO,
    # format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    format='%(asctime)s - %(filename)s[line:%(lineno)3d] - %(levelname)s: %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='ITU_run.log',
    filemode='a',   # w为写模式，会覆盖；a为追加模式
)
console = logging.StreamHandler()   # 往屏幕上输出
formatter = logging.Formatter('%(name)-6s: %(levelname)-6s %(message)s')   # 设置日志格式
console.setLevel(logging.INFO)   # 设置级别
console.setFormatter(formatter)   # 设置屏幕上显示格式
logging.getLogger('').addHandler(console)

def request_list_page():
    url = "https://www.itu.int/net4/ITU-T/search/GlobalSearch/Search"

    for x in range(START_PAGE, END_PAGE+1):
        start = x
        START = str(start * 10 - 10)  # payload参数里的Start
        ROWS = str(ROWS_PERPAGE)  # payload参数里的Rows
        print("---爬取的页数：第%s页到第%s页---Start值：%s---Rows值：%s---\n~~~~~~~~~~~~~~~当前页数：%d~~~~~~~~~~~~~~~~" % (START_PAGE, END_PAGE, START, ROWS, start))
        logging.info("爬取的页数：第%s页到第%s页,Start值：%s,Rows值：%s,当前页数：%d" % (START_PAGE, END_PAGE, START, ROWS, start))
        proxy = random.choice(PROXIES)
        print("------ 被选中的代理ip：%s ------" % proxy)
        logging.info("------ 被选中的代理ip：%s ------" , proxy)

        # 构造Request Payload参数
        str1 = "{\"json\":\"{\\\"Input\\\":\\\"\\\",\\\"Start\\\":"
        str2 = ",\\\"Rows\\\":"
        str3 = ",\\\"SortBy\\\":\\\"NEWEST FIRST\\\",\\\"ExactPhrase\\\":false,\\\"CollectionName\\\":\\\"General\\\",\\\"CollectionGroup\\\":\\\"Recommendations\\\",\\\"Sector\\\":\\\"all\\\",\\\"Criterias\\\":[{\\\"Name\\\":\\\"Search in\\\",\\\"Criterias\\\":[{\\\"Selected\\\":false,\\\"Value\\\":\\\"\\\",\\\"Label\\\":\\\"Name\\\",\\\"Target\\\":\\\"\\\\\\\\/name_s\\\",\\\"TypeName\\\":\\\"CHECKBOX\\\",\\\"GetCriteriaType\\\":0,\\\"$$hashKey\\\":\\\"object:1438\\\"},{\\\"Selected\\\":false,\\\"Value\\\":\\\"\\\",\\\"Label\\\":\\\"Short description\\\",\\\"Target\\\":\\\"\\\\\\\\/short_description_s\\\",\\\"TypeName\\\":\\\"CHECKBOX\\\",\\\"GetCriteriaType\\\":0,\\\"$$hashKey\\\":\\\"object:1439\\\"},{\\\"Selected\\\":false,\\\"Value\\\":\\\"\\\",\\\"Label\\\":\\\"File content\\\",\\\"Target\\\":\\\"\\\\\\\\/file\\\",\\\"TypeName\\\":\\\"CHECKBOX\\\",\\\"GetCriteriaType\\\":0,\\\"$$hashKey\\\":\\\"object:1440\\\"}],\\\"ShowCheckbox\\\":true,\\\"Selected\\\":false,\\\"$$hashKey\\\":\\\"object:1422\\\"}],\\\"Topics\\\":\\\"\\\",\\\"ClientData\\\":{\\\"ip\\\":\\\""
        str4 = "\\\"},\\\"Language\\\":\\\"en\\\",\\\"IP\\\":\\\""
        str5 = "\\\",\\\"SearchType\\\":\\\"All\\\"}\"}"
        payloadData = str1 + START + str2 + ROWS + str3 + proxy + str4 + proxy + str5
        loadsJsonData = json.loads(payloadData)
        response = requests.post(url=url, headers=headers, data=payloadData)
        # json方法：如果返回的是json数据，那么该方法自动load成字典
        results = response.json()

        results_list = results.get("results")
        print(results_list)
        print("=-" * 60)

        json_str = loadsJsonData["json"]
        jsonStr = json.loads(json_str)
        print(jsonStr, type(jsonStr))  # <class 'dict'>
        start_page = (jsonStr["Start"] + 10) // 10  # 地板除 返回int
        print("=========>>> Start Page:", start_page)  # <class 'int'>
        logging.info("---START---当前爬取的页数为：第%d页---START---", start_page)      ##########log
        print("=-" * 60)

        detail_list = []

        for result in results_list:
            identifier = result.get('Identifier')  # Identifier
            title = result.get('Title')  # Title
            redirection = result.get('Redirection')  # Redirection
            print(identifier, "|", title, "|", redirection)
            print("-=+=-" * 20)

            language = result.get('Language')
            if language == 'en':
                # parse_page1_detail(redirection)
                detail_dict = parse_page1_detail(redirection)
                detail_list.append(detail_dict)
                cell_num = results_list.index(result) + 1
                print("==========↑↑↑ 输出第%d页第%d条数据 ↑↑↑==========" %(start, cell_num))
            else:
                # 专利声明 Patent Statement不需要该页面
                # parse_page2_detail(redirection)
                print("------>>> Patent Statement 专利声明 <<<------")
                cell_num = results_list.index(result) + 1
                print("==========↑↑↑ 输出第%d页第%d条数据 ↑↑↑==========" %(start, cell_num))

            time.sleep(random.uniform(1, 3))
        print("+++++++++++detail_list++++++++++++++++++++",detail_list)
        logging.info("---THE END---本页爬取完成，即将进入第%d页---THE END---", start_page+1)
        csv_export(detail_list)   # 写入CSV文件中

# 页面解析
def parse_page1_detail(url):
    # 解析页面样式1：language="en"
    detail_dict = {}
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)

    contentTable = html.xpath("//div[@class='content']//div[@id='ctl00_content_main_UpdatePanel2']//table[@id='ctl00_content_main_table_details']")[0]
    # 详情栏目里的项目个数(通过标签<td class='cell_left'>反向取到上一层父节点)
    detailCells = contentTable.xpath("//div[@id='ctl00_content_main_uc_rec_main_info1_div_rec_main_info']//tr//td[@class='cell_left']/..")
    # 遍历详情栏目里的每一项
    for index, detailCell in enumerate(detailCells):
        cell_name = detailCell.xpath("./td[1]/text()")[0].strip()
        # print(index, cell_name)
        if cell_name.startswith("Approval process:"):
            # 审批流程 approval_process
            approval_process = detailCell.xpath("./td[2]//text()")[0].strip()
            detail_dict["审批流程"] = approval_process
            # print("======------>>>>>> ", approval_process)
        if cell_name.startswith("Provisional name:"):
            provisional_name = detailCell.xpath("./td[2]//text()")[0].strip()
            detail_dict["临时名称"] = provisional_name
        if cell_name.startswith("Observation:"):
            # 观察 observation
            observation = detailCell.xpath("./td[2]//text()")[0].strip()
            detail_dict["观察"] = observation
        if cell_name.startswith("Identical standard:"):
            # 国际协调标准 identical_standard
            identical_standard = detailCell.xpath("./td[2]//text()")[0].strip()
            detail_dict["国际协调标准"] = identical_standard

    # 1.标准号 std_num
    std_num = contentTable.xpath("//div[@id='ctl00_content_main_uc_rec_main_info1_div_rec_main_info']//span[@id='ctl00_content_main_uc_rec_main_info1_rpt_main_ctl00_lbl_rec']/text()")[0].strip()
    detail_dict["标准号"] = std_num
    # 2.标题 title
    try:
        title = contentTable.xpath("//div[@id='ctl00_content_main_uc_rec_main_info1_div_rec_main_info']//td[@class='title']")[0]
        title = title.xpath("./text()")[0].strip()
        detail_dict["名称"] = title
        # print("~~~~~~~~~~~title is not NULL")
    except:
        title = " "
        # print("~~~~~~~~~~~title is NULL")
    # 3.pdf文件下载链接 pdf_link
    try:
        pdf_link = contentTable.xpath("//div[@id='ctl00_content_main_uc_rec_main_info1_div_rec_main_info']/table/tr[1]/td/table[2]/tr[1]//td//a/@href")[0].strip()   # try try try
        detail_dict["文件链接"] = pdf_link
        print("-----pdf link-------",pdf_link)
        print("~~~~~~~~~~~pdf link is not NULL")
    except:
        pdf_link = " "
        print("~~~~~~~~~~~pdf link is NULL")

    # 4.引用 citation
    citation = contentTable.xpath("//div[@id='ctl00_content_main_uc_rec_main_info1_div_rec_main_info']//span[@id='ctl00_content_main_uc_rec_main_info1_rpt_main_ctl00_Label6']/text()")[0].strip()
    detail_dict["引用"] = citation
    # 5.状态 status
    status = contentTable.xpath(
        "//div[@id='ctl00_content_main_uc_rec_main_info1_div_rec_main_info']//span[@id='ctl00_content_main_uc_rec_main_info1_rpt_main_ctl00_Label7']/text()")[0].strip()
    detail_dict["状态"] = status
    detail_dict["语言"] = "English"
    # 6.临时名称 provisional_name
    # provisional_name = contentTable.xpath("//div[@id='ctl00_content_main_uc_rec_main_info1_div_rec_main_info']//td[@class='cell_right']/text()")[0].strip()
    # detail_dict["临时名称"] = provisional_name
    # 7.审批日期 approval_date
    approval_date = contentTable.xpath("//div[@id='ctl00_content_main_uc_rec_main_info1_div_rec_main_info']//span[@id='ctl00_content_main_uc_rec_main_info1_rpt_main_ctl00_Label5']/text()")[0].strip()
    detail_dict["审批日期"] = approval_date

    # 8.版本 Editions (单独版块)
    edition_container = contentTable.xpath("//div[@id='ctl00_content_main_TabContainer1']//div[@id='ctl00_content_main_TabContainer1_body']//div[@id='ctl00_content_main_TabContainer1_tab_edition']")[0]
    editions = edition_container.xpath("//div[@id='ctl00_content_main_TabContainer1_tab_edition_uc_rec_details1_div_rec_details']/div[1]/table//tr")[1:]   # 去除掉第一个tr标签，为标签的header
    print(">>>>>>>>>>>>Editions Container<<<<<<<<<<<<", editions, len(editions), type(editions))
    # 遍历Editions板块中的所有edition
    edition_list = []
    for edition in editions:
        # print("->->->editon->->->",edition)
        edition_title = edition.xpath("./td[2]//a/text()")[0].strip()
        edition_status = edition.xpath("./td[3]/span/text()")[0].strip()
        edition_item = edition_title + ":" + edition_status
        print("|->|->|->|->", edition_item)
        edition_list.append(edition_item)
    detail_dict["版本"] = "||".join(edition_list)   # 使用join方法将所有的edition用||分隔
    # print(edition_list, len(edition_list))
    print(detail_dict["版本"])

    print(detail_dict, type(detail_dict))
    print(
        "标准号：", std_num,
        "\n名称：", title,
        "\n引用：", citation,
        "\n状态：", status,
        "\n语言：", "English",
        # "\n临时名称：", detail_dict["临时名称"],
        # "\n审批流程：", detail_dict["审批流程"],
        "\n审批日期：", approval_date,
        # "\n国际协调标准: ", detail_dict["国际协调标准"],
        # "\n观察: ", detail_dict["观察"],
        # "\n文件链接：", detail_dict["文件链接"]
    )
    print("----------page analysis----------"*3)
    print(detailCells, len(detailCells))   # 详情条数
    print("----------!!!page analysis test!!!----------"*2)

    return detail_dict

# Patent Statement不需要解析
def parse_page2_detail(url):
    # 解析页面样式2：language="xx"
    # response = requests.get(url, headers=headers)
    # html = etree.HTML(response.text)
    pass

# 写入CSV文件
def csv_export(data):
    # 判断csv文件是否存在，不存在则创建文件，并写入表头添加数据；存在则增量写入
    csv_headers = ['标准号', '名称', '引用', '状态', '语言', '临时名称', '审批流程', '审批日期', "国际协调标准", "观察", "文件链接", "版本"]  # 定义csv表头
    values = data

    if not(os.path.exists('ITU_result.csv')):
        print("------log------文件不存在，创建csv文件并写入表头")
        with open('ITU_result.csv', 'w', encoding='UTF-8', newline='') as fp:
            writer = csv.DictWriter(fp, csv_headers)
            writer.writeheader()  # 写入表头数据的时候，需要调用writerheader方法
            writer.writerows(values)
    else:
        with open('ITU_result.csv', 'a', encoding='UTF-8', newline='') as fp:
            print("------log------文件存在，增量写入csv文件")
            writer = csv.DictWriter(fp, csv_headers)
            writer.writerows(values)

def main():
    request_list_page()

if __name__ == '__main__':
    main()