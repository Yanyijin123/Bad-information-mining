import os
import time
import requests
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def clean_filename(filename):
    # 清理特殊字符
    invalid_chars = ['?', '\\']
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename

def create_folder(folder_name):
    # 创建文件夹
    os.makedirs(folder_name, exist_ok=True)

def save_image(img_url, folder_name):
    # 保存图片
    if img_url and img_url.startswith('http'):
        img_data = requests.get(img_url).content
        img_name = img_url.split('/')[-1]
        img_name = clean_filename(img_name)  # 清理文件名
        img_path = os.path.join(folder_name, img_name)
        with open(img_path, 'wb') as img_file:
            img_file.write(img_data)
            print(f"保存图片: {img_path}")

def scroll_page(driver, scroll_times, delay):
    # 模拟滚动页面以加载更多图片
    for i in range(scroll_times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

def get_image_elements(driver):
    # 等待页面加载完成
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'img')))

    # 获取所有图片元素
    img_elements = driver.find_elements(By.CSS_SELECTOR, 'img[src^="http"]')
    return img_elements

def save_images_from_url(url):
    # 解析URL获取域名
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # 创建文件夹
    folder_name = domain
    create_folder(folder_name)

    # 配置Selenium WebDriver
    options = Options()
    options.headless = True  # 无界面模式
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0")
    driver = webdriver.Firefox(options=options)

    try:
        # 加载网页
        driver.get(url)

        # 模拟滚动页面以加载更多图片（根据需要调整滚动次数和延迟时间）
        scroll_times = 5
        delay = 2
        scroll_page(driver, scroll_times, delay)

        # 获取所有图片元素
        img_elements = get_image_elements(driver)

        # 保存图片
        for img_element in img_elements:
            img_url = img_element.get_attribute('src')
            save_image(img_url, folder_name)

    finally:
        # 关闭浏览器
        driver.quit()

# 输入网站URL
url = input("请输入网站URL: ")
save_images_from_url(url)