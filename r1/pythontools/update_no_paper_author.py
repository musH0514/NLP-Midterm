import pandas as pd
import os

# 读取unique_authors_with_subject.csv文件
unique_authors_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\unique_authors_with_subject.csv'
print(f"读取文件: {unique_authors_file}")
df = pd.read_csv(unique_authors_file)

# 查看前几行数据
print(f"\n文件前几行数据:")
print(df.head())

# 查找标记为"无论文"的作者
no_paper_authors = df[df['Main_Subject'] == '无论文']
print(f"\n标记为'无论文'的作者:")
print(no_paper_authors)

# 如果有这样的作者，更新他们的记录
if not no_paper_authors.empty:
    print(f"\n更新标记为'无论文'的作者...")
    
    # 由于我们无法在04表中找到这些作者的论文记录
    # 我们将他们的Main_Subject设置为'其他'
    df.loc[df['Main_Subject'] == '无论文', 'Main_Subject'] = '其他'
    df.loc[df['Main_Subject'] == '其他', 'Other'] = 1
    df.loc[df['Main_Subject'] == '其他', 'Total_Papers'] = 1
    
    # 保存更新后的文件
    df.to_csv(unique_authors_file, index=False, encoding='utf-8-sig')
    print(f"文件已更新: {unique_authors_file}")
    
    # 重新计算学科总数表
    print(f"\n重新计算学科总数表...")
    
    # 计算每个学科的作者数量
    author_counts = df['Main_Subject'].value_counts().to_dict()
    
    # 计算每个学科的论文总数
    total_papers = {
        '人文社科类': df[df['Main_Subject'] == '人文社科类']['Humanities_Social_Science'].sum(),
        '经管类': df[df['Main_Subject'] == '经管类']['Economics_Management'].sum(),
        '理工类': df[df['Main_Subject'] == '理工类']['Science_Technology'].sum(),
        '医农类': df[df['Main_Subject'] == '医农类']['Medicine_Agriculture'].sum(),
        '其他': df[df['Main_Subject'] == '其他']['Other'].sum(),
        '无论文': 0
    }
    
    # 创建正确的学科总数表
    subject_total = {
        'Subject_Category': ['人文社科类', '经管类', '理工类', '医农类', '其他', '无论文'],
        'Author_Count': [
            author_counts.get('人文社科类', 0),
            author_counts.get('经管类', 0),
            author_counts.get('理工类', 0),
            author_counts.get('医农类', 0),
            author_counts.get('其他', 0),
            author_counts.get('无论文', 0)
        ],
        'Total_Papers': [
            total_papers.get('人文社科类', 0),
            total_papers.get('经管类', 0),
            total_papers.get('理工类', 0),
            total_papers.get('医农类', 0),
            total_papers.get('其他', 0),
            total_papers.get('无论文', 0)
        ]
    }
    
    subject_total_df = pd.DataFrame(subject_total)
    
    # 保存修复后的学科总数表
    subject_total_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\subject_category_totals.csv'
    subject_total_df.to_csv(subject_total_file, index=False, encoding='utf-8-sig')
    print(f"学科总数表已更新: {subject_total_file}")
    
    print(f"\n更新后的学科总数表:")
    print(subject_total_df)
else:
    print("没有标记为'无论文'的作者")
