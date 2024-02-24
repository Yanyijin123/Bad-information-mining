# —*—coding：utf-8-*—
#这个代码是用来实现决策树中判断属性输入的转化，包含video，book两种分别对应小说网站和视频网站
from bs4 import BeautifulSoup
from collections import defaultdict
from content_capture import content_Capture
import requests
import re
#-------------------------------------------------------------------------------
#(1） URL的后缀类型，后缀类型为.html则特征值为0，为.js则特征值为1，其它类型的后缀则特征值为2;
def get_suffix_feature(url):
    # 获取URL的后缀
    suffix = url.split('.')[-1]
    # 根据后缀类型返回特征值
    if suffix == 'html':
        return 0
    elif suffix == 'js':
        return 1
    else:
        return 2

#------------------------------------------------------------------------------------
#这里需要注意的是target_tag = soup.find('a', href=target_url)需要输入的target_url是匹配相对路径，因为实现的时候为了减少一个检索过程在获取url的时候获取的是一个包含绝对
#路径和相对路径的元组('/books/85357/', 'https://www.asvmw.cc/books/85357/')当需要访问时使用元组的第1个元素，匹配的时候使用第0个元素
#(2)URL所处层级，通过对HTML文本结构的分析并依据DOM树的层级特点，本文对HTML文本中的每个URL设置了层级属性，以<html>标签所处的层级为第0级
# 每个标签的所处层级为其外部嵌套的标签的层级加1，特征值为URL所处的层级树
def get_url_hierarchy(html_content, target_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    url_hierarchy = None
    # 找到目标URL所在的标签
    target_tag = soup.find('a', href=target_url)
    if target_tag:
        # 计算目标URL所处的层级
        url_hierarchy = calculate_hierarchy(target_tag)
    return url_hierarchy

def calculate_hierarchy(tag):
    hierarchy = 0
    current_tag = tag
    # 逐级向上查找标签，直到<html>标签
    while current_tag and current_tag.name != 'html':
        hierarchy += 1
        current_tag = current_tag.parent
    return hierarchy


#------------------------------------------------------------------------------------
#(3)URL所处层级的其它URL数量
def get_all_urls_with_hierarchy(html_content):
    urls_by_hierarchy = defaultdict(list)
    soup = BeautifulSoup(html_content, 'html.parser')
    all_a_tags = soup.find_all('a')

    for tag in all_a_tags:
        if 'href' in tag.attrs:  # 检查标签是否包含 'href' 属性
            hierarchy = calculate_hierarchy(tag)
            urls_by_hierarchy[hierarchy].append(tag['href'])

    return urls_by_hierarchy

def count_other_urls_at_hierarchy(html_content, target_url):
    urls_by_hierarchy = get_all_urls_with_hierarchy(html_content)
    target_hierarchy = get_url_hierarchy(html_content, target_url)

    if target_hierarchy is not None:
        other_urls_count = sum(
            len(urls) for hierarchy, urls in urls_by_hierarchy.items() if hierarchy == target_hierarchy) - 1
        # 减去目标URL本身的数量
        return other_urls_count
    else:
        return 0

#------------------------------------------------------------------------------------
#(4）URL后是否有title属性，有则特征值为1，否则为0;
#(5）URL后是否有target属性，有则特征值为1，否则为0;
def extract_features(html_content, target_url):
    title_attribute = 0
    target_attribute = 0

    soup = BeautifulSoup(html_content, 'html.parser')

    target_element = soup.find(attrs={'href': target_url})
    if target_element is not None:
        if target_element.has_attr('title'):
            title_attribute = 1
        if target_element.has_attr('target'):
            target_attribute = 1

    return title_attribute, target_attribute

#-----------------------------------------------------------------------------------
# (6)URL中是否包含'play''book''chapter''read'字符串，包含则特征值为1，否则为0;
def url_contains_keyword(url):
    keywords = ["play", "book", "chapter"]
    for keyword in keywords:
        if keyword in url:
            return 1
    return 0

#-----------------------------------------------------------------------------------
#(7)URL是否可访问，若可访问即对URL发出请求后返回的HTTP状态码为-200，则特征值为1，否则为0
def url_accessible(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return 1
        else:
            return 0
    except requests.RequestException:
        return 0

#-----------------------------------------------------------------------------------
#( 8）URL中是否含有"数字-数字"模式的子串，包含则特征值为1，否则为0
def url_contains_pattern(url):
    pattern = r'\d+/\d+'
    match = re.search(pattern, url)
    if match:
        return 1
    else:
        return 0

#在这里我又设置了一个函数将离散的url数目转化3层简化我们的思路，如果是0-3层，那么这个url属于底层url，3-6中层，超过6说明这个url是非常深层次的url
def convert_hierarchy_level(level):
    if level <= 3:
        return 0
    elif level <= 6:
        return 1
    else:
        return 2

#在这里我又设置了一个函数将离散的url数目转化3层简化我们的思路，如果是0-10层，那么这个url属于少量类似url，10-50中量类似url，超过50说明这个大量相似url
def convert_count_level(level):
    if level <= 10:
        return 0
    elif level <= 50:
        return 1
    else:
        return 2

#总调用函数获取所有特征target_url是元组('/books/85357/', 'https://www.asvmw.cc/books/85357/')
def get_features(url, target_url):
    html_content = content_Capture(url)
    if html_content:
        suffix = get_suffix_feature(target_url[1])
        hierarchy = get_url_hierarchy(html_content, target_url[0])
        urls_count = count_other_urls_at_hierarchy(html_content, target_url[0])
        title_attribute, target_attribute = extract_features(html_content, target_url[0])
        keywords = url_contains_keyword(target_url[1])
        response = url_accessible(target_url[1])
        match = url_contains_pattern(target_url[1])

        # 确保所有变量都不为 None 才计算 url_hierarchy 和 other_urls_count
        if all(x is not None for x in
               [suffix, hierarchy, urls_count, title_attribute, target_attribute, keywords, response, match]):
            url_hierarchy = convert_hierarchy_level(hierarchy)
            other_urls_count = convert_count_level(urls_count)
            return suffix, url_hierarchy, other_urls_count, title_attribute, target_attribute, keywords, response, match
    return None

#test
#suffix,url_hierarchy,other_urls_count,title_attribute, target_attribute,keywords,response,match=get_features("https://www.asvmw.cc/books/18231/", ('/indexlist/18231/', 'https://www.asvmw.cc/indexlist/18231/'))
#print(suffix,url_hierarchy,other_urls_count,title_attribute, target_attribute,keywords,response,match)