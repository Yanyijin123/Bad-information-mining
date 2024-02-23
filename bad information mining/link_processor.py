import os
import re
import time
import urllib
import pandas as pd
from page_capture.content_capture import url_Capture  # 导入从一个页面获取链接的函数
from url_jugement.judgement_links import Judgement_Links  # 导入一个从页面判断链接的函数,决策树

def process_links(website_Links):
    if not website_Links.empty:
        Website_Links = website_Links['url'].tolist()  # 转换为列表
        print("Processing link:", Website_Links)

        # 使用 Website_Links 变量处理链接
        tag_L_links = []

        while Website_Links:
            url = Website_Links.pop(0)
            try:
                S_link = url_Capture(url)
            except urllib.error.HTTPError as e:
                if e.code == 403:
                    print(f"HTTP Error 403: Forbidden for {url}. Skipping...")
                    continue  # 跳过当前链接的处理
                else:
                    raise e  # 如果不是HTTP Error 403，抛出异常

            # test
            print("在首页获取的链接")
            print(S_link)

            for L_url in S_link:
                L_jud = Judgement_Links(L_url)  # 直接传递URL字符串
                sum_P_links = []  # 初始化 sum_P_links 列表
                tag_P_links = []  # 初始化 tag_P_links 列表

                if L_jud == 1:
                    T_link = url_Capture(L_url)
                    tag_L_links.append(L_url)

                    # test
                    print("在章节页获取的链接")
                    print(T_link)

                    for P_url in T_link:
                        P_jud = Judgement_Links(P_url)  # 直接传递URL字符串

                        if P_jud == 2:
                            tag_P_links.append(P_url)
                            sum_P_links.append(P_url)
                            # 处理已经获取的页面内容

                        else:
                            # 如果P_jud为假，则重新获取一条S_link中的P_url进行判断
                            break

                    # 如果tag_P_links中的元素个数超过五个，或者T_link不再有元素，则重新获取一条S_link中的链接进行判断
                    if len(tag_P_links) >= 5 or not T_link:
                        break

                    # test
                    print("--------标记p-链接------")
                    print(tag_P_links)

                else:
                    # 如果L_jud为假，则重新获取一条S_link中的链接进行判断
                    break
                # test
                print("标记L-链接")
                print(tag_L_links)

            # 如果tag_L_links中的元素个数超过5个，或者S_link不再有元素，则重新获取Website_Links中一条url进行判断
            if len(tag_L_links) >= 5 or not Website_Links:
                break

            # 合并 tag-P-links 到 sum_P_links 列表中
            sum_P_links.extend(tag_P_links)

            # 对 URL 进行处理，生成合法的文件名
            file_name = re.sub(r'[/:*?"<>|]', '_', url)  # 将不合法的字符替换为下划线
            file_name = file_name.rstrip(".")  # 去除末尾可能的点号

            # 保存标记的 P-url 和 L-url 到以每个 S-link 为命名的 Excel 文件下
            data = {'tag-L-url': tag_L_links, 'sum-P-url': sum_P_links}
            # 确保两个列的长度相同，用 None 填充
            max_length = max(len(tag_L_links), len(sum_P_links))
            data['tag-L-url'] += [None] * (max_length - len(tag_L_links))
            data['sum-P-url'] += [None] * (max_length - len(sum_P_links))
            df = pd.DataFrame(data)

            # 创建保存文件夹
            folder_path = "需要检测的页面"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # 保存Excel文件到文件夹中
            file_path = os.path.join(folder_path, f"{file_name}.xlsx")
            df.to_excel(file_path, index=False, engine='openpyxl')

            # 添加延迟，每处理完一个链接后延迟1秒
            time.sleep(2)

    else:
        print("Empty row, skipping...")
