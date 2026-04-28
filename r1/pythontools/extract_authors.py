import pandas as pd

# 读取Excel文件
def extract_authors():
    input_file = '04_Diaspora_Articles_12195(1).xlsx'
    output_file = 'extracted_authors.csv'
    
    print(f"Reading Excel file: {input_file}")
    # 读取Excel文件
    df = pd.read_excel(input_file)
    
    print(f"Columns in the file: {list(df.columns)}")
    
    # 检查是否存在Diaspora_Author_Names列
    if 'Diaspora_Author_Names' not in df.columns:
        print("Error: Diaspora_Author_Names column not found!")
        return
    
    # 提取作者列
    author_column = df['Diaspora_Author_Names']
    
    # 收集所有作者名字
    all_authors = []
    
    for authors in author_column:
        if pd.notna(authors):
            # 处理分号分隔的多个作者
            authors_list = [author.strip() for author in str(authors).split(';') if author.strip()]
            all_authors.extend(authors_list)
    
    # 去重
    unique_authors = list(set(all_authors))
    
    # 按字母顺序排序
    unique_authors.sort()
    
    # 创建新的DataFrame
    result_df = pd.DataFrame({'Author': unique_authors})
    
    # 保存为CSV文件
    result_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"Extraction completed!")
    print(f"Total authors found: {len(all_authors)}")
    print(f"Unique authors after deduplication: {len(unique_authors)}")
    print(f"Results saved to: {output_file}")

if __name__ == '__main__':
    extract_authors()