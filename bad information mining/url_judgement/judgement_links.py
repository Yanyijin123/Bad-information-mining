#这个函数是使用决策树来判断url的层次
#输入为suffix,url_hierarchy,other_urls_count,title_attribute, target_attribute,keywords,response,match
import pandas as pd
from  DT_main import ID3Tree
from DT_Attribute_conversion import get_features

def Judgement_Links(html_content , target_url):
    # 使用正则表达式匹配数字结尾
    # 读取Excel文件
    # 读取 Excel 文件
    df = pd.read_excel('DT_test_data.xlsx')

    # 选择第二列到第9列，使用iloc方法,第一行是标题行
    selected_columns = df.iloc[:, 1:10]

    # 将选定的列转换为列表
    dataset = selected_columns.values.tolist()

    # 前八列的名字（特征列）分别为后缀、url层级、相同层级的url数目、title标志，target标志，关键词标致、响应、
    labels = ['suffix','url_hierarchy','other_urls_count','title_attribute','target_attribute','keywords','response','match']
    id3 = ID3Tree(dataset, labels)  # 实例化决策树对象
    id3.train()
    #print(id3.tree)  # 输出决策树
    # treeplotter.createPlot(id3.tree) # 因treePlotter不能直接导入，这里会报错
    #DT_help.createPlot(id3.tree)  # 可视化决策树


    # 给定新一天的url数据指标，根据决策树，来判断是否会去打球
    def predict_play(tree, new_dic):
        """
        根据构造的决策树，对未知数据进行预测
        :param tree: 决策树（根据已知数据构造的）
        :param new_dic: 一条待预测的数据
        :return:返回叶子节点，也就是最终的决策
        """
        while isinstance(tree, dict):
            key = next(iter(tree))
            tree = tree.get(key, {}).get(new_dic.get(key))
        return tree

    result = get_features(html_content , target_url)
    if result is None:
        jud = 0
    else:
        suffix, url_hierarchy, other_urls_count, title_attribute, target_attribute, keywords, response, match = result

        # 使用特征值进行预测
        jud = predict_play(id3.tree, {
            'suffix': suffix,
            'url_hierarchy': url_hierarchy,
            'other_urls_count': other_urls_count,
            'title_attribute': title_attribute,
            'target_attribute': target_attribute,
            'keywords': keywords,
            'response': response,
            'match': match
        })

    print(jud)
    print(type(jud))
    # 输出决策结果
    return  jud