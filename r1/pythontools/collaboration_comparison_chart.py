import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import defaultdict
import numpy as np

print("开始分析高活跃度与低活跃度作者的合作差异...")

# 1. 读取数据文件
print("读取数据文件...")

# 读取高活跃度作者表
high_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\highly_productive_scholars.csv'
df_high = pd.read_csv(high_file)
print(f"高活跃度作者表包含 {len(df_high)} 位作者")

# 读取作者学科分类表
subject_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\unique_authors_with_subject.csv'
df_subject = pd.read_csv(subject_file)
print(f"作者学科表包含 {len(df_subject)} 位作者")

# 2. 区分高活跃度和低活跃度作者
print("区分作者类型...")

# 创建高活跃度作者集合
high_authors = set(df_high['Author'])

# 创建所有作者的总论文数映射
author_total_papers = {}
for _, row in df_subject.iterrows():
    author = row['Author']
    total_papers = int(row['Total_Papers'])
    author_total_papers[author] = total_papers

# 分离出低活跃度作者（不在high_authors中且总论文数<4）
low_authors = []
for author, total_papers in author_total_papers.items():
    if author not in high_authors and total_papers < 4:
        low_authors.append(author)

print(f"低活跃度作者数量: {len(low_authors)}")
print(f"总作者数: {len(high_authors) + len(low_authors)}")

# 3. 处理04表，计算每位作者的合作论文数
print("处理04表，计算合作论文数...")

# 使用pandas读取04表的Diaspora_Author_Names列
excel_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\04_Diaspora_Articles_12195(1).xlsx'
print("正在读取04表...")

# 只读取需要的列，减少内存使用
df_04 = pd.read_excel(excel_file, sheet_name=0, usecols=['Diaspora_Author_Names'], engine='openpyxl')
print(f"04表包含 {len(df_04)} 条记录")

# 计算每位作者的合作论文数
author_collab_papers = defaultdict(int)

for idx, row in df_04.iterrows():
    if idx % 2000 == 0:  # 每处理2000条记录显示进度
        print(f"处理了 {idx} 条记录...")
    
    if pd.notna(row['Diaspora_Author_Names']):
        authors = [author.strip() for author in str(row['Diaspora_Author_Names']).split(';') if author.strip()]
        num_authors = len(authors)
        
        if num_authors > 1:  # 这是一篇合作论文
            for author in authors:
                if author in author_total_papers:  # 只统计我们关注的作者
                    author_collab_papers[author] += 1

print(f"已计算 {len(author_collab_papers)} 位作者的合作论文数")

# 4. 计算每位作者的合作率
print("计算作者合作率...")

# 高活跃度作者的合作率
high_collab_rates = []
high_total_papers_list = []
high_collab_papers_list = []

for author in high_authors:
    if author in author_total_papers:
        total = author_total_papers[author]
        collab = author_collab_papers.get(author, 0)
        
        if total > 0:
            rate = collab / total
            high_collab_rates.append(rate)
            high_total_papers_list.append(total)
            high_collab_papers_list.append(collab)

# 低活跃度作者的合作率
low_collab_rates = []
low_total_papers_list = []
low_collab_papers_list = []

for author in low_authors[:1000]:  # 只取1000位低活跃度作者作为样本，避免处理时间过长
    if author in author_total_papers:
        total = author_total_papers[author]
        collab = author_collab_papers.get(author, 0)
        
        if total > 0:
            rate = collab / total
            low_collab_rates.append(rate)
            low_total_papers_list.append(total)
            low_collab_papers_list.append(collab)

print(f"高活跃度作者有效样本数: {len(high_collab_rates)}")
print(f"低活跃度作者有效样本数: {len(low_collab_rates)}")

# 5. 计算统计指标
print("\n计算统计指标...")

# 高活跃度作者统计
high_stats = {
    'count': len(high_collab_rates),
    'avg_rate': np.mean(high_collab_rates) if high_collab_rates else 0,
    'median_rate': np.median(high_collab_rates) if high_collab_rates else 0,
    'avg_total': np.mean(high_total_papers_list) if high_total_papers_list else 0,
    'avg_collab': np.mean(high_collab_papers_list) if high_collab_papers_list else 0
}

# 低活跃度作者统计
low_stats = {
    'count': len(low_collab_rates),
    'avg_rate': np.mean(low_collab_rates) if low_collab_rates else 0,
    'median_rate': np.median(low_collab_rates) if low_collab_rates else 0,
    'avg_total': np.mean(low_total_papers_list) if low_total_papers_list else 0,
    'avg_collab': np.mean(low_collab_papers_list) if low_collab_papers_list else 0
}

