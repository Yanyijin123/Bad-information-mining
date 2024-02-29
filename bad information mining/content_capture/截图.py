import asyncio
from playwright.async_api import async_playwright
import time
async def wait_for_all_images_loaded(page):
    print("等待页面加载...")
    # 等待页面加载完成
    await page.wait_for_load_state("networkidle")

    print("等待所有图片加载...")
    # 等待所有图片加载完成
    while True:
        images = await page.query_selector_all('.iconfont.icon-play.play.hidden-xs img')
        loaded = await asyncio.gather(*[image.evaluate('(img) => img.complete') for image in images])
        if all(loaded):
            print("所有图片加载完成！")
            break
        else:
            print("等待图片加载中...")
            await asyncio.sleep(2)

async def slow_scroll_to_bottom(page):
    print("慢慢地滚动到页面底部...")
    # 获取页面高度
    page_height = await page.evaluate("document.body.scrollHeight")
    current_position = 0
    while current_position < page_height:
        await page.evaluate(f"window.scrollTo(0, {current_position})")
        current_position += 100  # 每次滚动50像素
        await asyncio.sleep(1)  # 等待一小段时间


async def capture_screenshots():
    # start_time = time.time() #开始记录时间
    # url = "https://www.fcwei.com/vod/fengkuangdeshitou.html"
    url = "https://zhujikong.net/"
    # url = "https://www.mjwo.net/play/19279-1-1/"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # 设置 headless 参数为 False，启动可见的浏览器
        page = await browser.new_page()

        # 处理 JavaScript 弹窗
        popup_loaded = asyncio.Future()
        page.on("dialog", lambda dialog: asyncio.ensure_future(dialog.dismiss()))
        page.on("dialog", lambda dialog: popup_loaded.set_result(True))

        print("正在打开页面...")
        try:
            await asyncio.wait_for(page.goto(url, wait_until='load'), timeout=20)  # 设置超时为60秒
            print("页面加载完成！")
        except asyncio.TimeoutError:
            print("页面加载超时！")


        # 慢慢地滚动到页面底部
        await slow_scroll_to_bottom(page)

        # 等待 JavaScript 弹窗加载成功
        print("等待 JavaScript 弹窗加载...")

        try:
            await asyncio.wait_for(popup_loaded, timeout=5)
        except asyncio.TimeoutError:
            print("等待 JavaScript 弹窗加载超时！")
        # await popup_loaded

        print("等待所有图片加载...")
        await wait_for_all_images_loaded(page)

        # 获取整个可视区域的高度
        height = await page.evaluate("document.body.clientHeight")
        # 设置页面视口大小为整个可视区域大小
        await page.set_viewport_size({"width": 1920, "height": height})

        print("开始截图...")
        await page.screenshot(path='./sc0.png')

        print("请手动关闭浏览器窗口！")
        # 不关闭浏览器，等待手动关闭
        # await browser.close()

        # end_time = time.time #记录结束时间
        # total_time = end_time - start_time
        # print(f'程序运行时间为: {total_time}秒')

async def main():
    await capture_screenshots()


if __name__ == "__main__":
    asyncio.run(main())
