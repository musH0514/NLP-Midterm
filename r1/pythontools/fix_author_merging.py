import pandas as pd
import openpyxl
import os
import re
from collections import defaultdict
import time

# 定义学科分类的关键词和WoS分类映射
subject_keywords = {
    '人文社科类': [
        'history', 'philosophy', 'sociology', 'anthropology', 'politics', 'political', 
        'literature', 'linguistics', 'psychology', 'education', 'art', 'arts', 
        'culture', 'cultural', 'religion', 'religious', 'law', 'legal', 
        'communication', 'media', 'archeology', 'archaeology', 'history', 'historical',
        '伦理', '道德', '哲学', '历史', '社会', '文化', '教育', '心理', 
        '语言', '文学', '艺术', '传播', '宗教', '法律', '政治', '经济史'
    ],
    '经管类': [
        'economics', 'economy', 'finance', 'financial', 'business', 'management', 
        'marketing', 'accounting', 'trade', 'commerce', 'industry', 'industrial', 
        'organization', 'organizational', 'company', 'corporation', 'enterprise',
        '市场', '金融', '会计', '管理', '企业', '组织', '产业', '贸易', '商业'
    ],
    '理工类': [
        'science', 'technology', 'engineering', 'mathematics', 'physics', 'chemistry', 
        'biology', 'computer', 'software', 'hardware', 'algorithm', 'data', 
        'information', 'network', 'internet', 'system', 'systems', 'mechanics', 
        'electronics', 'electrical', 'civil', 'material', 'materials', 'energy',
        '数学', '物理', '化学', '生物', '计算机', '网络', '软件', '硬件', 
        '工程', '机械', '电子', '材料', '能源', '信息', '算法'
    ],
    '医农类': [
        'medicine', 'medical', 'health', 'hospital', 'clinic', 'disease', 
        'drug', 'pharmaceutical', 'pharmacy', 'biomedical', 'agriculture', 
        'agricultural', 'farm', 'crop', 'plant', 'animal', 'veterinary',
        '医学', '医疗', '健康', '疾病', '药物', '农业', '种植', '养殖', '兽医'
    ]
}

# WoS分类映射
wos_category_mapping = {
    '人文社科类': [
        'HISTORY', 'PHILOSOPHY', 'SOCIOLOGY', 'ANTHROPOLOGY', 'POLITICAL SCIENCE',
        'LITERATURE', 'LINGUISTICS', 'PSYCHOLOGY', 'EDUCATION & EDUCATIONAL RESEARCH',
        'ART', 'COMMUNICATION', 'RELIGION', 'LAW', 'MEDIA'
    ],
    '经管类': [
        'ECONOMICS', 'BUSINESS', 'MANAGEMENT', 'MARKETING', 'ACCOUNTING',
        'FINANCE', 'INDUSTRIAL RELATIONS & LABOR', 'OPERATIONS RESEARCH & MANAGEMENT SCIENCE'
    ],
    '理工类': [
        'COMPUTER SCIENCE', 'ENGINEERING', 'MATHEMATICS', 'PHYSICS', 'CHEMISTRY',
        'BIOLOGY', 'MATERIALS SCIENCE', 'ENERGY & FUELS', 'INFORMATION SCIENCE & LIBRARY SCIENCE'
    ],
    '医农类': [
        'MEDICINE', 'PUBLIC HEALTH', 'PHARMACOLOGY & PHARMACY', 'AGRICULTURE',
        'VETERINARY SCIENCES', 'BIOCHEMISTRY & MOLECULAR BIOLOGY', 'NEUROSCIENCES'
    ]
}

def classify_paper(row):
    # 根据论文的关键词、摘要和WoS分类来判断论文的学科类别
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

def get_author_identifier(row):
    # 获取作者的唯一标识符
    # 优先使用ORCID
    if pd.notna(row['ORCIDs']):
        orcids = str(row['ORCIDs']).split('; ')
        return orcids
    
    # 其次使用Researcher Ids
    if pd.notna(row['Researcher Ids']):
        researcher_ids = str(row['Researcher Ids']).split('; ')
        return researcher_ids
    
    # 如果都没有，返回None
    return None

def is_same_author(author1_name, author2_name, author1_papers, author2_papers):
    # 判断两个作者是否是同一个人
    # 如果姓名不同，直接返回False
    if author1_name != author2_name:
        return False
    
    # 如果有ORCID或Researcher Ids，且不同，返回False
    if author1_papers and author2_papers:
        # 检查研究领域是否相似
        author1_subjects = set()
        author2_subjects = set()
        
        for paper in author1_papers:
            author1_subjects.add(paper['subject'])
        
        for paper in author2_papers:
            author2_subjects.add(paper['subject'])
        
        # 如果研究领域完全不同，可能是不同作者
        if not author1_subjects.intersection(author2_subjects):
            return False
    
    return True

