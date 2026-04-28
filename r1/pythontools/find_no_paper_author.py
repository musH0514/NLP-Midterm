import openpyxl

# 标记为"无论文"的作者是"Ai, Angela"
no_paper_author = "Ai, Angela"
print(f"正在查找作者 {no_paper_author} 在04表中的位置...")

# 使用openpyxl直接读取Excel文件
excel_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\04_Diaspora_Articles_12195(1).xlsx'
workbook = openpyxl.load_workbook(excel_file, read_only=True)
sheet = workbook.active

# 获取表头
headers = []
for cell in sheet[1]:
    headers.append(cell.value)

# 找到Diaspora_Author_Names列的索引
if 'Diaspora_Author_Names' in headers:
    author_col_idx = headers.index('Diaspora_Author_Names')
    print(f"Diaspora_Author_Names列位于第 {author_col_idx + 1} 列")
    
    found_rows = []
    # 逐行搜索
    print("开始逐行搜索...")
    for row_idx, row in enumerate(sheet.iter_rows(min_row=2), start=2):  # 从第二行开始，行号从2开始
        if author_col_idx < len(row) and row[author_col_idx].value is not None:
            author_names = str(row[author_col_idx].value)
            # 检查作者是否在该行
            if no_paper_author in author_names:
                found_rows.append(row_idx)
                print(f"  找到: 第 {row_idx} 行")
        
        # 每处理1000行输出一次进度
        if row_idx % 1000 == 0:
            print(f"  已处理 {row_idx} 行")
    
    if found_rows:
        print(f"\n搜索完成！找到 {len(found_rows)} 行包含作者 {no_paper_author}:")
        for row in found_rows:
            print(f"  第 {row} 行")
    else:
        print(f"\n搜索完成！在04表中未找到作者 {no_paper_author} 的论文")
else:
    print("Diaspora_Author_Names列不存在")

workbook.close()
