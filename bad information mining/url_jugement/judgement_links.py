#这个函数是使用决策树来判断url的层次
import re

def Judgement_Links(url):
    # 使用正则表达式匹配数字结尾
    if re.search(r'\d/$', url):
        return 1
    # 使用正则表达式匹配以.html结尾
    elif url.endswith('.html'):
        return 2
    else:
        return 0