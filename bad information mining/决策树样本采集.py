# —*—coding：utf-8-*—
import time
import urllib
import pandas as pd
import requests
from url_judgement.DT_Attribute_conversion import features
from page_capture.content_capture import url_Capture  # 导入从一个页面获取链接的函数


def can_access(url):
    try:
        response = requests.head(url)
        return response.status_code == 200  # 如果状态码为200，返回True，表示可访问
    except requests.RequestException:
        return False  # 发生任何异常，返回False，表示不可访问

def catch(website_Links):
    if not website_Links.empty:
        Website_Links = website_Links['url'].tolist()  # 转换为列表
        print("Processing link:", Website_Links)
        sum_L_links = []
        sum_P_links = []
        for url in Website_Links:
            # 使用 Website_Links 变量处理链接
            tag_L_links = []

            try:
                L_link,L_html_content = url_Capture(url)

            except urllib.error.HTTPError as e:
                if e.code == 403:
                    print(f"HTTP Error 403: Forbidden for {url}. Skipping...")
                    continue  # 跳过当前链接的处理
                else:
                    raise e  # 如果不是HTTP Error 403，抛出异常

            for L_url in L_link:
                tag_P_links = []  # 初始化 tag_P_links 列表
                if len(tag_L_links) < 10:
                    # 判断是否能够访问L_url
                    if can_access(L_url[1]):
                        suffix1, url_hierarchy1, other_urls_count1, title_attribute1, target_attribute1, keywords1, response1, match1=features(L_html_content,L_url)
                        L=[L_url[1],L_url,suffix1, url_hierarchy1, other_urls_count1, title_attribute1, target_attribute1, keywords1, response1, match1]
                        print("L",L)
                        sum_L_links.append(L)
                        tag_L_links.append(L_url)
                        # 捕获P-links
                        try:
                            P_link,P_html_content = url_Capture(L_url[1])


                        except urllib.error.HTTPError as e:
                            if e.code == 403:
                                print(f"HTTP Error 403: Forbidden for {L_url[1]}. Skipping...")
                                continue  # 跳过当前链接的处理
                            else:
                                raise e  # 如果不是HTTP Error 403，抛出异常

                        for p_url in P_link:
                            # 判断是否能够访问P_link
                            if len(tag_P_links) < 3:
                                if can_access(p_url[1]):
                                    suffix2, url_hierarchy2, other_urls_count2, title_attribute2, target_attribute2, keywords2, response2, match2 = features(P_html_content, p_url)
                                    P = [p_url[1],p_url, suffix2, url_hierarchy2, other_urls_count2, title_attribute2, target_attribute2, keywords2, response2, match2]
                                    print("p",P)
                                    sum_P_links.append(P)
                                    tag_P_links.append(p_url)
                            else:
                                break

                    else:
                        break
                else:
                    break

            # 将 sum_L_links 和 sum_P_links 合并成一个列表
            sum_links = sum_L_links + sum_P_links
            # 将列表转换为 DataFrame
            df = pd.DataFrame(sum_links,
                              columns=['clik','url', 'suffix', 'url_hierarchy', 'other_urls_count', 'title_attribute',
                                       'target_attribute', 'keywords', 'response', 'match'])
            # 将 DataFrame 写入 Excel 文件
            df.to_excel('output.xlsx', index=False)

            # 添加延迟，每处理完一个链接后延迟2秒
            time.sleep(2)
    else:
        print("Empty row, skipping...")

def extract_links_from_excel(file_path):
        # 读取 Excel 文件
    df = pd.read_excel(file_path)

        # 将整个 DataFrame 传递给 catch() 函数
    catch(df)

if __name__ == '__main__':
    # 读取Excel文件
    excel_file_path = 'testurl.xlsx'
    # 提取链接并处理
    extract_links_from_excel(excel_file_path)