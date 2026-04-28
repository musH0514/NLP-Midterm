import openpyxl

# 使用openpyxl直接读取特定行
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
    print(f"Diaspora_Author_Names列位于索引 {author_col_idx}（Excel第 {author_col_idx + 1} 列）")
    
    # 检查第8613行
    row_idx = 8613
    print(f"\n检查04表第 {row_idx} 行的Diaspora_Author_Names列:")
    print("=" * 50)
    
    # 获取该行的Diaspora_Author_Names列的值
    cell = sheet.cell(row=row_idx, column=author_col_idx + 1)  # Excel单元格索引从1开始
    author_names = cell.value
    
    if author_names is not None:
        print(f"Diaspora_Author_Names: {author_names}")
        print(f"类型: {type(author_names)}")
        print(f"字符串长度: {len(str(author_names))}")
        
        # 检查是否包含'Ai, Angela'
        if 'Ai, Angela' in str(author_names):
            print(f"\n该行确实包含 'Ai, Angela'")
        else:
            print(f"\n该行不包含 'Ai, Angela'")
    else:
        print(f"Diaspora_Author_Names: None")
else:
    print("Diaspora_Author_Names列不存在")

workbook.close()
