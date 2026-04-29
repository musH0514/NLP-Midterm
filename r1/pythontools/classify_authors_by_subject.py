import pandas as pd
import numpy as np
import re
import os
import time
from collections import defaultdict

# 设置显示选项，以便查看完整的内容
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

# 定义学科分类关键词
subject_keywords = {
    '人文社科类': [
        'psychology', 'education', 'sociology', 'anthropology', 'history',
        'philosophy', 'linguistics', 'literature', 'art', 'culture',
        'communication', 'political science', 'law', 'religion', 'archeology',
        'ethics', 'gender', 'media', 'social', 'humanities'
    ],
    '经管类': [
        'business', 'economics', 'management', 'finance', 'accounting',
        'marketing', 'entrepreneurship', 'organizational', 'strategy',
        'industry', 'commerce', 'trade', 'investment', 'corporate', 'business'
    ],
    '理工类': [
        'computer science', 'engineering', 'physics', 'chemistry', 'mathematics',
        'biology', 'technology', 'information', 'data', 'algorithm',
        'software', 'hardware', 'programming', 'machine learning', 'artificial intelligence',
        'statistics', 'quantum', 'materials', 'electronics', 'mechanical',
        'civil', 'electrical', 'chemical engineering'
    ],
    '医农类': [
        'medicine', 'health', 'medical', 'nursing', 'pharmacy',
        'agriculture', 'veterinary', 'public health', 'biomedical',
        'clinical', 'disease', 'pharmaceutical', 'patient', 'treatment',
        'diagnosis', 'epidemiology', 'nutrition', 'agricultural', 'crop'
    ]
}

# 定义WoS类别映射
wos_category_mapping = {
    '人文社科类': [
        'EDUCATION, EDUCATIONAL RESEARCH', 'PSYCHOLOGY, EDUCATIONAL',
        'PSYCHOLOGY, DEVELOPMENTAL', 'SOCIOLOGY', 'ANTHROPOLOGY',
        'HISTORY', 'PHILOSOPHY', 'LINGUISTICS', 'LITERATURE', 'ART',
        'COMMUNICATION', 'POLITICAL SCIENCE', 'LAW', 'RELIGION',
        'SOCIAL SCIENCES, INTERDISCIPLINARY', 'HUMANITIES, MULTIDISCIPLINARY'
    ],
    '经管类': [
        'BUSINESS', 'ECONOMICS', 'MANAGEMENT', 'FINANCE', 'ACCOUNTING',
        'BUSINESS, FINANCE', 'BUSINESS, MANAGEMENT', 'ECONOMICS, BUSINESS',
        'BUSINESS, STRATEGY', 'INDUSTRIAL RELATIONS & LABOR'
    ],
    '理工类': [
        'COMPUTER SCIENCE', 'ENGINEERING', 'PHYSICS', 'CHEMISTRY',
        'MATHEMATICS', 'BIOLOGY', 'TECHNOLOGY', 'INFORMATION SCIENCE & LIBRARY SCIENCE',
        'COMPUTER SCIENCE, ARTIFICIAL INTELLIGENCE', 'COMPUTER SCIENCE, INFORMATION SYSTEMS',
        'ENGINEERING, ELECTRICAL & ELECTRONIC', 'ENGINEERING, MECHANICAL',
        'ENGINEERING, CIVIL', 'ENGINEERING, CHEMICAL', 'MATERIALS SCIENCE',
        'STATISTICS & PROBABILITY', 'QUANTUM SCIENCE & TECHNOLOGY'
    ],
    '医农类': [
        'MEDICINE', 'HEALTH SCIENCES', 'NURSING', 'PHARMACY', 'AGRICULTURE',
        'VETERINARY SCIENCES', 'PUBLIC, ENVIRONMENTAL & OCCUPATIONAL HEALTH',
        'BIOMEDICINE', 'CLINICAL MEDICINE', 'DISEASE', 'PHARMACEUTICAL SCIENCES',
        'AGRICULTURAL ECONOMICS & POLICY', 'AGRICULTURAL ENGINEERING',
        'AGRICULTURAL SOILS', 'CROP SCIENCES', 'FOOD SCIENCE & TECHNOLOGY'
    ]
}

