import pandas as pd
import os

# 读取CSV文件，处理UTF-8 BOM问题
csv_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\unique_authors_with_subject.csv'
print(f"读取文件: {csv_file}")

# 使用utf-8-sig编码读取，自动处理BOM
df = pd.read_csv(csv_file, encoding='utf-8-sig')

# 查看前几行数据
print(f"\n原始数据前几行:")
print(df.head())

# 定义中文学科名称到英文的映射
subject_mapping = {
    '人文社科类': 'Humanities & Social Sciences',
    '经管类': 'Economics & Management',
    '理工类': 'Science & Technology',
    '医农类': 'Medicine & Agriculture',
    '其他': 'Others'
}

# 将学科名称从中文转换为英文
print(f"\n将学科名称从中文转换为英文...")
df['Main_Subject'] = df['Main_Subject'].map(subject_mapping)

# 也需要更新列名中的中文
print(f"\n更新列名...")
column_mapping = {
    'Main_Subject': 'Main_Subject',  # 保持不变
    'Humanities_Social_Science': 'Humanities_Social_Science',  # 已经是英文
    'Economics_Management': 'Economics_Management',  # 已经是英文
    'Science_Technology': 'Science_Technology',  # 已经是英文
    'Medicine_Agriculture': 'Medicine_Agriculture',  # 已经是英文
    'Other': 'Other',  # 已经是英文
    'Total_Papers': 'Total_Papers'  # 已经是英文
}
df = df.rename(columns=column_mapping)

# 将数值转换为整数类型
print(f"\n将数值转换为整数类型...")
integer_columns = ['Humanities_Social_Science', 'Economics_Management', 'Science_Technology', 'Medicine_Agriculture', 'Other', 'Total_Papers']
df[integer_columns] = df[integer_columns].astype(int)

# 保存修复后的文件
print(f"\n保存修复后的文件...")
df.to_csv(csv_file, index=False, encoding='utf-8-sig')

print(f"\n修复后的数据前几行:")
print(df.head())

print(f"\n修复完成！")
print(f"\n数值含义解释:")
print("1. Humanities_Social_Science: 人文社科类论文数量")
print("2. Economics_Management: 经管类论文数量")
print("3. Science_Technology: 理工类论文数量")
print("4. Medicine_Agriculture: 医农类论文数量")
print("5. Other: 其他学科论文数量")
print("6. Total_Papers: 总论文数量")
