import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def save_images_from_url(url):
    # 创建文件夹
    folder_name = url.split("//")[-1].split("/")[0]
    os.makedirs(folder_name, exist_ok=True)

    # 模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 获取所有图片标签
    img_tags = soup.find_all('img')

    # 保存图片
    for img_tag in img_tags:
        img_url = img_tag.get('src')
        if img_url.startswith('http'):
            img_data = requests.get(img_url).content
            img_name = img_url.split('/')[-1]
            img_path = os.path.join(folder_name, img_name)
            with open(img_path, 'wb') as img_file:
                img_file.write(img_data)
                print(f"保存图片: {img_path}")

# 从Excel读取网站URL
df = pd.read_excel('urls.xlsx')  # 替换为Excel文件路径和名称
urls = df['URL'].tolist()

# 使用线程池并发下载图片
with ThreadPoolExecutor() as executor:
    executor.map(save_images_from_url, urls)