# 定义学科分类函数
def classify_paper(row):
    """根据论文的关键词、摘要和WoS分类来判断论文的学科类别"""
    # 将所有文本转换为小写
    keywords = str(row['Author Keywords']).lower() if pd.notna(row['Author Keywords']) else ''
    abstract = str(row['Abstract']).lower() if pd.notna(row['Abstract']) else ''
    title = str(row['Article Title']).lower() if pd.notna(row['Article Title']) else ''
    wos_categories = str(row['WoS Categories']).upper() if pd.notna(row['WoS Categories']) else ''
    
    # 合并所有文本
    all_text = keywords + ' ' + abstract + ' ' + title
    
    # 统计每个学科的匹配次数
    subject_counts = {
        '人文社科类': 0,
        '经管类': 0,
        '理工类': 0,
        '医农类': 0
    }
    
    # 1. 先使用WoS分类（更准确）
    if wos_categories:
        for category in wos_categories.split('; '):
            for subject, wos_list in wos_category_mapping.items():
                if category in wos_list:
                    subject_counts[subject] += 1
    
    # 2. 如果WoS分类没有匹配到，使用关键词匹配
    if all(count == 0 for count in subject_counts.values()):
        for subject, keywords_list in subject_keywords.items():
            for keyword in keywords_list:
                # 使用正则表达式匹配整个单词
                if re.search(r'\b' + keyword + r'\b', all_text):
                    subject_counts[subject] += 1
    
    # 找出匹配次数最多的学科
    max_count = max(subject_counts.values())
    if max_count > 0:
        # 如果有多个学科匹配次数相同，返回第一个
        for subject, count in subject_counts.items():
            if count == max_count:
                return subject
    
    # 如果没有匹配到任何学科，返回'其他'
    return '其他'

