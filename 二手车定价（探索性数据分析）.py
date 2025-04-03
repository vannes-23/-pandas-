import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/auto.csv'
original_df = pd.read_csv(url)

df1 = original_df.replace('?', np.nan)

headers = ["symboling", "normalized-losses", "make", "fuel-type", "aspiration", "num-of-doors", "body-style",
           "drive-wheels", "engine-location", "wheel-base", "length", "width", "height", "curb-weight", "engine-type",
           "num-of-cylinders", "engine-size", "fuel-system", "bore", "stroke", "compression-ratio", "horsepower",
           "peak-rpm", "city-mpg", "highway-mpg", "price"]
df1.columns = headers

missing_data = df1.isnull()
for column in missing_data.columns.tolist():
    print(column)
    print(missing_data[column].value_counts(dropna=False))
    print("")

mean_df1 = df1.copy()

mean_df1['normalized-losses'] = mean_df1['normalized-losses'].astype(float)
mean_df1['normalized-losses'] = mean_df1['normalized-losses'].fillna(mean_df1['normalized-losses'].mean())

mean_df1['bore'] = mean_df1['bore'].astype(float)
mean_df1['bore'] = mean_df1['bore'].fillna(mean_df1['bore'].mean(axis=0))

mean_df1['horsepower'] = mean_df1['horsepower'].astype(float)
mean_df1['horsepower'] = mean_df1['horsepower'].fillna(mean_df1['horsepower'].mean(axis=0))

mean_df1['peak-rpm'] = mean_df1['peak-rpm'].astype(float)
mean_df1['peak-rpm'] = mean_df1['peak-rpm'].fillna(mean_df1['peak-rpm'].mean(axis=0))

print(mean_df1['num-of-doors'].value_counts())

mean_df1['num-of-doors'] = mean_df1['num-of-doors'].fillna('Four')

mean_df1.dropna(subset=['price'], axis=0, inplace=True)

mean_df1[["bore", "stroke"]] = mean_df1[["bore", "stroke"]].astype("float")
mean_df1[["normalized-losses"]] = mean_df1[["normalized-losses"]].astype("int")
mean_df1[["price"]] = mean_df1[["price"]].astype("float")
mean_df1[["peak-rpm"]] = mean_df1[["peak-rpm"]].astype("float")

mean_df1['city-L/100km'] = 235 / mean_df1['city-mpg']
mean_df1['highway-L/100km'] = 235 / mean_df1['highway-mpg']

mean_df1.rename(columns={'city-mpg': 'city-L/100km'}, inplace=True)
mean_df1.rename(columns={'highway-mpg': 'highway-L/100km'})

mean_df1['length'] = mean_df1['length'] / mean_df1['length'].max()
mean_df1['width'] = mean_df1['width'] / mean_df1['width'].max()
mean_df1['height'] = mean_df1['height'] / mean_df1['height'].max()

df1 = mean_df1

drive_wheels_counnts = df1['drive-wheels'].value_counts().to_frame()
drive_wheels_counnts.reset_index(inplace=True)
drive_wheels_counnts = drive_wheels_counnts.rename(columns={'drive-wheels': 'Value-counts'})
drive_wheels_counnts.index.name = 'drive-wheels'

engine_loc_counts = df1['engine-location'].value_counts().to_frame()
engine_loc_counts.reset_index(inplace=True)
engine_loc_counts = engine_loc_counts.rename(columns={'engine-location': 'value-counts'})
engine_loc_counts.index.name = 'engine-loaction'

df1_groupby_one = df1[['drive-wheels', 'body-style', 'price']]
df1_grouped = df1_groupby_one.groupby('drive-wheels', as_index=False).agg({'price': 'mean'})
grouped_test1 = df1_groupby_one.groupby(['drive-wheels', 'body-style'], as_index=False).mean()

grouped_pivot = grouped_test1.pivot(index='drive-wheels', columns='body-style')

grouped_pivot = grouped_pivot.fillna(0)
grouped_pivot = grouped_pivot.astype(float)

fig, ax = plt.subplots(figsize=(10, 8))  # 设置图表大小
im = ax.pcolor(grouped_pivot, cmap='RdBu')  # 使用 RdBu 配色方案

row_labels = grouped_pivot.columns.levels[1]  # 提取列标签（车身类型）
col_labels = grouped_pivot.index  # 提取行标签（驱动类型）

# 调整刻度位置到单元格中心 shape中 0代表column 1代表row
ax.set_xticks(np.arange(grouped_pivot.shape[1]) + 0.5, minor=False)
ax.set_yticks(np.arange(grouped_pivot.shape[0]) + 0.5, minor=False)

# 设置刻度标签
ax.set_xticklabels(row_labels, minor=False)
ax.set_yticklabels(col_labels, minor=False)

# 旋转 x 轴标签以避免重叠
plt.xticks(rotation=45)

# 添加颜色条
cbar = fig.colorbar(im, ax=ax)
cbar.ax.set_ylabel('Average Price', rotation=270, labelpad=15)  # 设置颜色条标签

# 添加网格线
ax.grid(which="major", color="gray", linestyle="--", linewidth=0.5)

# 添加标题
plt.title("Pseudocolor Plot of Grouped Pivot Table")

# 显示图表
plt.show()