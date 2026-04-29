import pandas as pd
import os

print("开始快速分析作者合作情况...")

# 1. 读取04表，获取每篇文章的作者列表
excel_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\04_Diaspora_Articles_12195(1).xlsx'
print("正在读取04表...")

# 只读取Diaspora_Author_Names列
df_04 = pd.read_excel(excel_file, sheet_name=0, usecols=['Diaspora_Author_Names'], engine='openpyxl')
print(f"04表包含 {len(df_04)} 条记录")

# 2. 读取作者总列表（包含总论文数）
subject_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\unique_authors_with_subject.csv'
print("正在读取作者总列表...")
df_subject = pd.read_csv(subject_file)
print(f"作者总列表包含 {len(df_subject)} 位作者")

# 3. 创建作者字典，存储合作文章数
print("正在计算合作文章数...")
author_collab = {}

for idx, row in df_04.iterrows():
    if idx % 1000 == 0:  # 每处理1000条记录显示一次进度
        print(f"处理了 {idx} 条记录...")
        
    if pd.notna(row['Diaspora_Author_Names']):
        authors = [author.strip() for author in str(row['Diaspora_Author_Names']).split(';') if author.strip()]
        num_authors = len(authors)
        
        if num_authors > 1:  # 这是一篇合作文章
            for author in authors:
                if author not in author_collab:
                    author_collab[author] = 0
                author_collab[author] += 1

print(f"已计算 {len(author_collab)} 位作者的合作文章数")

# 4. 生成作者合作分析表
print("正在生成作者合作分析表...")

# 创建空列表存储结果
results = []

for _, row in df_subject.iterrows():
    author = row['Author']
    total_papers = int(row['Total_Papers'])
    
    # 获取该作者的合作文章数
    collab_papers = author_collab.get(author, 0)
    
    # 计算合作率
    if total_papers > 0:
        collab_rate = round(collab_papers / total_papers, 4)
    else:
        collab_rate = 0.0
    
    results.append({
        'Author': author,
        'Total_Papers': total_papers,
        'Collaboration_Papers': collab_papers,
        'Collaboration_Rate': collab_rate
    })

# 创建DataFrame
df_collaboration = pd.DataFrame(results)

# 5. 保存作者合作分析表
output_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\author_collaboration_analysis.csv'
df_collaboration.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"作者合作分析表已保存到: {output_file}")

# 6. 区分高活跃度和低活跃度作者
highly_productive = df_collaboration[df_collaboration['Total_Papers'] >= 4]
low_productive = df_collaboration[df_collaboration['Total_Papers'] < 4]

print(f"\n高活跃度作者 (≥4篇论文): {len(highly_productive)} 位")
print(f"低活跃度作者 (<4篇论文): {len(low_productive)} 位")

# 7. 计算并比较两类作者的合作率
print("\n=== 合作率比较 ===")

# 高活跃度作者统计
high_avg = highly_productive['Collaboration_Rate'].mean()
high_med = highly_productive['Collaboration_Rate'].median()
high_max = highly_productive['Collaboration_Rate'].max()
high_min = highly_productive['Collaboration_Rate'].min()

# 低活跃度作者统计
low_avg = low_productive['Collaboration_Rate'].mean()
low_med = low_productive['Collaboration_Rate'].median()
low_max = low_productive['Collaboration_Rate'].max()
low_min = low_productive['Collaboration_Rate'].min()

# 打印比较结果
print("\n统计指标 | 高活跃度作者 | 低活跃度作者")
print("-" * 50)
print(f"平均合作率 | {high_avg:.4f} | {low_avg:.4f}")
print(f"中位数合作率 | {high_med:.4f} | {low_med:.4f}")
print(f"最高合作率 | {high_max:.4f} | {low_max:.4f}")
print(f"最低合作率 | {high_min:.4f} | {low_min:.4f}")

# 8. 保存对比结果
comparison_data = {
    'Metric': ['Average Collaboration Rate', 'Median Collaboration Rate', 'Max Collaboration Rate', 'Min Collaboration Rate', 'Number of Authors'],
    'Highly Productive Authors': [round(high_avg, 4), round(high_med, 4), round(high_max, 4), round(high_min, 4), len(highly_productive)],
    'Low Productive Authors': [round(low_avg, 4), round(low_med, 4), round(low_max, 4), round(low_min, 4), len(low_productive)]
}

df_comparison = pd.DataFrame(comparison_data)
comparison_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\collaboration_comparison.csv'
df_comparison.to_csv(comparison_file, index=False, encoding='utf-8-sig')
print(f"\n对比结果已保存到: {comparison_file}")

# 9. 显示前10位作者的合作情况
print("\n=== 前10位作者的合作情况 ===")
print(df_collaboration.head(10))

print("\n=== 分析完成！ ===")
print("已生成以下文件:")
print(f"1. {output_file} - 所有作者的合作分析表")
print(f"2. {comparison_file} - 高活跃度与低活跃度作者的对比")
