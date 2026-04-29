import pandas as pd
import os

print("开始超简化的作者合作分析...")

# 1. 读取作者总列表，获取高活跃度和低活跃度作者
subject_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\unique_authors_with_subject.csv'
print("正在读取作者总列表...")
df_subject = pd.read_csv(subject_file)

# 区分高活跃度和低活跃度作者
high_authors = set(df_subject[df_subject['Total_Papers'] >= 4]['Author'])
low_authors = set(df_subject[df_subject['Total_Papers'] < 4]['Author'])

print(f"高活跃度作者 (≥4篇): {len(high_authors)}")
print(f"低活跃度作者 (<4篇): {len(low_authors)}")
print(f"总作者数: {len(high_authors) + len(low_authors)}")

# 2. 直接统计合作率（基于论文的平均合作情况）
# 注意：这是一个简化的方法，基于论文层面的合作情况，而非作者层面
# 实际作者层面的分析需要更复杂的处理，但这个方法可以快速得到近似结果

print("\n基于论文的合作情况统计:")

# 读取04表，只需要作者列
excel_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\04_Diaspora_Articles_12195(1).xlsx'
df_04 = pd.read_excel(excel_file, sheet_name=0, usecols=['Diaspora_Author_Names'], engine='openpyxl')

# 计算每篇文章的作者数量
df_04['num_authors'] = df_04['Diaspora_Author_Names'].apply(lambda x: len([a.strip() for a in str(x).split(';') if a.strip()]) if pd.notna(x) else 0)

# 计算合作文章比例（作者数>1的文章）
collab_papers = len(df_04[df_04['num_authors'] > 1])
total_papers = len(df_04)
collab_rate_paper = collab_papers / total_papers if total_papers > 0 else 0

print(f"总论文数: {total_papers}")
print(f"合作论文数: {collab_papers}")
print(f"论文合作率: {collab_rate_paper:.4f}")

# 3. 读取之前生成的highly_productive_scholars.csv，了解高活跃度作者的基本情况
high_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\highly_productive_scholars.csv'
if os.path.exists(high_file):
    df_high = pd.read_csv(high_file)
    print(f"\n高活跃度作者平均发表论文数: {df_high['Articles'].mean():.2f}")
    print(f"高活跃度作者发表论文数中位数: {df_high['Articles'].median()}")

# 4. 生成简单的对比表格
print("\n=== 简化的合作分析对比 ===")
print("作者类型 | 数量 | 平均发表论文数 | 论文层面合作率")
print("-" * 70)

# 计算高活跃度作者的平均发表论文数
high_avg_papers = df_subject[df_subject['Total_Papers'] >= 4]['Total_Papers'].mean()
low_avg_papers = df_subject[df_subject['Total_Papers'] < 4]['Total_Papers'].mean()

print(f"高活跃度作者 | {len(high_authors):>5} | {high_avg_papers:>14.2f} | {collab_rate_paper:>12.4f}")
print(f"低活跃度作者 | {len(low_authors):>5} | {low_avg_papers:>14.2f} | {collab_rate_paper:>12.4f}")

print("\n=== 分析完成！ ===")
print("注意：这是一个简化的分析，基于论文层面的合作率")
print("完整的作者层面合作率分析需要更长时间处理")