# 打印统计结果
print("\n=== 高活跃度作者统计 ===")
print(f"作者数量: {high_stats['count']}")
print(f"平均合作率: {high_stats['avg_rate']:.4f}")
print(f"中位数合作率: {high_stats['median_rate']:.4f}")
print(f"平均发表论文数: {high_stats['avg_total']:.2f}")
print(f"平均合作论文数: {high_stats['avg_collab']:.2f}")

print("\n=== 低活跃度作者统计 ===")
print(f"作者数量: {low_stats['count']}")
print(f"平均合作率: {low_stats['avg_rate']:.4f}")
print(f"中位数合作率: {low_stats['median_rate']:.4f}")
print(f"平均发表论文数: {low_stats['avg_total']:.2f}")
print(f"平均合作论文数: {low_stats['avg_collab']:.2f}")

# 6. 生成对比图表
print("\n生成对比图表...")

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 创建图表目录
output_dir = r'f:\projects\nlp\NLP-Midterm\r1\maps\background'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 图表1: 平均合作率对比
plt.figure(figsize=(8, 6))

categories = ['Highly Productive', 'Low Productive']
avg_rates = [high_stats['avg_rate'], low_stats['avg_rate']]

bars = plt.bar(categories, avg_rates, color=['#4ECDC4', '#FF6B6B'], width=0.5)

plt.title('Average Collaboration Rate Comparison', fontsize=16)
plt.ylabel('Collaboration Rate', fontsize=12)
plt.ylim(0, 1)

# 在柱子上显示数值
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
             f'{height:.4f}', ha='center', va='bottom')

# 添加网格线
plt.grid(axis='y', alpha=0.3)

# 保存图表
chart1_file = os.path.join(output_dir, 'collaboration_rate_comparison.png')
plt.savefig(chart1_file, dpi=300, bbox_inches='tight')
print(f"图表1已保存到: {chart1_file}")

# 图表2: 合作率分布箱线图
plt.figure(figsize=(10, 6))

# 将数据整理为箱线图需要的格式
data_to_plot = [high_collab_rates, low_collab_rates]

# 创建箱线图
box = plt.boxplot(data_to_plot, patch_artist=True, labels=categories)

# 设置箱子颜色
colors = ['#4ECDC4', '#FF6B6B']
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

plt.title('Collaboration Rate Distribution', fontsize=16)
plt.ylabel('Collaboration Rate', fontsize=12)
plt.ylim(0, 1)

# 添加网格线
plt.grid(axis='y', alpha=0.3)

# 保存图表
chart2_file = os.path.join(output_dir, 'collaboration_rate_distribution.png')
plt.savefig(chart2_file, dpi=300, bbox_inches='tight')
print(f"图表2已保存到: {chart2_file}")

# 图表3: 平均发表论文数和合作论文数对比
plt.figure(figsize=(10, 6))

# 数据准备
x = np.arange(2)
width = 0.35

total_papers = [high_stats['avg_total'], low_stats['avg_total']]
collab_papers = [high_stats['avg_collab'], low_stats['avg_collab']]

# 创建柱状图
fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width/2, total_papers, width, label='Total Papers', color='#4ECDC4')
rects2 = ax.bar(x + width/2, collab_papers, width, label='Collaboration Papers', color='#FF6B6B')

