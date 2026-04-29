import pandas as pd
import os

print("开始分析作者合作情况...")

# 1. 读取04表，提取作者信息
print("正在读取04表...")
excel_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\04_Diaspora_Articles_12195(1).xlsx'

# 使用openpyxl读取Diaspora_Author_Names列
df_04 = pd.read_excel(excel_file, sheet_name=0, usecols=['Diaspora_Author_Names'], engine='openpyxl')

print(f"04表包含 {len(df_04)} 条记录")

# 2. 处理每篇文章，记录文章作者数量
print("正在处理文章作者信息...")
article_collaboration = []  # 存储每篇文章的作者数量和作者列表

for idx, row in df_04.iterrows():
    if pd.notna(row['Diaspora_Author_Names']):
        authors = [author.strip() for author in str(row['Diaspora_Author_Names']).split(';') if author.strip()]
        num_authors = len(authors)
        is_collaborative = num_authors > 1
        article_collaboration.append({'authors': authors, 'num_authors': num_authors, 'is_collaborative': is_collaborative})
    else:
        article_collaboration.append({'authors': [], 'num_authors': 0, 'is_collaborative': False})

# 3. 计算每个作者的合作统计
print("\n计算每个作者的合作统计...")
author_stats = {}

for article in article_collaboration:
    if article['num_authors'] == 0:
        continue
    
    for author in article['authors']:
        if author not in author_stats:
            author_stats[author] = {'total_papers': 0, 'collaboration_papers': 0}
        
        author_stats[author]['total_papers'] += 1
        if article['is_collaborative']:
            author_stats[author]['collaboration_papers'] += 1

print(f"已计算 {len(author_stats)} 位作者的合作统计")

# 4. 读取作者总列表
print("\n读取作者总列表...")
subject_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\unique_authors_with_subject.csv'
df_subject = pd.read_csv(subject_file)

# 5. 生成作者合作分析表
print("\n生成作者合作分析表...")
author_list = []

for _, row in df_subject.iterrows():
    author = row['Author']
    total_papers = int(row['Total_Papers'])
    
    if author in author_stats:
        collab_papers = author_stats[author]['collaboration_papers']
        # 确保统计的总论文数与subject表一致
        if author_stats[author]['total_papers'] != total_papers:
            print(f"警告：作者 {author} 的论文数不匹配 ({author_stats[author]['total_papers']} vs {total_papers})")
    else:
        collab_papers = 0
    
    # 计算合作率
    if total_papers > 0:
        collab_rate = round(collab_papers / total_papers, 4)
    else:
        collab_rate = 0.0
    
    author_list.append({
        'Author': author,
        'Total_Papers': total_papers,
        'Collaboration_Papers': collab_papers,
        'Collaboration_Rate': collab_rate
    })

# 创建DataFrame
df_collaboration = pd.DataFrame(author_list)

# 保存到文件
output_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\author_collaboration_analysis.csv'
df_collaboration.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"作者合作分析表已保存到: {output_file}")

# 6. 区分高活跃度和低活跃度作者
print("\n区分高活跃度和低活跃度作者...")

# 高活跃度作者：发表论文数 >= 4
highly_productive = df_collaboration[df_collaboration['Total_Papers'] >= 4].copy()

# 低活跃度作者：发表论文数 < 4
low_productive = df_collaboration[df_collaboration['Total_Papers'] < 4].copy()

print(f"高活跃度作者: {len(highly_productive)} 位")
print(f"低活跃度作者: {len(low_productive)} 位")

# 7. 计算两类作者的合作率统计
print("\n计算合作率统计:")

# 高活跃度作者统计
high_stats = {
    'Average Collaboration Rate': highly_productive['Collaboration_Rate'].mean(),
    'Median Collaboration Rate': highly_productive['Collaboration_Rate'].median(),
    'Max Collaboration Rate': highly_productive['Collaboration_Rate'].max(),
    'Min Collaboration Rate': highly_productive['Collaboration_Rate'].min(),
    'Count': len(highly_productive)
}

# 低活跃度作者统计
low_stats = {
    'Average Collaboration Rate': low_productive['Collaboration_Rate'].mean(),
    'Median Collaboration Rate': low_productive['Collaboration_Rate'].median(),
    'Max Collaboration Rate': low_productive['Collaboration_Rate'].max(),
    'Min Collaboration Rate': low_productive['Collaboration_Rate'].min(),
    'Count': len(low_productive)
}

print("\n高活跃度作者统计:")
for key, value in high_stats.items():
    if key != 'Count':
        print(f"  {key}: {round(value, 4)}")
    else:
        print(f"  {key}: {value}")

print("\n低活跃度作者统计:")
for key, value in low_stats.items():
    if key != 'Count':
        print(f"  {key}: {round(value, 4)}")
    else:
        print(f"  {key}: {value}")

# 8. 保存对比结果到文件
print("\n保存对比结果到文件...")

comparison_data = {
    'Metric': ['Average Collaboration Rate', 'Median Collaboration Rate', 'Max Collaboration Rate', 'Min Collaboration Rate', 'Number of Authors'],
    'Highly Productive Authors': [round(high_stats['Average Collaboration Rate'], 4),
                                  round(high_stats['Median Collaboration Rate'], 4),
                                  round(high_stats['Max Collaboration Rate'], 4),
                                  round(high_stats['Min Collaboration Rate'], 4),
                                  high_stats['Count']],
    'Low Productive Authors': [round(low_stats['Average Collaboration Rate'], 4),
                               round(low_stats['Median Collaboration Rate'], 4),
                               round(low_stats['Max Collaboration Rate'], 4),
                               round(low_stats['Min Collaboration Rate'], 4),
                               low_stats['Count']]
}

df_comparison = pd.DataFrame(comparison_data)

comparison_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\collaboration_comparison.csv'
df_comparison.to_csv(comparison_file, index=False, encoding='utf-8-sig')
print(f"对比结果已保存到: {comparison_file}")

# 9. 显示一些示例数据
print("\n=== 作者合作分析示例 ===")
print("前10位作者的合作情况:")
print(df_collaboration.head(10))

print("\n=== 合作分析完成！ ===")
print(f"已生成两个文件:")
print(f"1. {output_file} - 所有作者的合作分析表")
print(f"2. {comparison_file} - 高活跃度与低活跃度作者的对比")
