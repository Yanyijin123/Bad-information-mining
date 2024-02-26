import os
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from urllib.parse import urlparse
from tqdm import tqdm


def validate_folder_path(folder_path):
    # 检查文件夹路径是否存在
    if not os.path.exists(folder_path):
        print("文件夹路径不存在:", folder_path)
        return False

    # 检查文件夹路径是否为目录
    if not os.path.isdir(folder_path):
        print("文件夹路径不是一个目录:", folder_path)
        return False

    # 检查文件夹路径是否具有写权限
    if not os.access(folder_path, os.W_OK):
        print("文件夹路径没有写权限:", folder_path)
        return False

    return True


def save_images_from_website(url, folder_path):
    # 发送网络请求获取网页内容
    response = requests.get(url)
    if response.status_code != 200:
        print("无法访问网页:", url)
        return

    # 创建文件夹
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # 查找所有的<img>元素，并保存图片
    img_tags = soup.find_all('img')
    total_images = len(img_tags)
    with tqdm(total=total_images, ncols=60, desc="进度") as pbar:
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if img_url:
                # 保存图片到本地文件夹
                img_filename = img_url.split('/')[-1]
                img_filepath = os.path.join(folder_path, img_filename)
                urlretrieve(img_url, img_filepath)
                pbar.update(1)
                pbar.set_postfix({"保存图片": img_filepath})


# 测试代码
website_url = input("请输入网站URL: ")
folder_path = input("请输入文件夹路径: ")


# 验证文件夹路径的有效性
if validate_folder_path(folder_path):
    # 文件夹路径有效，调用保存图片的函数
    save_images_from_website(website_url, folder_path)
else:
    # 文件夹路径无效，进行适当的处理
    print("文件夹路径无效，请提供有效的文件夹路径。")