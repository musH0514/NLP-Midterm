import pandas as pd
import os
import numpy as np

print("开始更新collaboration_comparison_report.html文件...")

# 1. 读取数据
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
high_authors_set = set(df_high['Author'])

# 创建所有作者的总论文数映射
author_total_papers = {}
for _, row in df_subject.iterrows():
    author = row['Author']
    total_papers = int(row['Total_Papers'])
    author_total_papers[author] = total_papers

# 确定低活跃度作者（不在高活跃度作者集合中）
low_authors = [author for author in author_total_papers if author not in high_authors_set]

print(f"高活跃度作者数量: {len(high_authors_set)}")
print(f"低活跃度作者数量: {len(low_authors)}")
print(f"总作者数: {len(author_total_papers)}")

# 3. 计算合作论文数（基于最新数据）
print("计算合作论文数...")

# 使用之前生成的合作分析数据
collab_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\collaboration_comparison_result.csv'
df_collab = pd.read_csv(collab_file)

# 提取统计数据
high_stats = {
    'count': int(df_collab[df_collab['Metric'] == 'Number of Authors']['Highly Productive Authors'].iloc[0]),
    'avg_rate': float(df_collab[df_collab['Metric'] == 'Average Collaboration Rate']['Highly Productive Authors'].iloc[0]),
    'median_rate': float(df_collab[df_collab['Metric'] == 'Median Collaboration Rate']['Highly Productive Authors'].iloc[0])
}

low_stats = {
    'count': int(df_collab[df_collab['Metric'] == 'Number of Authors']['Low Productive Authors'].iloc[0]),
    'avg_rate': float(df_collab[df_collab['Metric'] == 'Average Collaboration Rate']['Low Productive Authors'].iloc[0]),
    'median_rate': float(df_collab[df_collab['Metric'] == 'Median Collaboration Rate']['Low Productive Authors'].iloc[0])
}

# 计算平均发表论文数
high_avg_papers = df_high['Articles'].mean()
low_avg_papers = df_subject[~df_subject['Author'].isin(high_authors_set)]['Total_Papers'].mean()

# 计算平均合作论文数（估算）
high_avg_collab = high_avg_papers * high_stats['avg_rate']
low_avg_collab = low_avg_papers * low_stats['avg_rate']

print("\n=== 统计数据 ===")
print(f"高活跃度作者:")
print(f"  数量: {high_stats['count']}")
print(f"  平均合作率: {high_stats['avg_rate']:.4f}")
print(f"  中位数合作率: {high_stats['median_rate']:.4f}")
print(f"  平均发表论文数: {high_avg_papers:.2f}")
print(f"  平均合作论文数: {high_avg_collab:.2f}")

print(f"\n低活跃度作者:")
print(f"  数量: {low_stats['count']}")
print(f"  平均合作率: {low_stats['avg_rate']:.4f}")
print(f"  中位数合作率: {low_stats['median_rate']:.4f}")
print(f"  平均发表论文数: {low_avg_papers:.2f}")
print(f"  平均合作论文数: {low_avg_collab:.2f}")

# 4. 更新HTML报告
print("\n更新HTML报告...")

# 读取现有的HTML报告
report_file = r'f:\projects\nlp\NLP-Midterm\r1\maps\background\collaboration_comparison_report.html'

with open(report_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 替换数据
# Author Classification部分
html_content = html_content.replace('<p style="font-size: 24px; font-weight: bold;">644</p>', f'<p style="font-size: 24px; font-weight: bold;">{high_stats["count"]}</p>')
html_content = html_content.replace('<p style="font-size: 24px; font-weight: bold;">1000</p>', f'<p style="font-size: 24px; font-weight: bold;">{low_stats["count"]}</p>')
html_content = html_content.replace('<p style="font-size: 24px; font-weight: bold;">1644</p>', f'<p style="font-size: 24px; font-weight: bold;">{high_stats["count"] + low_stats["count"]}</p>')
# 更新高活跃度作者定义
html_content = html_content.replace('<p>(Publishing ≥4 papers)</p>', '<p>(Publishing ≥5 papers in any 5-year period)</p>')
# 更新低活跃度作者定义，确保包含所有不符合高活跃度定义的作者
html_content = html_content.replace('<p>(Publishing <4 papers)</p>', '<p>(Not meeting highly productive criteria)</p>')

# Collaboration Statistics表格
html_content = html_content.replace('<td>0.3024</td>', f'<td>{high_stats["avg_rate"]:.4f}</td>')
html_content = html_content.replace('<td>0.2322</td>', f'<td>{low_stats["avg_rate"]:.4f}</td>')
html_content = html_content.replace('<td>0.2500</td>', f'<td>{high_stats["median_rate"]:.4f}</td>')
html_content = html_content.replace('<td>6.92</td>', f'<td>{high_avg_papers:.2f}</td>')
html_content = html_content.replace('<td>1.40</td>', f'<td>{low_avg_papers:.2f}</td>')
html_content = html_content.replace('<td>2.00</td>', f'<td>{high_avg_collab:.2f}</td>')
html_content = html_content.replace('<td>0.33</td>', f'<td>{low_avg_collab:.2f}</td>')

# Key Findings部分
html_content = html_content.replace('Highly productive authors have published an average of 6.92 papers, while low productive authors have published an average of 1.40 papers.', f'Highly productive authors have published an average of {high_avg_papers:.2f} papers, while low productive authors have published an average of {low_avg_papers:.2f} papers.')
html_content = html_content.replace('The average collaboration rate of highly productive authors is 0.3024, compared to 0.2322 for low productive authors.', f'The average collaboration rate of highly productive authors is {high_stats["avg_rate"]:.4f}, compared to {low_stats["avg_rate"]:.4f} for low productive authors.')
html_content = html_content.replace('Highly productive authors have published an average of 2.00 collaboration papers, while low productive authors have published an average of 0.33.', f'Highly productive authors have published an average of {high_avg_collab:.2f} collaboration papers, while low productive authors have published an average of {low_avg_collab:.2f}.')

# 保存更新后的HTML报告
with open(report_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"HTML报告已更新: {report_file}")

# 5. 检查更新是否成功
print("\n验证更新内容...")

# 读取更新后的文件并检查几个关键数据点
with open(report_file, 'r', encoding='utf-8') as f:
    updated_content = f.read()

# 检查几个关键数据点是否已更新
check_points = [
    f'{high_stats["count"]}',
    f'{low_stats["count"]}',
    f'{high_stats["avg_rate"]:.4f}',
    f'{low_stats["avg_rate"]:.4f}'
]

all_updated = True
for point in check_points:
    if point not in updated_content:
        print(f"警告: 数据点 {point} 未在更新后的报告中找到")
        all_updated = False
    else:
        print(f"✓ 数据点 {point} 已成功更新")

if all_updated:
    print("\n=== 更新完成！ ===")
    print(f"collaboration_comparison_report.html已成功更新")
    print(f"新的高活跃度作者定义：任何5年区间内发表文章≥5篇的作者")
else:
    print("\n=== 更新完成，但有部分数据可能未成功更新 ===")
    print("请检查HTML文件内容")
