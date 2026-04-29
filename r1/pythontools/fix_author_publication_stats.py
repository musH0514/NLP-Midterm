import pandas as pd
import os
from collections import defaultdict

print("开始修复author_publication_stats.csv的年份问题...")

# 读取原始04表，提取作者、论文标题和年份
print("正在读取04表...")
excel_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\04_Diaspora_Articles_12195(1).xlsx'

# 使用openpyxl读取特定列
df_04 = pd.read_excel(excel_file, sheet_name=0, usecols=['Diaspora_Author_Names', 'Article Title', 'Publication Year'], engine='openpyxl')

print(f"04表包含 {len(df_04)} 条记录")

# 建立作者-年份映射
print("正在提取作者的年份信息...")
author_years = defaultdict(list)

for _, row in df_04.iterrows():
    authors = str(row['Diaspora_Author_Names']).split(';') if pd.notna(row['Diaspora_Author_Names']) else []
    year = row['Publication Year']
    
    for author in authors:
        author = author.strip()
        if author and pd.notna(year):
            author_years[author].append(int(year))

print(f"已提取 {len(author_years)} 位作者的年份信息")

# 读取修复后的作者学科数据
fix_authors_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\unique_authors_with_subject.csv'
df_fix = pd.read_csv(fix_authors_file)

print(f"已读取修复后的作者数据，共 {len(df_fix)} 位作者")

# 更新 author_publication_stats.csv
print("\n1. 更新 author_publication_stats.csv...")

publication_stats = []
for _, row in df_fix.iterrows():
    author = row['Author']
    articles = int(row['Total_Papers'])
    
    # 获取该作者的所有年份
    years = author_years.get(author, [])
    
    if years:
        min_year = min(years)
        max_year = max(years)
        year_range = f"{min_year}-{max_year}"
        
        # 计算平均每年发表论文数
        if min_year == max_year:
            average = articles
        else:
            years_span = max_year - min_year + 1
            average = round(articles / years_span, 2)
    else:
        year_range = 'N/A'
        average = articles
    
    publication_stats.append({
        'Author': author,
        'Articles': articles,
        'Year Range': year_range,
        'Average': average
    })

# 创建DataFrame
df_publication_stats = pd.DataFrame(publication_stats)

# 保存到文件
publication_stats_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\author_publication_stats.csv'
df_publication_stats.to_csv(publication_stats_file, index=False, encoding='utf-8-sig')
print(f"已更新到: {publication_stats_file}")

# 更新 highly_productive_scholars.csv
print("\n2. 更新 highly_productive_scholars.csv...")

# 筛选高产学者（发表论文数 >= 4）
highly_productive = df_fix[df_fix['Total_Papers'] >= 4].copy()

highly_productive_list = []
for _, row in highly_productive.iterrows():
    author = row['Author']
    articles = int(row['Total_Papers'])
    
    # 获取该作者的所有年份
    years = author_years.get(author, [])
    
    if years:
        min_year = min(years)
        max_year = max(years)
        year_range = f"{min_year}-{max_year}"
        
        # 计算平均每年发表论文数
        if min_year == max_year:
            average = articles
        else:
            years_span = max_year - min_year + 1
            average = round(articles / years_span, 2)
    else:
        year_range = 'N/A'
        average = articles
    
    highly_productive_list.append({
        'Author': author,
        'Articles': articles,
        'Year Range': year_range,
        'Average': average
    })

# 创建DataFrame
df_highly_productive = pd.DataFrame(highly_productive_list)

# 按论文数量降序排序
df_highly_productive = df_highly_productive.sort_values(by='Articles', ascending=False)

# 保存到文件
highly_productive_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\highly_productive_scholars.csv'
df_highly_productive.to_csv(highly_productive_file, index=False, encoding='utf-8-sig')
print(f"已更新到: {highly_productive_file}")

# 验证修复结果
print("\n3. 验证修复结果...")

# 查看修复后的文件前10行
print("\nauthor_publication_stats.csv 前10行:")
df_updated = pd.read_csv(publication_stats_file)
print(df_updated.head(10))

# 统计有年份信息的作者比例
has_year_count = len(df_updated[df_updated['Year Range'] != 'N/A'])
total_count = len(df_updated)
year_coverage = round(has_year_count / total_count * 100, 2)
print(f"\n有年份信息的作者比例: {year_coverage}% ({has_year_count}/{total_count})")

print("\n年份问题修复完成！")
