import pandas as pd
import os
from collections import defaultdict

print("开始分析作者合作情况...")

# 读取原始04表，提取作者和合作信息
print("正在读取04表...")
excel_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\04_Diaspora_Articles_12195(1).xlsx'

# 使用openpyxl读取特定列
df_04 = pd.read_excel(excel_file, sheet_name=0, usecols=['Diaspora_Author_Names'], engine='openpyxl')

print(f"04表包含 {len(df_04)} 条记录")

# 建立作者-文章映射，记录每个作者参与的文章
author_articles = defaultdict(set)

for index, row in df_04.iterrows():
    if pd.notna(row['Diaspora_Author_Names']):
        authors = str(row['Diaspora_Author_Names']).split(';')
        authors = [author.strip() for author in authors if author.strip()]
        
        # 为每个作者添加这篇文章
        for author in authors:
            author_articles[author].add(index)  # 使用行索引作为文章标识

print(f"已提取 {len(author_articles)} 位作者的文章信息")

# 读取作者学科分类表，获取总文章数
subject_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\unique_authors_with_subject.csv'
df_subject = pd.read_csv(subject_file)

print(f"已读取 {len(df_subject)} 位作者的学科信息")

# 计算每个作者的合作率
print("\n计算每个作者的合作率...")
author_collaboration = []

for _, row in df_subject.iterrows():
    author = row['Author']
    total_papers = int(row['Total_Papers'])
    
    # 获取该作者的所有文章
    if author in author_articles:
        articles = author_articles[author]
        
        # 计算合作文章数
        collaboration_papers = 0
        for article_index in articles:
            # 检查这篇文章的作者数量
            if pd.notna(df_04.at[article_index, 'Diaspora_Author_Names']):
                article_authors = str(df_04.at[article_index, 'Diaspora_Author_Names']).split(';')
                article_authors = [a.strip() for a in article_authors if a.strip()]
                if len(article_authors) > 1:
                    collaboration_papers += 1
        
        # 计算合作率
        if total_papers > 0:
            collaboration_rate = round(collaboration_papers / total_papers, 4)
        else:
            collaboration_rate = 0.0
    else:
        collaboration_papers = 0
        collaboration_rate = 0.0
    
    author_collaboration.append({
        'Author': author,
        'Total_Papers': total_papers,
        'Collaboration_Papers': collaboration_papers,
        'Collaboration_Rate': collaboration_rate
    })

# 创建DataFrame
df_collaboration = pd.DataFrame(author_collaboration)

# 保存到文件
output_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\author_collaboration_analysis.csv'
df_collaboration.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"作者合作分析表已保存到: {output_file}")

# 区分高活跃度和低活跃度作者
print("\n区分高活跃度和低活跃度作者...")

# 高活跃度作者：发表论文数 >= 4
highly_productive = df_collaboration[df_collaboration['Total_Papers'] >= 4].copy()

# 低活跃度作者：发表论文数 < 4
low_productive = df_collaboration[df_collaboration['Total_Papers'] < 4].copy()

print(f"高活跃度作者: {len(highly_productive)} 位")
print(f"低活跃度作者: {len(low_productive)} 位")

# 计算两类作者的合作率统计
print("\n计算合作率统计:")

# 高活跃度作者统计
high_stats = {
    'Average_Collaboration_Rate': highly_productive['Collaboration_Rate'].mean(),
    'Median_Collaboration_Rate': highly_productive['Collaboration_Rate'].median(),
    'Max_Collaboration_Rate': highly_productive['Collaboration_Rate'].max(),
    'Min_Collaboration_Rate': highly_productive['Collaboration_Rate'].min()
}

# 低活跃度作者统计
low_stats = {
    'Average_Collaboration_Rate': low_productive['Collaboration_Rate'].mean(),
    'Median_Collaboration_Rate': low_productive['Collaboration_Rate'].median(),
    'Max_Collaboration_Rate': low_productive['Collaboration_Rate'].max(),
    'Min_Collaboration_Rate': low_productive['Collaboration_Rate'].min()
}

print("\n高活跃度作者统计:")
for key, value in high_stats.items():
    print(f"  {key}: {round(value, 4)}")

print("\n低活跃度作者统计:")
for key, value in low_stats.items():
    print(f"  {key}: {round(value, 4)}")

# 保存对比结果到文件
print("\n保存对比结果到文件...")

comparison_data = {
    'Metric': ['Average Collaboration Rate', 'Median Collaboration Rate', 'Max Collaboration Rate', 'Min Collaboration Rate'],
    'Highly Productive Authors': [round(high_stats['Average_Collaboration_Rate'], 4),
                                  round(high_stats['Median_Collaboration_Rate'], 4),
                                  round(high_stats['Max_Collaboration_Rate'], 4),
                                  round(high_stats['Min_Collaboration_Rate'], 4)],
    'Low Productive Authors': [round(low_stats['Average_Collaboration_Rate'], 4),
                               round(low_stats['Median_Collaboration_Rate'], 4),
                               round(low_stats['Max_Collaboration_Rate'], 4),
                               round(low_stats['Min_Collaboration_Rate'], 4)]
}

df_comparison = pd.DataFrame(comparison_data)

comparison_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\collaboration_comparison.csv'
df_comparison.to_csv(comparison_file, index=False, encoding='utf-8-sig')
print(f"对比结果已保存到: {comparison_file}")

print("\n分析完成！")
