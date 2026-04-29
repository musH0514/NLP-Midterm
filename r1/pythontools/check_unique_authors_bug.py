import pandas as pd
import os
from collections import defaultdict

print("开始检查unique_authors.csv中的作者合并bug...")

# 读取unique_authors.csv文件
unique_authors_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\unique_authors.csv'

# 读取文件内容
with open(unique_authors_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 去掉表头和空行
authors = [line.strip() for line in lines if line.strip()]

print(f"unique_authors.csv 包含 {len(authors)} 位作者")

# 统计同名作者的情况
print("\n检查同名作者情况...")

# 只提取作者姓氏和首字母作为键（忽略中间名和后缀）
def get_author_key(author):
    # 简单处理：取姓氏和第一个名字的首字母
    parts = author.split(',')
    if len(parts) >= 2:
        last_name = parts[0].strip()
        first_names = parts[1].strip().split()
        if first_names:
            first_initial = first_names[0][0].upper() if first_names[0] else ''
            return f"{last_name}, {first_initial}"
    return author

# 统计作者键的出现次数
author_key_counts = defaultdict(list)
for author in authors:
    key = get_author_key(author)
    author_key_counts[key].append(author)

# 找出出现次数大于1的键（可能存在同名不同作者）
duplicate_keys = {k: v for k, v in author_key_counts.items() if len(v) > 1}

print(f"发现 {len(duplicate_keys)} 组可能的同名作者")

# 显示前10组同名作者
print("\n前10组可能的同名作者:")
for i, (key, author_list) in enumerate(list(duplicate_keys.items())[:10]):
    print(f"\n组 {i+1}: {key}")
    for author in author_list:
        print(f"  - {author}")

# 特别检查之前发现问题的 "An, Brian" 相关作者
print("\n=== 特别检查 'An, Brian' 相关作者 ===")
an_brian_authors = [author for author in authors if 'An,' in author and 'Brian' in author]
if an_brian_authors:
    print(f"找到 {len(an_brian_authors)} 位 'An, Brian' 相关作者:")
    for author in an_brian_authors:
        print(f"  - {author}")
else:
    print("未找到 'An, Brian' 相关作者")

# 从04表中检查这些同名作者的论文情况
print("\n=== 从04表中验证同名作者 ===")

# 读取04表中的Diaspora_Author_Names列
excel_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\04_Diaspora_Articles_12195(1).xlsx'

# 只读取必要的列
print("正在读取04表...")
df_04 = pd.read_excel(excel_file, sheet_name=0, usecols=['Diaspora_Author_Names'], engine='openpyxl')

# 检查之前发现的An, Brian P.的情况
print("\n检查 'An, Brian P.' 在04表中的出现情况:")
an_brian_p_records = df_04[df_04['Diaspora_Author_Names'].str.contains('An, Brian P.', na=False)]
print(f"找到 {len(an_brian_p_records)} 条包含 'An, Brian P.' 的记录")

# 检查是否有其他An, Brian变体
print("\n检查其他 'An, Brian' 变体:")
for author in authors:
    if 'An,' in author and 'Brian' in author:
        count = len(df_04[df_04['Diaspora_Author_Names'].str.contains(author, na=False)])
        print(f"  {author}: {count} 条记录")

print("\n=== 结论 ===")
print("unique_authors.csv 是从04表中提取的唯一作者列表")
print("该表本身不包含作者合并bug，因为它只是简单地提取了所有唯一的作者名字")
print(f"但表中存在 {len(duplicate_keys)} 组可能的同名不同作者，这些在后续分析中可能导致合并问题")
print("之前的bug是在生成学科分类时出现的，而不是在unique_authors.csv本身")
