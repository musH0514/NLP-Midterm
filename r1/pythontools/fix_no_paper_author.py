import pandas as pd
import os
from collections import defaultdict
import re

# 定义学科分类函数（从原脚本复制）
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

# 定义学科关键词映射（从原脚本复制）
subject_keywords = {
    '人文社科类': ['history', 'philosophy', 'literature', 'sociology', 'anthropology', 'psychology', 'education', 'law', 'politics', 'religion', 'art', 'culture', 'language', 'communication', 'media', 'ethics', 'archeology', 'humanities', 'social science', '社会', '人文', '历史', '哲学', '文学', '社会学', '人类学', '心理学', '教育', '法律', '政治', '宗教', '艺术', '文化', '语言', '传播', '媒介', '伦理', '考古'],
    '经管类': ['economics', 'management', 'business', 'finance', 'marketing', 'accounting', 'trade', 'commerce', 'investment', 'industry', 'economy', '管理', '经济', '商业', '金融', '市场', '会计', '贸易', '投资', '产业'],
    '理工类': ['science', 'technology', 'engineering', 'math', 'physics', 'chemistry', 'biology', 'computer', 'software', 'hardware', 'electronics', 'mechanics', 'materials', 'energy', 'environment', '数学', '物理', '化学', '生物', '计算机', '软件', '硬件', '电子', '机械', '材料', '能源', '环境', '科学', '技术', '工程'],
    '医农类': ['medicine', 'medical', 'health', 'disease', 'pharmacy', 'nursing', 'biomedical', 'agriculture', 'agricultural', 'farm', 'crop', 'plant', 'animal', '兽医', '农业', '医学', '健康', '疾病', '药学', '护理', '生物医学', '农场', '作物', '植物', '动物']
}

# 定义WoS分类映射（从原脚本复制）
wos_category_mapping = {
    '人文社科类': ['HISTORY', 'PHILOSOPHY', 'LITERATURE', 'SOCIOLOGY', 'ANTHROPOLOGY', 'PSYCHOLOGY', 'EDUCATION', 'LAW', 'POLITICAL SCIENCE', 'RELIGION', 'ART', 'CULTURE', 'LANGUAGE', 'COMMUNICATION', 'MEDIA', 'ETHICS', 'ARCHAEOLOGY', 'HUMANITIES', 'SOCIAL SCIENCES'],
    '经管类': ['ECONOMICS', 'MANAGEMENT', 'BUSINESS', 'FINANCE', 'MARKETING', 'ACCOUNTING', 'TRADE', 'COMMERCE', 'INDUSTRIAL RELATIONS', 'BUSINESS FINANCE & INVESTMENT'],
    '理工类': ['SCIENCE', 'TECHNOLOGY', 'ENGINEERING', 'MATHEMATICS', 'PHYSICS', 'CHEMISTRY', 'BIOLOGY', 'COMPUTER SCIENCE', 'ELECTRONICS', 'MECHANICS', 'MATERIALS SCIENCE', 'ENERGY & FUELS', 'ENVIRONMENTAL SCIENCES', 'EARTH SCIENCES', 'ASTRONOMY', 'STATISTICS'],
    '医农类': ['MEDICINE', 'HEALTH', 'DISEASE', 'PHARMACY', 'NURSING', 'BIOMEDICAL RESEARCH', 'AGRICULTURE', 'AGRONOMY', 'CROP SCIENCE', 'PLANT SCIENCES', 'ANIMAL SCIENCES', 'VETERINARY SCIENCE', 'FOOD SCIENCE', 'NUTRITION']
}

# 定义要查找的作者
target_author = 'Ai, Angela'
print(f"处理作者: {target_author}")

# 1. 首先检查unique_authors_with_subject.csv中该作者的情况
unique_authors_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\unique_authors_with_subject.csv'
print(f"\n读取unique_authors_with_subject.csv文件...")
df_authors = pd.read_csv(unique_authors_file)
ai_author = df_authors[df_authors['Author'] == target_author]
print(f"当前分类结果:")
print(ai_author)

# 2. 尝试使用openpyxl逐行读取04表，找到包含该作者的行
excel_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\04_Diaspora_Articles_12195(1).xlsx'
import openpyxl
print(f"\n使用openpyxl读取04表...")
workbook = openpyxl.load_workbook(excel_file, read_only=True)
sheet = workbook.active

# 获取表头
headers = []
for cell in sheet[1]:
    headers.append(cell.value)

# 找到所需列的索引
column_indices = {}
columns_to_read = ['Diaspora_Author_Names', 'Author Keywords', 'Abstract', 'Article Title', 'WoS Categories']
for col in columns_to_read:
    if col in headers:
        column_indices[col] = headers.index(col)
    else:
        print(f"警告: 列 {col} 不存在")

print(f"\n搜索包含 {target_author} 的行...")

# 逐行搜索
for row_idx, row in enumerate(sheet.iter_rows(min_row=2), start=2):
    # 检查是否有海外华人学者
    if 'Diaspora_Author_Names' in column_indices:
        author_col_idx = column_indices['Diaspora_Author_Names']
        if author_col_idx < len(row) and row[author_col_idx].value:
            author_names = str(row[author_col_idx].value)
            
            # 检查作者是否在该行
            if target_author in author_names:
                print(f"\n找到作者 {target_author} 在第 {row_idx} 行")
                
                # 构建行数据字典
                row_data = {}
                for col_name, col_idx in column_indices.items():
                    if col_idx < len(row):
                        row_data[col_name] = row[col_idx].value
                    else:
                        row_data[col_name] = None
                
                # 打印行数据
                for key, value in row_data.items():
                    print(f"{key}: {value}")
                
                # 尝试分类这篇论文
                print(f"\n尝试分类这篇论文...")
                try:
                    subject = classify_paper(row_data)
                    print(f"论文分类结果: {subject}")
                except Exception as e:
                    print(f"分类失败: {e}")
                
                # 尝试分割作者名称
                print(f"\n尝试分割作者名称...")
                authors = [author.strip() for author in author_names.split(';')]
                print(f"分割后的作者列表: {authors}")
                print(f"是否包含 {target_author}: {target_author in authors}")
                
                # 检查作者名称的精确匹配
                print(f"\n检查作者名称的精确匹配...")
                for author in authors:
                    if author == target_author:
                        print(f"找到精确匹配: {author}")
                    elif target_author in author:
                        print(f"找到包含匹配: {author}")
                
                # 提前结束循环
                break

workbook.close()
