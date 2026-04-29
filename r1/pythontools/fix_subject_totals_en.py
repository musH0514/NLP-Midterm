import pandas as pd
import os

# 读取学科总数表
totals_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\subject_category_totals.csv'
print(f"读取文件: {totals_file}")
df_totals = pd.read_csv(totals_file, encoding='utf-8-sig')

# 查看当前数据
print(f"\n当前数据:")
print(df_totals)

# 定义中文学科名称到英文的映射
subject_mapping = {
    '人文社科类': 'Humanities & Social Sciences',
    '经管类': 'Economics & Management',
    '理工类': 'Science & Technology',
    '医农类': 'Medicine & Agriculture',
    '其他': 'Others',
    '无论文': 'No Papers'
}

# 将学科名称从中文转换为英文
print(f"\n将学科名称从中文转换为英文...")
df_totals['Subject_Category'] = df_totals['Subject_Category'].map(subject_mapping)

# 将数值转换为整数类型
print(f"\n将数值转换为整数类型...")
integer_columns = ['Author_Count', 'Total_Papers']
df_totals[integer_columns] = df_totals[integer_columns].astype(int)

# 保存修复后的文件
print(f"\n保存修复后的文件...")
df_totals.to_csv(totals_file, index=False, encoding='utf-8-sig')

print(f"\n修复后的数据:")
print(df_totals)

print(f"\n修复完成！")
