import pandas as pd
import os

# 读取Excel文件的前1000行进行测试
excel_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\04_Diaspora_Articles_12195(1).xlsx'

try:
    print(f"读取Excel文件的前1000行...")
    df = pd.read_excel(excel_file, sheet_name=0, nrows=1000, engine='openpyxl')
    
    print(f"读取完成，共 {len(df)} 行数据")
    
    # 检查是否有包含"An, Brian P."的记录
    author_name = "An, Brian P."
    author_records = df[df['Diaspora_Author_Names'].str.contains(author_name, na=False)]
    
    print(f"\n在前1000行中找到 {len(author_records)} 条包含 '{author_name}' 的记录")
    
    if not author_records.empty:
        print(f"\n记录详情:")
        for index, row in author_records.iterrows():
            print(f"行号: {index+2} (Excel行号)")
            print(f"文章标题: {row['Article Title']}")
            print(f"WoS分类: {row['WoS Categories']}")
            print(f"发表年份: {row['Publication Year']}")
            print(f"Diaspora作者: {row['Diaspora_Author_Names']}")
            print("-" * 50)
    else:
        print(f"\n在前1000行中未找到 '{author_name}' 的记录")
        
    # 检查是否有Researcher Ids或ORCIDs列
    if 'Researcher Ids' in df.columns:
        print(f"\nResearcher Ids列存在")
    if 'ORCIDs' in df.columns:
        print(f"ORCIDs列存在")
    
    # 检查unique_authors_with_subject.csv中的记录
    subject_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\unique_authors_with_subject.csv'
    df_subject = pd.read_csv(subject_file)
    
    print(f"\n从unique_authors_with_subject.csv中读取的作者信息:")
    author_subject = df_subject[df_subject['Author'] == author_name]
    if not author_subject.empty:
        print(author_subject)
    
    
    # 检查学科分布
    if not author_records.empty:
        print(f"\n学科分布:")
        if 'WoS Categories' in df.columns:
            # 合并所有WoS分类
            all_categories = []
            for cats in author_records['WoS Categories'].dropna():
                all_categories.extend(str(cats).split('; '))
            
            # 统计出现次数
            from collections import Counter
            cat_counter = Counter(all_categories)
            
            for cat, count in cat_counter.items():
                if cat:
                    print(f"{cat}: {count}")
    
    print(f"\n结论:")
    print(f"'{author_name}' 在04表中至少有 {len(author_records)} 篇论文（仅检查前1000行）")
    print(f"从unique_authors_with_subject.csv可以看到，该作者涉及多个学科领域")
    print(f"这可能是因为：")
    print(f"1. 同一个作者发表了跨领域的论文")
    print(f"2. 存在多个同名不同作者被合并到一起")
    print(f"3. 学科分类标准可能不够精确")
    

except Exception as e:
    print(f"处理过程中出错: {e}")
    import traceback
    traceback.print_exc()
