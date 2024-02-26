import urllib.request  # 导入用于打开URL的扩展库模块
import urllib.parse
import re  # 导入正则表达式模块


def open_url(url):
    req = urllib.request.Request(url)  # 将Request类实例化并传入url为初始值，然后赋值给req
    # 添加header，伪装成浏览器
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0')
    # 访问url，并将页面的二进制数据赋值给page
    page = urllib.request.urlopen(req)
    # 将page中的内容转换为utf-8编码
    html = page.read().decode('utf-8')

    return html


def get_img(html):
    # [^"]+\.jpg 匹配除"以外的所有字符多次,后面跟上转义的.和png
    p = r'(http.:[\S]*?.(jpg|jpeg|png|gif|bmp|webp))'
    # 返回正则表达式在字符串中所有匹配结果的列表
    imglist = re.findall(p, html)
    print("List of Img: " + str(imglist))
    # 循环遍历列表的每一个值
    for img in imglist:
        # 以/为分隔符，-1返回最后一个值
        filename = img[0].split("/")[-1]
        # 访问each，并将页面的二进制数据赋值给photo
        photo = urllib.request.urlopen(img[0])
        w = photo.read()
        # 打开指定文件，并允许写入二进制数据
        f = open('D:/test/' + filename, 'wb')
        # 写入获取的数据
        f.write(w)
        # 关闭文件
        f.close()
        print(filename + " have been download...")


# 该模块既可以导入到别的模块中使用，另外该模块也可自我执行
if __name__ == '__main__':
    # 定义url
    url = "https://movie.douban.com/top250"
    # 将url作为open_url()的参数，然后将open_url()的返回值作为参数赋给get_img()
    get_img(open_url(url))
    print("all over...")