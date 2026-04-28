import pandas as pd
import numpy as np
import os
import time

# 读取Excel文件，使用绝对路径
excel_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\04_Diaspora_Articles_12195(1).xlsx'

print(f"Excel文件路径: {excel_file}")
print(f"文件是否存在: {os.path.exists(excel_file)}")

try:
    print("开始读取Excel文件...")
    start_time = time.time()
    
    # 只读取前100行数据
    df = pd.read_excel(excel_file, sheet_name=0, nrows=100)
    
    end_time = time.time()
    print(f"Excel文件读取完成，耗时: {end_time - start_time:.2f}秒")
    
    # 查看基本信息
    print(f"数据行数: {len(df)}")
    print(f"数据列数: {len(df.columns)}")
    
    # 查看所有列名
    print(f"\n所有列名:")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")
    
    # 查看Diaspora_Author_Names列的前10个值
    print(f"\nDiaspora_Author_Names列的前10个值:")
    if 'Diaspora_Author_Names' in df.columns:
        print(df['Diaspora_Author_Names'].head(10))
    else:
        print("Diaspora_Author_Names列不存在")
        
    # 检查是否有包含"作者"或"author"的列
    print(f"\n查找包含'Author'或'作者'的列:")
    for col in df.columns:
        col_lower = str(col).lower()
        if 'author' in col_lower:
            print(f"列名: {col}")
            # 查看该列的前10个非空值
            non_null_values = df[col].dropna().head(10)
            print(f"示例值: {list(non_null_values)}")
            print()
            
except Exception as e:
    print(f"读取Excel文件时出错: {e}")
    import traceback
    traceback.print_exc()
