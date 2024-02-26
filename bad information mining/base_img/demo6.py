import requests
from bs4 import BeautifulSoup
import os
import re

# 定义要爬取的网页URL
url = "http://www.youku.com"

# 发送请求，获取网页源代码
response = requests.get(url)
html = response.content.decode('utf-8')

# 使用BeautifulSoup解析网页
soup = BeautifulSoup(html, 'html.parser')

# 创建目标文件夹
if not os.path.exists('images'):
    os.mkdir('images')

# 遍历所有图片标签，获取图片并保存到本地
for img in soup.findAll('img'):
    img_url = img.get('src')

    #判断图片地址是否包含协议头
    if not re.match(r'http[s]?:', img_url):
        img_url = 'https:' + img_url

    r = requests.get(img_url)

    #清理文件名
    image_name = re.sub(r'[^\w\-_\. ]', '', os.path.basename(img_url))

    with open('images/' + image_name, 'wb') as f:
        f.write(r.content)

print('图片爬取完成！')

