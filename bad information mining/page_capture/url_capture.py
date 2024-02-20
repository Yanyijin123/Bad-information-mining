# —*—coding：utf-8-*—
#这个函数是用来获取一个页面所有的链接
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

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


