import pandas as pd
from link_processor import process_links

def extract_links_from_excel(file_path):
    # 读取 Excel 文件
    df = pd.read_excel(file_path)

    # 将整个 DataFrame 传递给 process_links() 函数
    process_links(df)

# 读取Excel文件
excel_file_path = 'testurl.xlsx'
# 提取链接并处理
extract_links_from_excel(excel_file_path)
