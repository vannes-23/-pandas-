# 导入必要的库
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 从指定的 URL 加载数据集
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/auto.csv'
original_df = pd.read_csv(url)

# 将数据集中所有的 '?' 替换为 NaN（缺失值）
df1 = original_df.replace('?', np.nan)

# 为数据框设置列名
headers = ["symboling", "normalized-losses", "make", "fuel-type", "aspiration", "num-of-doors", "body-style",
           "drive-wheels", "engine-location", "wheel-base", "length", "width", "height", "curb-weight", "engine-type",
           "num-of-cylinders", "engine-size", "fuel-system", "bore", "stroke", "compression-ratio", "horsepower",
           "peak-rpm", "city-mpg", "highway-mpg", "price"]
df1.columns = headers

# 检查数据框中每列是否存在缺失值，并统计每列的缺失值数量
missing_data = df1.isnull()  # 生成一个布尔型数据框，True 表示缺失值，False 表示非缺失值
for column in missing_data.columns.tolist():  # 遍历每一列
    print(column)  # 打印当前列名
    print(missing_data[column].value_counts(dropna=False))  # 确保统计结果完整
    print("")  # 打印空行，用于分隔不同列的输出

# 处理缺失值的方法1：将缺失值替换为均值

mean_df1 = df1.copy()  # 创建数据框的副本防止df1数据集被修改

# 确保 'normalized-losses' 列是数值类型并替换缺失值
mean_df1['normalized-losses'] = mean_df1['normalized-losses'].astype(float)  # 转换为浮点型
mean_df1['normalized-losses'] = mean_df1['normalized-losses'].fillna(mean_df1['normalized-losses'].mean())  # 替换缺失值为均值 fillna(value) 会将数据框或系列（DataFrame 或 Series）中的所有 NaN 替换为指定的 value。

# 确保 'bore' 列是数值类型并替换缺失值
mean_df1['bore'] = mean_df1['bore'].astype(float)  # 转换为浮点型
mean_df1['bore'] = mean_df1['bore'].fillna(mean_df1['bore'].mean(axis=0))  # 替换缺失值为均值

#确保 'horsepower' 列是数值类型并替换缺失值
mean_df1['horsepower']=mean_df1['horsepower'].astype(float)
mean_df1['horsepower']=mean_df1['horsepower'].fillna(mean_df1['horsepower'].mean(axis=0))

#确保'peak-rpm'列是数值类型并替换缺失值
mean_df1['peak-rpm']=mean_df1['peak-rpm'].astype(float)
mean_df1['peak-rpm']=mean_df1['peak-rpm'].fillna(mean_df1['peak-rpm'].mean(axis=0))

# 这将显示该列中每种类型的车门数量（如 'Four', 'Two' ）的频数统计
print(mean_df1['num-of-doors'].value_counts())

#'Four' 是该列中最常见的值（众数），因此用它来填补缺失值
mean_df1['num-of-doors'] = mean_df1['num-of-doors'].fillna('Four')

mean_df1.dropna(subset=['price'],axis=0,inplace=True)

mean_df1.dropna(subset=['price'],axis=0)
mean_df1[["bore", "stroke"]] = mean_df1[["bore", "stroke"]].astype("float")
mean_df1[["normalized-losses"]] = mean_df1[["normalized-losses"]].astype("int")
mean_df1[["price"]] = mean_df1[["price"]].astype("float")
mean_df1[["peak-rpm"]] = mean_df1[["peak-rpm"]].astype("float")

# 数据标准化：将 'city-mpg' 列转换为 'city-L/100km'
# 公式：235 / city-mpg
mean_df1['city-L/100km'] = 235 / mean_df1['city-mpg']
mean_df1['highway-L/100km']=235 / mean_df1['highway-mpg']

# 重命名列名
mean_df1.rename(columns={'city-mpg': 'city-L/100km'}, inplace=True)
mean_df1.rename(columns={'highway-mpg':'highway-L/100km'})

#数据归一
mean_df1['length'] = mean_df1['length']/mean_df1['length'].max()
mean_df1['width'] =mean_df1['width']/mean_df1['width'].max()
mean_df1['height']=mean_df1['height']/mean_df1['height'].max()


# 生成散点图以展示 'horsepower' 和 'price' 的关系
plt.figure(figsize=(12, 8))  # 设置图表大小

# 绘制散点图
plt.scatter(mean_df1['horsepower'], mean_df1['price'], color='blue', alpha=0.6, edgecolor='k')

# 设置 x 轴和 y 轴标签
plt.xlabel("Horsepower", fontsize=14)
plt.ylabel("Price", fontsize=14)

# 设置图表标题
plt.title("Relationship between Horsepower and Price", fontsize=16)

# 显示网格线
plt.grid(linestyle='--', alpha=0.7)

# 将图表保存为dpi为300的png文件
plt.savefig("horsepower_distribution.png", dpi=300, bbox_inches='tight')

# 显示图表
plt.show()