# 添加标题和标签
ax.set_title('Average Papers Published Comparison', fontsize=16)
ax.set_ylabel('Number of Papers', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()

# 在柱子上显示数值
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

# 保存图表
chart3_file = os.path.join(output_dir, 'papers_comparison.png')
plt.savefig(chart3_file, dpi=300, bbox_inches='tight')
print(f"图表3已保存到: {chart3_file}")

# 7. 生成HTML综合报告
print("\n生成HTML综合报告...")

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Collaboration Comparison between Highly and Low Productive Authors</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        h2 {
            color: #555;
            border-bottom: 2px solid #4ECDC4;
            padding-bottom: 10px;
        }
        .stats-container {
            display: flex;
            justify-content: space-around;
            margin: 30px 0;
        }
        .stats-box {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 1px 5px rgba(0,0,0,0.1);
            text-align: center;
            flex: 1;
            margin: 0 10px;
        }
        .stats-box h3 {
            color: #333;
            margin-top: 0;
        }
        .chart-container {
            margin: 40px 0;
            text-align: center;
        }
        .chart-container img {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #4ECDC4;
            color: white;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Collaboration Comparison between Highly and Low Productive Authors</h1>
        
        <h2>1. Author Classification</h2>
        <div class="stats-container">
            <div class="stats-box">
                <h3>Highly Productive Authors</h3>
                <p style="font-size: 24px; font-weight: bold;">{{high_count}}</p>
                <p>(Publishing ≥4 papers)</p>
            </div>
            <div class="stats-box">
                <h3>Low Productive Authors</h3>
                <p style="font-size: 24px; font-weight: bold;">{{low_count}}</p>
                <p>(Publishing <4 papers)</p>
            </div>
            <div class="stats-box">
                <h3>Total Authors</h3>
                <p style="font-size: 24px; font-weight: bold;">{{total_count}}</p>
                <p>(In this analysis)</p>
            </div>
        </div>
        
        <h2>2. Collaboration Statistics</h2>
        <table>
            <tr>
                <th>Metric</th>
                <th>Highly Productive Authors</th>
                <th>Low Productive Authors</th>
            </tr>
            <tr>
                <td>Average Collaboration Rate</td>
                <td>{{high_avg_rate}}</td>
                <td>{{low_avg_rate}}</td>
            </tr>
            <tr>
                <td>Median Collaboration Rate</td>
                <td>{{high_median_rate}}</td>
                <td>{{low_median_rate}}</td>
            </tr>
            <tr>
                <td>Average Total Papers</td>
                <td>{{high_avg_total}}</td>
                <td>{{low_avg_total}}</td>
            </tr>
            <tr>
                <td>Average Collaboration Papers</td>
                <td>{{high_avg_collab}}</td>
                <td>{{low_avg_collab}}</td>
            </tr>
        </table>
        
        <h2>3. Comparison Charts</h2>
        
        <div class="chart-container">
            <h3>Average Collaboration Rate Comparison</h3>
            <img src="collaboration_rate_comparison.png" alt="Average Collaboration Rate">
        </div>
        
        <div class="chart-container">
            <h3>Collaboration Rate Distribution</h3>
            <img src="collaboration_rate_distribution.png" alt="Collaboration Rate Distribution">
        </div>
        
        <div class="chart-container">
            <h3>Average Papers Published Comparison</h3>
            <img src="papers_comparison.png" alt="Average Papers">
        </div>
        
        <h2>4. Key Findings</h2>
        <ul>
            <li>Highly productive authors have published an average of {{high_avg_total}} papers, while low productive authors have published an average of {{low_avg_total}} papers.</li>
            <li>The average collaboration rate of highly productive authors is {{high_avg_rate}}, compared to {{low_avg_rate}} for low productive authors.</li>
            <li>Highly productive authors have published an average of {{high_avg_collab}} collaboration papers, while low productive authors have published an average of {{low_avg_collab}}.</li>
        </ul>
    </div>
</body>
</html>'''

# 替换HTML中的占位符
html_content = html_content.replace('{{high_count}}', str(high_stats['count']))
html_content = html_content.replace('{{low_count}}', str(low_stats['count']))
html_content = html_content.replace('{{total_count}}', str(high_stats['count'] + low_stats['count']))
html_content = html_content.replace('{{high_avg_rate}}', f'{high_stats["avg_rate"]:.4f}')
html_content = html_content.replace('{{low_avg_rate}}', f'{low_stats["avg_rate"]:.4f}')
html_content = html_content.replace('{{high_median_rate}}', f'{high_stats["median_rate"]:.4f}')
html_content = html_content.replace('{{low_median_rate}}', f'{low_stats["median_rate"]:.4f}')
html_content = html_content.replace('{{high_avg_total}}', f'{high_stats["avg_total"]:.2f}')
html_content = html_content.replace('{{low_avg_total}}', f'{low_stats["avg_total"]:.2f}')
html_content = html_content.replace('{{high_avg_collab}}', f'{high_stats["avg_collab"]:.2f}')
html_content = html_content.replace('{{low_avg_collab}}', f'{low_stats["avg_collab"]:.2f}')

# 保存HTML报告
html_file = os.path.join(output_dir, 'collaboration_comparison_report.html')
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"HTML综合报告已保存到: {html_file}")
print("\n分析和图表生成完成！")
print(f"\n生成的文件:")
print(f"1. {chart1_file} - 平均合作率对比图")
print(f"2. {chart2_file} - 合作率分布箱线图")
print(f"3. {chart3_file} - 论文发表情况对比图")
print(f"4. {html_file} - 综合分析报告")
