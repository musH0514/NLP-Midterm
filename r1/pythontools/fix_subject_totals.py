import pandas as pd
import os

# 读取数据文件
data_dir = r'f:\projects\nlp\NLP-Midterm\r1\csv'
unique_authors_file = os.path.join(data_dir, 'unique_authors_with_subject.csv')

# 读取unique_authors_with_subject.csv
df = pd.read_csv(unique_authors_file)

# 重新计算学科总数
print("重新计算学科总数...")

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
subject_total_file = os.path.join(data_dir, 'subject_category_totals.csv')
subject_total_df.to_csv(subject_total_file, index=False, encoding='utf-8-sig')

print(f"修复后的学科总数表已保存到: {subject_total_file}")
print("\n修复后的学科总数表:")
print(subject_total_df)
