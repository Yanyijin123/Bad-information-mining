from math import log2

# import treePlotter # 导入失败


class ID3Tree(object):
    def __init__(self, data, cols):
        self.all_data = data  # 初始化数据集
        self.all_cols = cols  # 初始化数据集的各个列名（类别名）
        self.tree = {}  # 初始化ID3决策树

    def train(self):
        self.tree = self.make_tree(self.all_data, self.all_cols)

    def make_tree(self, data, cols):
        """
        :param data: 数据集：可能是总集，也可能是子集
        :param cols: 列名（特征名）：可能是全列名，也可能是当前数据集去掉最大信息熵特征后的列名集
        :return:树
        """
        all_label_datas = [item[-1] for item in data]  # 所有的标签对应的所有值
        # 1、如果这个数据集的全部标签都是一样的，那么没有属性划分的必要，决策树就一个叶子节点（即拿这个标签直接作为决策）
        if all_label_datas.count(all_label_datas[0]) == len(all_label_datas):
            return all_label_datas[0]
        # 2、如果这个数据集中每条数据（默认每条数据的长度和格式都一样）没有任何属性，只有标签
        # 我们看哪类标签出现的次数最多，直接拿它作为决策结果，这种情况决策树也就一个叶子结点
        elif len(data[0]) == 1:
            # 初始化出现的次数
            max_num = all_label_datas.count(all_label_datas[0])
            # 初始化出现次数最多的标签
            max_sort_data = all_label_datas[0]
            # set对原列表去重，但不改变原列表
            for i in list(set(all_label_datas)):
                if all_label_datas.count(all_label_datas[i]) > max_num:
                    max_num = all_label_datas.count(all_label_datas[i])
                    max_sort_data = i
            return max_sort_data
        # 3、正常情况，我们来构建决策树
        # *** 选取信息熵最大的属性（特征）***
        best_xns_feature_index = self.find_best_xns_feature(data)  # 找到香农熵最大的特征的下标
        best_feature_label = cols[best_xns_feature_index]  # 找到香农熵最大的特征的名称
        tree = {best_feature_label: {}}  # 构造一个（新的）树结点,一个根节点，大括号是子树
        del (cols[best_xns_feature_index])  # 删除数据集中香农熵最大的特征所在的列
        # 抽取最大增益的特征对应的列的数据
        best_xns_feature_values = [item[best_xns_feature_index] for item in data]
        for value in list(set(best_xns_feature_values)):
            # 此时的all_data是上次all_data去掉一列特征得到的
            sub_cols = cols
            sub_data = self.construct_new_dataset(data, best_xns_feature_index, value)
            # 递归构造子树
            tree[best_feature_label][value] = self.make_tree(sub_data, sub_cols)  # 向子树中放入值
        return tree

    def find_best_xns_feature(self, data):
        """
        计算各个特征的香农熵的大小，并返回香农熵最大的特征的下标
        :return: 香农熵最大的特征的下标
        """
        data_num = len(data)  # 数据集中样本的总数
        feature_nums = len(data[0]) - 1  # 数据集中所有特征的数量，-1是因为数据中不止有特征，还有标签
        I = self.calculate_xns(data)  # 数据集（样本标签）的香农熵
        best_xns_feature_value = 0  # 初始化香农熵最大的特征的值
        best_xns_feature_index = -1  # 初始化香农熵最大的特征的下标

        for i in range(feature_nums):
            feat_values = [number[i] for number in data]  # 得到某个特征列（随机变量）下的所有值
            feat_sorts = set(feat_values)  # 去重，得到特征的所有无重复的取值
            E = 0  # 初始化当前特征的信息熵
            # 对当前特征下具有相同特征值的子集，根据正负样本算出信息熵，并乘以prob。在不同特征值下计算完后，进行加和，得到E
            for value in feat_sorts:
                sub_dataset = self.construct_new_dataset(data, i, value)  # 得到i特征下，特征值为value的数据，去除特征i构成的集合
                prob = len(sub_dataset) / float(data_num)  # 特征i的值为value的数据所占的比例
                E += prob * self.calculate_xns(sub_dataset)
            # 用 I 减去 E，得到当前特征的信息增益gain
            gain = I - E  # 当前i特征的信息增益
            # 保留最大的信息熵及其对应的特征索引
            if gain > best_xns_feature_value:
                best_xns_feature_value = gain
                best_xns_feature_index = i

        return best_xns_feature_index  # 返回最大信息增益的特征的下标

    def construct_new_dataset(self, data, axis, value):
        """
        从数据集的某个特征中，选取值为某个特征值的数据，并去掉此特征，然后将这类数据构成新的数据集
        比如，在性别这个特征中，把特征值是男的数据抽出来，然后把这些数据的性别列去掉，构成数据集
        :param data:数据集
        :param axis:数据集中某个特征在数据中的索引
        :param value:此特征下的一个特征值
        :return:数据集中特征值是给定特征值的数据构成的子集
        """
        remain_dataset = []
        for item in data:  # 数据集中的每条数据
            if item[axis] == value:  # 如果这条数据的特征等于给定的某个特征值时
                # 把此条数据去掉这个特征列，重构此条数据
                remain_data = item[:axis]
                remain_data.extend(item[axis + 1:])
                remain_dataset.append(remain_data)  # 将重构后的数据加入列表中
        return remain_dataset

    def calculate_xns(self, data):
        """
        计算给定数据集的香农熵（信息熵）
        :return:数据集的香农熵
        """
        xns = 0.0  # 香农熵
        data_num = len(data)  # 样本集的总数，用于计算分类标签出现的概率

        # 将数据集样本标签的特征值（分类值）放入列表
        all_labels = [c[-1] for c in data]  # c[-1]：即取数据集中的每条数据的标签：Yes 或 No
        # print(all_labels)  # 得到 [Yes,No,No,...] 的结果
        # 按标签的种类进行统计，Yes这一类几个；No这一类几个
        every_label = {}  # 以词典形式存储每个类别（键）及个数（值）
        for item in list(set(all_labels)):  # 对每个类别计数，并放入词典, 其中set(all_labels) = [Yes,No]
            every_label[item] = all_labels.count(item)
        # 计算样本标签的香农熵，即数据集的香农熵
        for item2 in every_label:
            prob = every_label[item2] / float(data_num)  # 每个特征值出现的概率
            xns -= prob * log2(prob)  # xns是全局变量，这样就可以计算关于决策的要考虑的某个随机变量（如收入特征）的香农熵
        return xns