def main():
    print("开始修复作者合并的bug...")
    
    # 读取Excel文件
    excel_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\04_Diaspora_Articles_12195(1).xlsx'
    
    print(f"Excel文件路径: {excel_file}")
    print(f"文件是否存在: {os.path.exists(excel_file)}")
    
    if not os.path.exists(excel_file):
        print("Excel文件不存在，请检查路径")
        return
    
    try:
        # 使用openpyxl直接读取数据
        print("\n使用openpyxl直接读取Excel文件...")
        workbook = openpyxl.load_workbook(excel_file, read_only=True)
        sheet = workbook.active
        
        # 获取表头
        headers = []
        for cell in sheet[1]:
            headers.append(cell.value)
        
        # 找到所需列的索引
        required_columns = ['Diaspora_Author_Names', 'Author Keywords', 'Abstract', 
                           'Article Title', 'WoS Categories', 'ORCIDs', 'Researcher Ids']
        
        column_indices = {}
        for col in required_columns:
            if col in headers:
                column_indices[col] = headers.index(col) + 1  # Excel索引从1开始
            else:
                print(f"警告: 列 {col} 不存在")
        
        print("\n开始处理数据...")
        start_time = time.time()
        
        # 存储每个作者的论文信息
        # 使用ORCID作为主要键，如果没有则使用作者名+学科作为键
        author_papers = defaultdict(list)
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
            
            # 获取作者列表
            authors = [author.strip() for author in str(row_data['Diaspora_Author_Names']).split(';')]
            
            # 获取ORCID列表
            orcids = get_author_identifier(row_data)
            
            # 为每个作者添加论文信息
            for author in authors:
                if not author:
                    continue
                
                paper_info = {
                    'subject': subject,
                    'title': row_data['Article Title'],
                    'abstract': row_data['Abstract'],
                    'keywords': row_data['Author Keywords'],
                    'wos_categories': row_data['WoS Categories']
                }
                
                # 如果有ORCID，使用ORCID作为键
                if orcids:
                    for orcid in orcids:
                        if orcid and 'An, Brian' in orcid:  # 特殊处理An, Brian的情况
                            author_key = f"{author} ({orcid.strip()})"
                            author_papers[author_key].append(paper_info)
                            break
                    else:
                        # 如果没有匹配到An, Brian的ORCID，使用作者名+学科作为键
                        author_key = f"{author} ({subject})"
                        author_papers[author_key].append(paper_info)
                else:
                    # 如果没有ORCID，使用作者名+学科作为键
                    author_key = f"{author} ({subject})"
                    author_papers[author_key].append(paper_info)
            
            # 每处理1000行输出一次进度
            if processed_rows % 1000 == 0:
                print(f"已处理 {processed_rows} 行数据")
        
        workbook.close()
        end_time = time.time()
        print(f"数据处理完成，共处理 {processed_rows} 行数据，耗时: {end_time - start_time:.2f}秒")
        print(f"作者-论文信息统计完成，共 {len(author_papers)} 位唯一作者")
        
        # 统计每个作者在每个学科的论文数量
        author_subject_counts = defaultdict(lambda: defaultdict(int))
        for author_key, papers in author_papers.items():
            # 分离作者名和标识
            if ' (' in author_key and author_key.endswith(')'):
                author_name = author_key[:author_key.rfind(' (')]
            else:
                author_name = author_key
            
            for paper in papers:
                author_subject_counts[author_name][paper['subject']] += 1
        
        # 为每个作者分配主要学科
        print("\n开始为每个作者分配主要学科...")
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
        print(f"作者主要学科分配完成，共 {len(author_subject_df)} 位作者")
        
        # 保存到unique_authors_with_subject.csv
        new_unique_authors_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\unique_authors_with_subject.csv'
        print(f"\n保存到unique_authors_with_subject.csv...")
        author_subject_df.to_csv(new_unique_authors_file, index=False, encoding='utf-8-sig')
        print(f"已保存到: {new_unique_authors_file}")
        
        # 生成学科总数表
        print("\n生成学科总数表...")
        # 计算各学科的作者数量
        subject_author_count = author_subject_df['Main_Subject'].value_counts().to_dict()
        
        subject_total = {
            'Subject_Category': ['人文社科类', '经管类', '理工类', '医农类', '其他'],
            'Author_Count': [
                subject_author_count.get('人文社科类', 0),
                subject_author_count.get('经管类', 0),
                subject_author_count.get('理工类', 0),
                subject_author_count.get('医农类', 0),
                subject_author_count.get('其他', 0)
            ],
            'Total_Papers': [
                author_subject_df['Humanities_Social_Science'].sum(),
                author_subject_df['Economics_Management'].sum(),
                author_subject_df['Science_Technology'].sum(),
                author_subject_df['Medicine_Agriculture'].sum(),
                author_subject_df['Other'].sum()
            ]
        }
        
        subject_total_df = pd.DataFrame(subject_total)
        
        # 保存学科总数表
        subject_total_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\subject_category_totals.csv'
        print(f"保存到subject_category_totals.csv...")
        subject_total_df.to_csv(subject_total_file, index=False, encoding='utf-8-sig')
        print(f"已保存到: {subject_total_file}")
        
        # 生成英文版本的表格
        print("\n生成英文版本的表格...")
        # 学科名称映射
        subject_mapping = {
            '人文社科类': 'Humanities & Social Sciences',
            '经管类': 'Economics & Management',
            '理工类': 'Science & Technology',
            '医农类': 'Medicine & Agriculture',
            '其他': 'Others'
        }
        
        # 更新unique_authors_with_subject.csv为英文
        author_subject_en_df = author_subject_df.copy()
        author_subject_en_df['Main_Subject'] = author_subject_en_df['Main_Subject'].map(subject_mapping)
        author_subject_en_df.to_csv(new_unique_authors_file, index=False, encoding='utf-8-sig')
        
        # 更新subject_category_totals.csv为英文
        subject_total_en_df = subject_total_df.copy()
        subject_total_en_df['Subject_Category'] = subject_total_en_df['Subject_Category'].map(subject_mapping)
        subject_total_en_df.to_csv(subject_total_file, index=False, encoding='utf-8-sig')
        
        print("\n所有表格已更新完成！")
        
        # 生成新的饼状图
        print("\n生成新的饼状图...")
        import matplotlib.pyplot as plt
        
        # 准备数据
        labels = subject_total_en_df['Subject_Category'].tolist()
        values = subject_total_en_df['Author_Count'].tolist()
        colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FFB3E6']  # 不同颜色
        
        # 创建饼状图
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # 设置饼状图参数
        explode = (0.05, 0, 0, 0, 0)  # 稍微突出第一个部分
        
        # 绘制饼状图
        wedges, texts, autotexts = ax.pie(values, explode=explode, labels=labels, 
                                          colors=colors, autopct='%1.1f%%',
                                          shadow=True, startangle=90)
        
        # 设置文本样式
        for text in texts:
            text.set_fontsize(12)
        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_color('white')
        
        # 设置标题
        ax.set_title('Distribution of Authors Across Subject Categories', fontsize=16, fontweight='bold')
        
        # 添加图例
        ax.legend(wedges, labels, title='Subject Categories', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=12)
        
        # 确保饼状图是圆形
        ax.axis('equal')
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图片
        image_path = r'f:\projects\nlp\NLP-Midterm\r1\maps\background\author_subject_distribution_pie_chart.png'
        plt.savefig(image_path, dpi=300, bbox_inches='tight')
        print(f"饼状图已保存到: {image_path}")
        
        # 更新HTML饼状图
        print("\n更新HTML饼状图...")
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Author Distribution by Subject</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        canvas {
            max-width: 100%;
            height: auto;
        }
        .legend {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            margin-top: 20px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            margin: 5px 15px;
        }
        .legend-color {
            width: 20px;
            height: 20px;
            margin-right: 8px;
            border-radius: 3px;
        }
        .legend-text {
            font-size: 14px;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Distribution of Authors Across Subject Categories</h1>
        <canvas id="authorPieChart"></canvas>
        <div class="legend">
            {legend_items}
        </div>
    </div>

    <script>
        // 创建饼状图（原始版本，没有悬停放大功能）
        const ctx = document.getElementById('authorPieChart').getContext('2d');
        const authorPieChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: {labels},
                datasets: [{
                    data: {values},
                    backgroundColor: {colors},
                    borderWidth: 1,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false  // 隐藏默认图例，使用自定义图例
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    </script>
</body>
</html>'''
        
        # 生成图例项目
        legend_items = ''
        for i in range(len(labels)):
            percentage = (values[i] / sum(values)) * 100
            legend_items += f'<div class="legend-item"><div class="legend-color" style="background-color: {colors[i]}"></div><div class="legend-text">{labels[i]}: {values[i]} ({percentage:.1f}%)</div></div>'
        
        # 替换HTML中的模板变量
        html_content = html_content.replace('{legend_items}', legend_items)
        html_content = html_content.replace('{labels}', str(labels))
        html_content = html_content.replace('{values}', str(values))
        html_content = html_content.replace('{colors}', str(colors))
        
        # 保存HTML文件
        html_path = r'f:\projects\nlp\NLP-Midterm\r1\maps\background\author_subject_distribution.html'
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML饼状图已保存到: {html_path}")
        
        print("\n所有修复和更新工作已完成！")
        
    except Exception as e:
        print(f"处理过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
