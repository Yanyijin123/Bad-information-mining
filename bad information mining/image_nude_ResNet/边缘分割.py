import cv2
import numpy as np
import matplotlib.pyplot as plt

def extract_movie_posters(large_image_path, output_path_prefix):
    # 读取大图
    large_image = cv2.imread(large_image_path)

    # 将大图转换为灰度图
    gray_image = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)

    # 使用闭运算连接边缘
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 定义闭运算的内核
    closed_image = cv2.morphologyEx(gray_image, cv2.MORPH_CLOSE, kernel)

    # 使用Canny边缘检测
    edges = cv2.Canny(closed_image, 50, 150, apertureSize=3)

    # 寻找轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 提取包含电影海报的区域
    posters = []  # 用于存储提取的海报
    not_mergeable = []  # 用于存储不可合并的海报
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # 限制提取的区域的最小大小
        if w > 100 and h > 100:
            poster_region = large_image[y:y+h, x:x+w]
            posters.append((x, y, w, h, poster_region))  # 存储海报及其位置信息

    # 检测并合并重叠的海报
    while len(posters) > 1:
        merged = False
        for i in range(len(posters)):
            for j in range(i+1, len(posters)):
                x1, y1, w1, h1, poster1 = posters[i]
                x2, y2, w2, h2, poster2 = posters[j]
                # 检查边缘是否重叠，宽松条件以允许部分重叠
                if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
                    # 根据位置信息从原图中切出相应区域进行合并
                    merged_poster_region = large_image[min(y1, y2):max(y1 + h1, y2 + h2), min(x1, x2):max(x1 + w1, x2 + w2)]
                    posters.pop(j)
                    posters.pop(i)
                    posters.append((min(x1, x2), min(y1, y2), merged_poster_region.shape[1], merged_poster_region.shape[0], merged_poster_region))
                    merged = True
                    break
            if merged:
                break
        if not merged:
            not_mergeable.extend(posters)
            break



    # 将不可合并的海报保存为图片文件
    for i, (x, y, w, h, poster) in enumerate(not_mergeable):
        cv2.imwrite(f'{output_path_prefix}_not_mergeable_{i}.png', poster)
        print(f'Not mergeable movie poster {i} saved successfully.')

    # 显示闭运算后的图像
    plt.imshow(closed_image, cmap='gray')
    plt.title('Closed Image')
    plt.axis('off')
    plt.show()

# 替换成你的大图路径
large_image_path = 'D:\\pic-deal\\segment\\mobile1.jpg'

# 定义输出电影海报的路径前缀
output_path_prefix = 'D:\\pic-deal\\segment\\'

extract_movie_posters(large_image_path, output_path_prefix)
