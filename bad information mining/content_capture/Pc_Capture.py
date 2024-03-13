import asyncio
from playwright.async_api import async_playwright
import requests
from io import BytesIO
from PIL import Image
import os

async def wait_for_all_images_loaded(page, folder_path):
    print("等待页面加载...")
    # 等待页面加载完成
    await page.wait_for_load_state("networkidle")

    print("等待所有图片加载...")
    # 等待所有图片加载完成
    while True:
        # 获取所有图片元素
        images = await page.query_selector_all('img')
        # 获取所有图片的 URL
        image_urls = [await image.evaluate('(img) => img.src') for image in images]

        # 获取通过 CSS background-image 加载的图片
        background_images = await page.evaluate('''() => {
            const backgroundImages = [];
            const elements = document.querySelectorAll('*');
            elements.forEach(element => {
                const backgroundImage = window.getComputedStyle(element).getPropertyValue('background-image');
                if (backgroundImage && backgroundImage !== 'none' && backgroundImage.startsWith('url(')) {
                    const imageUrl = backgroundImage.match(/url\(['"]?(.*?)['"]?\)/i)[1];
                    backgroundImages.push(imageUrl);
                }
            });
            return backgroundImages;
        }''')
        # 合并图片 URL
        image_urls.extend(background_images)
        # 去重
        image_urls = list(set(image_urls))
        # 去除不以 http:// 或 https:// 开头的 URL
        image_urls = [url for url in image_urls if url.startswith("http://") or url.startswith("https://")]

        # 将 URL 存入文本文件
        with open(f'{folder_path}/Pc-image_urls.txt', 'w') as txt_file:
            for url in image_urls:
                txt_file.write(f"{url}\n")

        # 保存所有图片到文件夹
        processed_urls = set()  # 用于存储已经处理过的图片 URL

        for i, url in enumerate(image_urls):
            if url not in processed_urls:  # 检查是否已经处理过该 URL
                try:
                    # 从 URL 中获取图片数据
                    response = requests.get(url,timeout=5) #设置超时时间为5s
                    response.raise_for_status() #若请求失败，立即抛出异常

                    img_data = BytesIO(response.content)

                    # 打开图片并转换格式为 PNG
                    img = Image.open(img_data)
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')

                    # 提取文件名
                    filename = os.path.basename(url)
                    # 将文件名的扩展名替换为png
                    filename = os.path.splitext(filename)[0] + '.png'

                    # 保存为 PNG 格式
                    output_path = os.path.join(folder_path, filename)
                    img.save(output_path, 'PNG')

                    print(f"转换完成，已保存为 {output_path}")
                except requests.Timeout:
                    print(f'转换超时:{url}')
                except Exception as e:
                    print(f"转换失败: {e}")

        # 清空已处理的 URL 集合
        processed_urls.clear()

        # 检查是否所有图片都加载完成
        loaded = await asyncio.gather(*[page.evaluate(f"""
            (url) => {{
                return new Promise(resolve => {{
                    const img = new Image();
                    img.onload = () => resolve(true);
                    img.onerror = () => resolve(false);
                    img.src = url;
                }});
            }}
        """, url) for url in image_urls if url])

        if all(loaded):
            print("所有图片加载完成！")
            break
        else:
            print("部分图片加载失败。")
            break



async def save_text_content(page, file_path):
    print("正在保存文本内容...")
    content = await page.evaluate("document.body.innerText")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    print("文本内容保存完成！")


async def slow_scroll_to_bottom(page):
    print("慢慢地滚动到页面底部...")
    # 获取页面高度
    page_height = await page.evaluate("document.body.scrollHeight")
    current_position = 0
    while current_position < page_height:
        await page.evaluate(f"window.scrollTo(0, {current_position})")
        current_position += 200  # 每次滚动100像素
        await asyncio.sleep(0.8)  # 等待一小段时间

async def capture_screenshots():
    # url = "https://zhujikong.net/"
    # url = "https://vidhub2.cc/voddetail/77102.html"
    url = "https://www.fcwei.com/vod/fengkuangdeshitou.html"
    folder_name = url.replace('/', '_').replace(':', '_').replace('.', '_')
    folder_path = f"./{folder_name}"  # 图片保存文件夹路径
    image_path = f"{folder_path}./Pc-screenshots"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if not os.path.exists(image_path):
        os.makedirs(image_path)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # 设置 headless 参数为 False，启动可见的浏览器
        page = await browser.new_page()

        # 处理 JavaScript 弹窗
        popup_loaded = asyncio.Future()
        page.on("dialog", lambda dialog: asyncio.ensure_future(dialog.dismiss()))
        page.on("dialog", lambda dialog: popup_loaded.set_result(True))

        print("正在打开页面...")
        try:
            await asyncio.wait_for(page.goto(url, wait_until='load'), timeout=15)  # 设置超时为60秒
            print("页面加载完成！")
        except asyncio.TimeoutError:
            print("页面加载超时！")

        # 慢慢地滚动到页面底部
        await slow_scroll_to_bottom(page)

        # 等待 JavaScript 弹窗加载成功
        print("等待 JavaScript 弹窗加载...")
        try:
            await asyncio.wait_for(popup_loaded, timeout=10)
        except asyncio.TimeoutError:
            print("等待 JavaScript 弹窗加载超时！")

        # 保存文本内容到文件
        await save_text_content(page, f"{folder_path}./Pc-content.txt")

        print("成功保存文本！")


        height = await page.evaluate("document.body.clientHeight")
        await page.set_viewport_size({'width':1920,'height':height})
        print("开始截图...")
        # path_screen = f'./{folder_path}./screenshoot.png'
        # await page.content_capture(path='./sc0.png',full_page=True)
        await page.screenshot(path=folder_path+'./Pc-screenshoot.png',full_page=True)

        print("等待所有图片加载...")
        await wait_for_all_images_loaded(page, image_path)

        print("over")

async def main():
    await capture_screenshots()

if __name__ == "__main__":
    asyncio.run(main())


