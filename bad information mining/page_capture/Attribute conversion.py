# —*—coding：utf-8-*—
#这个代码是用来实现决策树中判断属性输入的转化，包含video，book两种分别对应小说网站和视频网站
from bs4 import BeautifulSoup
from content_capture import content_Capture
from collections import defaultdict
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

def hierarchy(url, target_url):
    html_content = content_Capture(url)
    if html_content:
        # 尝试直接查找目标URL
        url_hierarchy = get_url_hierarchy(html_content, target_url)
        if url_hierarchy is not None:
            return  url_hierarchy
        else:
            # 如果直接查找失败，则尝试去除基础URL部分再查找
            base_url = url.rstrip('/') + '/'  # 确保基础URL以斜杠结尾
            cleaned_target_url = target_url.replace(base_url, '')  # 去除基础URL部分
            url_hierarchy = get_url_hierarchy(html_content, cleaned_target_url)

            if url_hierarchy is not None:
                return url_hierarchy
            else:
                return None
    else:
        return None

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

def count_other_urls_at_hierarchy(html_content, url, target_url):
    urls_by_hierarchy = get_all_urls_with_hierarchy(html_content)
    target_hierarchy = hierarchy(url, target_url)

    if target_hierarchy is not None:
        other_urls_count = sum(
            len(urls) for hierarchy, urls in urls_by_hierarchy.items() if hierarchy == target_hierarchy) - 1
        # 减去目标URL本身的数量
        return other_urls_count
    else:
        return None

def other_urls_at_hierarchy(url,target_url):
    html_content = content_Capture(url)

    if html_content:
        other_urls_count = count_other_urls_at_hierarchy(html_content, url, target_url)
        if other_urls_count is not None:
            return other_urls_count
        else:
            return None
    else:
        return None

a=other_urls_at_hierarchy("http://www.aishuge.cc/kan/62/62164/","http://www.aishuge.cc/kan/62/62164/132107.html")
b=hierarchy("https://www.bbaook.cn/","https://www.bbaook.cn/txt/15784260tzj3/")
print(a,b)
#if __name__ == "__main__":
    #url = "http://www.aishuge.cc/kan/62/62164/"
    #target_url = "http://www.aishuge.cc/kan/62/62164/132107.html"
