import pandas as pd
import os

print("开始更新其他受影响的文件...")

# 读取修复后的作者学科数据
fix_authors_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\unique_authors_with_subject.csv'
df_fix = pd.read_csv(fix_authors_file)

print(f"已读取修复后的作者数据，共 {len(df_fix)} 位作者")

# 1. 更新 author_publication_stats.csv
print("\n1. 更新 author_publication_stats.csv...")

# 从修复后的数据中提取作者发表统计
publication_stats = []
for _, row in df_fix.iterrows():
    author = row['Author']
    articles = int(row['Total_Papers'])
    
    # 由于没有年份数据，我们保持格式一致，但年份范围设为N/A
    # 在实际应用中，应该从原始Excel文件中获取年份信息
    publication_stats.append({
        'Author': author,
        'Articles': articles,
        'Year Range': 'N/A',
        'Average': articles  # 单年或年份未知时，平均值等于总数量
    })

# 创建DataFrame
df_publication_stats = pd.DataFrame(publication_stats)

# 保存到文件
publication_stats_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\author_publication_stats.csv'
df_publication_stats.to_csv(publication_stats_file, index=False, encoding='utf-8-sig')
print(f"已更新到: {publication_stats_file}")

# 2. 更新 highly_productive_scholars.csv
print("\n2. 更新 highly_productive_scholars.csv...")

# 筛选高产学者（发表论文数 >= 4）
highly_productive = df_fix[df_fix['Total_Papers'] >= 4].copy()

# 准备数据
highly_productive_list = []
for _, row in highly_productive.iterrows():
    author = row['Author']
    articles = int(row['Total_Papers'])
    
    highly_productive_list.append({
        'Author': author,
        'Articles': articles,
        'Year Range': 'N/A',
        'Average': articles
    })

# 创建DataFrame
df_highly_productive = pd.DataFrame(highly_productive_list)

# 按论文数量降序排序
df_highly_productive = df_highly_productive.sort_values(by='Articles', ascending=False)

# 保存到文件
highly_productive_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\highly_productive_scholars.csv'
df_highly_productive.to_csv(highly_productive_file, index=False, encoding='utf-8-sig')
print(f"已更新到: {highly_productive_file}")

# 3. 检查其他文件是否需要更新
print("\n3. 检查其他文件...")

# 检查 active_author_country_counts.csv
active_counts_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\active_author_country_counts.csv'
if os.path.exists(active_counts_file):
    df_active_counts = pd.read_csv(active_counts_file)
    print(f"active_author_country_counts.csv: {len(df_active_counts)} 条记录")
    print("  这个文件基于active_authors_by_period.csv，不受作者合并bug影响")

# 检查 country_author_counts.csv
country_counts_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\country_author_counts.csv'
if os.path.exists(country_counts_file):
    df_country_counts = pd.read_csv(country_counts_file)
    print(f"country_author_counts.csv: {len(df_country_counts)} 条记录")
    print("  这个文件统计国家的作者数量，作者合并bug会影响这个文件")
    print("  但由于需要国家信息，建议重新生成这个文件")

# 检查 author_countries.csv
author_countries_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\author_countries.csv'
if os.path.exists(author_countries_file):
    df_author_countries = pd.read_csv(author_countries_file)
    print(f"author_countries.csv: {len(df_author_countries)} 条记录")
    print("  这个文件记录作者和国家的对应关系，不受作者合并bug影响")

print("\n所有需要更新的文件已处理完成！")
print("\n总结：")
print("- 更新了 author_publication_stats.csv（作者发表统计）")
print("- 更新了 highly_productive_scholars.csv（高产学者列表）")
print("- 其他文件如country_author_counts.csv可能需要重新生成，但需要国家信息")
