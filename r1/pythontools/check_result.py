import pandas as pd
import os

# 读取生成的文件
data_dir = r'f:\projects\nlp\NLP-Midterm\r1\csv'

# 检查unique_authors_with_subject.csv
unique_authors_file = os.path.join(data_dir, 'unique_authors_with_subject.csv')
if os.path.exists(unique_authors_file):
    print(f"\n读取unique_authors_with_subject.csv文件...")
    df = pd.read_csv(unique_authors_file)
    print(f"文件包含 {len(df)} 行数据")
    print(f"\n学科分布:")
    print(df['Main_Subject'].value_counts())
    
    # 查看部分数据
    print(f"\n前10行数据:")
    print(df.head(10))
    
    # 查看有论文的作者
    has_papers = df[df['Main_Subject'] != '无论文']
    print(f"\n有论文的作者数量: {len(has_papers)}")
    print(f"无论文的作者数量: {len(df) - len(has_papers)}")
else:
    print("unique_authors_with_subject.csv文件不存在")

# 检查subject_category_totals.csv
subject_totals_file = os.path.join(data_dir, 'subject_category_totals.csv')
if os.path.exists(subject_totals_file):
    print(f"\n读取subject_category_totals.csv文件...")
    df_totals = pd.read_csv(subject_totals_file)
    print(df_totals)
else:
    print("subject_category_totals.csv文件不存在")
