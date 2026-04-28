import openpyxl
import os

# 读取Excel文件，使用openpyxl的read_only模式
excel_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\04_Diaspora_Articles_12195(1).xlsx'

print(f"正在读取Excel文件: {excel_file}")
print(f"文件是否存在: {os.path.exists(excel_file)}")

try:
    # 使用read_only模式打开文件
    workbook = openpyxl.load_workbook(excel_file, read_only=True)
    sheet = workbook.active
    
    # 获取表头
    headers = []
    for cell in sheet[1]:
        headers.append(cell.value)
    
    # 找到需要的列索引
    author_col_idx = headers.index('Diaspora_Author_Names') if 'Diaspora_Author_Names' in headers else -1
    wos_col_idx = headers.index('WoS Categories') if 'WoS Categories' in headers else -1
    
    # 查找包含"ID"或"id"的列及其索引
    id_columns = {}
    for i, col in enumerate(headers):
        if col and 'id' in str(col).lower():
            id_columns[col] = i
    
    print(f"\n找到的ID相关列: {list(id_columns.keys())}")
    
    # 查找作者为"An, Brian P."的所有记录
    author_name = "An, Brian P."
    author_records = []
    all_ids = {}
    all_categories = {}
    
    print(f"\n开始搜索包含 '{author_name}' 的记录...")
    
    # 逐行读取数据
    for row_num, row in enumerate(sheet.iter_rows(min_row=2), start=2):
        # 检查作者列
        if author_col_idx != -1 and row[author_col_idx].value:
            if author_name in str(row[author_col_idx].value):
                # 收集ID信息
                row_ids = {}
                for id_col, idx in id_columns.items():
                    if idx < len(row) and row[idx].value is not None:
                        row_ids[id_col] = row[idx].value
                        # 添加到全局ID集合
                        if id_col not in all_ids:
                            all_ids[id_col] = set()
                        all_ids[id_col].add(row[idx].value)
                
                # 收集WoS分类信息
                if wos_col_idx != -1 and row[wos_col_idx].value:
                    wos_cats = str(row[wos_col_idx].value).split('; ')
                    for cat in wos_cats:
                        if cat:
                            all_categories[cat] = all_categories.get(cat, 0) + 1
                
                author_records.append({"row": row_num, "ids": row_ids})
    
    print(f"搜索完成，找到 {len(author_records)} 条包含 '{author_name}' 的记录")
    
    # 显示ID信息
    print(f"\nID信息分析:")
    for id_col, ids in all_ids.items():
        print(f"  {id_col}: {len(ids)} 个不同值")
        if len(ids) <= 5:  # 只显示不多于5个的ID值
            print(f"    值: {ids}")
        else:
            print(f"    部分值: {list(ids)[:5]}...")
        
        if len(ids) > 1:
            print(f"    ⚠️  注意：{author_name} 在 {id_col} 列有 {len(ids)} 个不同的值，可能是同名不同作者！")
    
    # 检查是否有唯一标识作者的ID
    print(f"\n作者标识分析:")
    if 'Researcher Ids' in all_ids and len(all_ids['Researcher Ids']) > 1:
        print(f"    Researcher Ids 有多个不同值，说明确实存在多个同名作者")
    elif 'ORCIDs' in all_ids and len(all_ids['ORCIDs']) > 1:
        print(f"    ORCIDs 有多个不同值，说明确实存在多个同名作者")
    else:
        print(f"    没有找到明确的多个作者标识，但需要进一步分析")
    
    # 显示学科分布
    print(f"\n学科分布情况:")
    if all_categories:
        total_categories = sum(all_categories.values())
        print(f"    共涉及 {len(all_categories)} 个学科分类，{total_categories} 次出现")
        # 只显示出现次数最多的前5个学科
        sorted_categories = sorted(all_categories.items(), key=lambda x: x[1], reverse=True)[:5]
        for cat, count in sorted_categories:
            print(f"    {cat}: {count} 次")
        if len(all_categories) > 5:
            print(f"    ... 还有 {len(all_categories) - 5} 个学科分类")
    else:
        print(f"    未找到WoS分类信息")
    
    print(f"\n结论:")
    if any(len(ids) > 1 for ids in all_ids.values()):
        print(f"    {author_name} 很可能是多个同名不同作者的集合，因为在ID列中发现了多个不同的值")
    else:
        print(f"    {author_name} 可能是同一个作者发表了多个领域的论文，或者ID信息不完整")
    
    workbook.close()
    
except Exception as e:
    print(f"处理过程中出错: {e}")
    import traceback
    traceback.print_exc()
