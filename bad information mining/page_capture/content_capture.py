# —*—coding：utf-8-*—
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

#获取整个页面的内容用来计算链接层级
def content_Capture(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto(url)
            page.wait_for_load_state("load")
            # 获取页面的 HTML 内容
            html = page.content()
            return html  # 返回 HTML 内容
        except Exception as e:
            print(f"发生异常: {e}")
        finally:
            # 关闭浏览器
            browser.close()

#这个函数用来获取页面内部的url链接
def url_Capture(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto(url)
            page.wait_for_load_state("load")
            # 获取页面的 HTML 内容
            html = page.content()
            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(html, 'html.parser')
            # 提取所有链接
            slice_url= [a['href'] for a in soup.find_all('a', href=True)]
            Full_link = [urljoin(url, i_url) for i_url in slice_url]
            # 去重
            Child_url = list(set(Full_link))
            return Child_url
        except Exception as e:
            print(f"发生异常: {e}")
        finally:
            # 关闭浏览器
            browser.close()

