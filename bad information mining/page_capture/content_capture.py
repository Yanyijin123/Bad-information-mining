# —*—coding：utf-8-*—
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


# 这个函数用来获取页面内部的url链接
def url_Capture(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto(url)
            page.wait_for_load_state("load")
            # 等待10秒钟以确保页面加载完成
            page.wait_for_timeout(10000)
            # 获取页面的 HTML 内容
            html = page.content()
            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(html, 'html.parser')
            Full_link =[]
            # 提取所有链接
            slice_url = [a['href'] for a in soup.find_all('a', href=True)]
            for i_url in slice_url:
                combined_tuple = (i_url, urljoin(url, i_url))
                Full_link .append(combined_tuple)
            unique_Full_link = list(set(Full_link))
            return unique_Full_link,html

        except Exception as e:
            print(f"发生异常: {e}")
            print(f"无法访问网站: {url}")
            return []
        finally:
            # 关闭浏览器
            browser.close()

