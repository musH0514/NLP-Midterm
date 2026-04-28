import pandas as pd
import matplotlib.pyplot as plt
import os

# 设置中文字体支持（如果需要）
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 读取学科总数表
totals_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\subject_category_totals.csv'
df_totals = pd.read_csv(totals_file)

# 过滤掉No Papers类别（因为它有0个作者）
df_pie = df_totals[df_totals['Subject_Category'] != 'No Papers']

# 准备数据
labels = df_pie['Subject_Category']
values = df_pie['Author_Count']

# 创建饼状图
fig, ax = plt.subplots(figsize=(12, 8))

# 设置饼状图参数
explode = (0.05, 0, 0, 0, 0)  # 稍微突出第一个部分（人文社科类）
colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FFB3E6']  # 不同颜色

# 绘制饼状图
wedges, texts, autotexts = ax.pie(values, explode=explode, labels=labels, 
                                  colors=colors, autopct='%1.1f%%',
                                  shadow=True, startangle=90)

# 设置文本样式
for text in texts:
    text.set_fontsize(12)
for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_color('white')

# 设置标题
ax.set_title('Distribution of Authors Across Subject Categories', fontsize=16, fontweight='bold')

# 添加图例
ax.legend(wedges, labels, title='Subject Categories', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=12)

# 确保饼状图是圆形
ax.axis('equal')

# 调整布局
plt.tight_layout()

# 创建目标目录（如果不存在）
target_dir = r'f:\projects\nlp\NLP-Midterm\r1\map\background'
os.makedirs(target_dir, exist_ok=True)

# 保存图片
image_path = os.path.join(target_dir, 'author_subject_distribution_pie_chart.png')
plt.savefig(image_path, dpi=300, bbox_inches='tight')

print(f"饼状图已保存到: {image_path}")

# 显示图表
plt.show()
