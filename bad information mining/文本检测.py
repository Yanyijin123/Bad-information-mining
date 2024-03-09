import re

def detect_bad_websites(text):
    # 定义不良网站关键词列表
    bad_words = ['不良关键词1', '不良关键词2', '不良关键词3']

    # 将文本转换为小写，便于匹配
    text = text.lower()

    for word in bad_words:
        # 使用正则表达式进行匹配
        # re.IGNORECASE参数表示不区分大小写
        if re.search(r'\b' + re.escape(word) + r'\b', text, flags=re.IGNORECASE):
            return True

    return False

# 示例用法
text = '这是一段包含不良关键词的文本'
if detect_bad_websites(text):
    print('该文本包含不良内容')
else:
    print('该文本不包含不良内容')
