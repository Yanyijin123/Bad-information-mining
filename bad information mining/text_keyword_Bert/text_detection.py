import csv
import re

def load_bad_words_from_csv(file_path):
    bad_words = []
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            bad_words.extend(row)
    return bad_words

def detect_bad_websites(text, bad_words):
    text = text.lower()

    for word in bad_words:
        if re.search(r'\b' + re.escape(word) + r'\b', text, flags=re.IGNORECASE):
            return True

    return False

# 从CSV文件加载不良关键词列表
bad_words = load_bad_words_from_csv('C:\\Users\\吴伊\\bad_words.csv')

text = '这是一段包含不良关键词的文本'
if detect_bad_websites(text, bad_words):
    print('该文本包含不良内容')
else:
    print('该文本不包含不良内容')