# 主函数
def main():
    print("开始处理作者学科分类...")
    
    # 读取Excel文件
    excel_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\04_Diaspora_Articles_12195(1).xlsx'
    
    print(f"Excel文件路径: {excel_file}")
    print(f"文件是否存在: {os.path.exists(excel_file)}")
    print(f"文件大小: {os.path.getsize(excel_file) / (1024*1024):.2f} MB")
    
    if not os.path.exists(excel_file):
        print("Excel文件不存在，请检查路径")
        return
    
    try:
        # 检查所需列是否存在
        print("\n测试读取前10行数据，检查列名...")
        df_test = pd.read_excel(excel_file, sheet_name=0, nrows=10, engine='openpyxl')
        
        columns_to_read = [
            'Diaspora_Author_Names', 'Author Keywords', 'Abstract', 
            'Article Title', 'WoS Categories'
        ]
        
        print("\n检查所需列是否存在:")
        for col in columns_to_read:
            print(f"{col}: {'存在' if col in df_test.columns else '不存在'}")
        
        # 使用openpyxl直接读取数据，避免内存问题
        print("\n使用openpyxl直接读取Excel文件...")
        import openpyxl
        workbook = openpyxl.load_workbook(excel_file, read_only=True)
        sheet = workbook.active
        
        # 获取表头
        headers = []
        for cell in sheet[1]:
            headers.append(cell.value)
        
        # 找到所需列的索引
        column_indices = {}
        for col in columns_to_read:
            if col in headers:
                column_indices[col] = headers.index(col) + 1  # Excel索引从1开始
            else:
                print(f"警告: 列 {col} 不存在")
        
        print("\n开始处理数据...")
        start_time = time.time()
        
        # 统计每个作者在每个学科的论文数量
        author_subject_counts = defaultdict(lambda: defaultdict(int))
        processed_rows = 0
        
        # 逐行读取数据
        for row in sheet.iter_rows(min_row=2):  # 从第二行开始读取数据
            processed_rows += 1
            
            # 获取所需列的数据
            row_data = {}
            for col_name, col_idx in column_indices.items():
                if col_idx <= len(row):
                    row_data[col_name] = row[col_idx - 1].value  # Python索引从0开始
                else:
                    row_data[col_name] = None
            
            # 检查是否有海外华人学者
            if not pd.notna(row_data['Diaspora_Author_Names']):
                continue
            
            # 分类学科
            subject = classify_paper(row_data)
            
            # 统计作者学科
            authors = [author.strip() for author in str(row_data['Diaspora_Author_Names']).split(';')]
            for author in authors:
                if author:
                    author_subject_counts[author][subject] += 1
            
            # 每处理1000行输出一次进度
            if processed_rows % 1000 == 0:
                print(f"已处理 {processed_rows} 行数据")
        
        workbook.close()
        end_time = time.time()
        print(f"数据处理完成，共处理 {processed_rows} 行数据，耗时: {end_time - start_time:.2f}秒")
        print(f"作者学科论文数量统计完成，共 {len(author_subject_counts)} 位作者")
        
        # 为每个作者分配主要学科（发表论文最多的学科）
        print("\n开始为每个作者分配主要学科...")
        start_time = time.time()
        author_main_subjects = []
        for author, subject_counts in author_subject_counts.items():
            # 找出发表论文最多的学科
            max_count = max(subject_counts.values())
            main_subjects = [subject for subject, count in subject_counts.items() if count == max_count]
            
            # 如果有多个主要学科，返回第一个
            main_subject = main_subjects[0]
            
            author_main_subjects.append({
                'Author': author,
                'Main_Subject': main_subject,
                'Humanities_Social_Science': subject_counts.get('人文社科类', 0),
                'Economics_Management': subject_counts.get('经管类', 0),
                'Science_Technology': subject_counts.get('理工类', 0),
                'Medicine_Agriculture': subject_counts.get('医农类', 0),
                'Other': subject_counts.get('其他', 0),
                'Total_Papers': sum(subject_counts.values())
            })
        
        # 转换为DataFrame
        author_subject_df = pd.DataFrame(author_main_subjects)
        end_time = time.time()
        print(f"作者主要学科分配完成，共 {len(author_subject_df)} 位作者，耗时: {end_time - start_time:.2f}秒")
        
        # 查看部分结果
        print("\n部分作者学科分类结果:")
        print(author_subject_df.head())
        
        # 读取unique_authors表，直接使用文件操作避免逗号问题
        unique_authors_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\unique_authors.csv'
        if os.path.exists(unique_authors_file):
            print("\n开始读取unique_authors表...")
            # 直接使用文件操作读取每行
            authors = []
            with open(unique_authors_file, 'r', encoding='utf-8') as f:
                for line in f:
                    authors.append(line.strip())
            
            # 创建DataFrame
            unique_authors_df = pd.DataFrame({'Author': authors})
            print(f"unique_authors表读取完成，共 {len(unique_authors_df)} 位作者")
            
            # 检查是否有相同的作者
            common_authors = set(unique_authors_df['Author']) & set(author_subject_df['Author'])
            print(f"\n两个表共有 {len(common_authors)} 位相同的作者")
            
            # 合并两个表，为每个唯一作者添加主要学科
            print("\n开始合并两个表...")
            start_time = time.time()
            merged_df = pd.merge(unique_authors_df, author_subject_df, on='Author', how='left')
            end_time = time.time()
            print(f"表合并完成，耗时: {end_time - start_time:.2f}秒")
            
            # 处理没有论文的作者
            print("\n开始处理没有论文的作者...")
            merged_df = merged_df.fillna({
                'Main_Subject': '无论文',
                'Humanities_Social_Science': 0,
                'Economics_Management': 0,
                'Science_Technology': 0,
                'Medicine_Agriculture': 0,
                'Other': 0,
                'Total_Papers': 0
            })
            
            # 保存新表
            new_unique_authors_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\unique_authors_with_subject.csv'
            print(f"\n开始保存新表到: {new_unique_authors_file}")
            start_time = time.time()
            merged_df.to_csv(new_unique_authors_file, index=False, encoding='utf-8-sig')
            end_time = time.time()
            print(f"新表已保存到: {new_unique_authors_file}，耗时: {end_time - start_time:.2f}秒")
        
        # 生成学科总数表
        print("\n开始生成学科总数表...")
        # 计算有论文的作者的学科分布
        subject_author_count = author_subject_df['Main_Subject'].value_counts().to_dict()
        # 计算无论文的作者数量
        no_paper_count = len(unique_authors_df) - len(author_subject_df)
        
        subject_total = {
            'Subject_Category': ['人文社科类', '经管类', '理工类', '医农类', '无论文', '其他'],
            'Author_Count': [
                subject_author_count.get('人文社科类', 0),
                subject_author_count.get('经管类', 0),
                subject_author_count.get('理工类', 0),
                subject_author_count.get('医农类', 0),
                no_paper_count,
                subject_author_count.get('其他', 0)
            ],
            'Total_Papers': [
                author_subject_df['Humanities_Social_Science'].sum(),
                author_subject_df['Economics_Management'].sum(),
                author_subject_df['Science_Technology'].sum(),
                author_subject_df['Medicine_Agriculture'].sum(),
                0,
                author_subject_df['Other'].sum()
            ]
        }
        
        subject_total_df = pd.DataFrame(subject_total)
        
        # 保存学科总数表
        subject_total_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\subject_category_totals.csv'
        print(f"开始保存学科总数表到: {subject_total_file}")
        subject_total_df.to_csv(subject_total_file, index=False, encoding='utf-8-sig')
        print(f"学科总数表已保存到: {subject_total_file}")
        
        print("\n处理完成！")
        
    except Exception as e:
        print(f"处理过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
