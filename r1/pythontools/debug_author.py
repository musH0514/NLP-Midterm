import pandas as pd
import os
from collections import defaultdict

# 读取04表的部分数据来检查
print("开始读取04表的部分数据...")

excel_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\04_Diaspora_Articles_12195(1).xlsx'

# 只读取需要的列
columns_to_read = [
    'Diaspora_Author_Names', 'Author Keywords', 'Abstract', 
    'Article Title', 'WoS Categories'
]

# 读取整个表
print("正在读取整个04表...")
df = pd.read_excel(excel_file, sheet_name=0, usecols=columns_to_read)

print(f"表共有 {len(df)} 行数据")

# 查找包含Ai, Angela的行
print("\n查找包含Ai, Angela的行...")
# 创建一个包含Ai, Angela的作者列表
df['Contains_Ai'] = df['Diaspora_Author_Names'].apply(
    lambda x: 'Ai, Angela' in str(x) if pd.notna(x) else False
)

# 筛选出包含Ai, Angela的行
ai_rows = df[df['Contains_Ai']]

if not ai_rows.empty:
    print(f"找到 {len(ai_rows)} 行包含Ai, Angela:")
    
    # 重置索引，以便获取原始行号
    ai_rows_reset = ai_rows.reset_index()
    
    for index, row in ai_rows_reset.iterrows():
        # 原始行号（Excel行号）
        excel_row = row['index'] + 2  # 因为Excel行号从2开始
        print(f"\nExcel行号: {excel_row}")
        print(f"Diaspora_Author_Names: {row['Diaspora_Author_Names']}")
        print(f"Article Title: {row['Article Title']}")
        print(f"WoS Categories: {row['WoS Categories']}")
        print(f"Author Keywords: {row['Author Keywords']}")
else:
    print("未找到包含Ai, Angela的行")

# 现在检查unique_authors_with_subject.csv
print("\n\n检查unique_authors_with_subject.csv文件...")
unique_authors_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\unique_authors_with_subject.csv'
df_authors = pd.read_csv(unique_authors_file)

# 查找Ai, Angela
ai_author = df_authors[df_authors['Author'] == 'Ai, Angela']

if not ai_author.empty:
    print(f"Ai, Angela在unique_authors_with_subject.csv中的信息:")
    print(ai_author)
else:
    print("在unique_authors_with_subject.csv中未找到Ai, Angela")
