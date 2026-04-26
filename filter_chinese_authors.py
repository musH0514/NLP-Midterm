import csv
import zipfile
import xml.etree.ElementTree as ET
import sys


def load_chinese_surnames(xlsx_path):
    """从 .xlsx 文件（实际为 ZIP 格式）读取姓氏拼音列表。"""
    surnames = set()
    shared = {}

    with zipfile.ZipFile(xlsx_path, 'r') as z:
        # 读取共享字符串表
        try:
            with z.open('xl/sharedStrings.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                ns = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
                for i, si in enumerate(root.iter(ns + 'si')):
                    t = si.find('.//' + ns + 't')
                    if t is not None:
                        shared[str(i)] = t.text
        except KeyError:
            pass

        # 读取工作表
        with z.open('xl/worksheets/sheet1.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            ns = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
            rows = list(root.iter(ns + 'row'))
            for i, row in enumerate(rows):
                cells = []
                for c in row.iter(ns + 'c'):
                    v = c.find(ns + 'v')
                    t_attr = c.get('t')
                    if v is not None:
                        if t_attr == 's':
                            cells.append(shared.get(v.text, v.text))
                        else:
                            cells.append(v.text)
                    else:
                        cells.append('')
                # 跳过表头，取第二列（姓氏拼音）
                if i > 0 and len(cells) >= 2:
                    pinyin = cells[1].strip().lower()
                    if pinyin:
                        surnames.add(pinyin)

    return surnames


def get_address_last_part(address):
    """获取地址字符串按逗号分割后的最后一小节（去掉首尾空格）。"""
    if not address:
        return ''
    parts = [p.strip() for p in address.split(',') if p.strip()]
    return parts[-1] if parts else ''


def is_china_region(last_part):
    """判断地址最后一小节是否属于中国大陆、香港、澳门或台湾。"""
    lp = last_part.lower()
    keywords = [
        'china',               # 包含 people's republic of china, peoples r china 等
        'hong kong',
        'taiwan',
        'macau',
        'macao',
    ]
    for kw in keywords:
        if kw in lp:
            return True
    return False


def main():
    surnames_xlsx = 'chinese_surname.csv'      # 实际为 xlsx 格式
    input_csv = 'name_address_year.csv'
    output_csv = 'chinesename_address_year.csv'

    print('Loading Chinese surnames...')
    surnames = load_chinese_surnames(surnames_xlsx)
    print(f'Loaded {len(surnames)} Chinese surname pinyin entries.')

    # 第一步：读取所有记录，筛选出中国人名的记录，并按 name 分组
    chinese_name_rows = []
    author_rows = {}  # name -> list of rows

    with open(input_csv, 'r', encoding='utf-8-sig') as fin:
        reader = csv.DictReader(fin)
        fieldnames = reader.fieldnames

        for row in reader:
            name = row.get('name', '').strip()
            address = row.get('address', '').strip()

            if ',' not in name:
                continue

            # name 格式为 "Lastname, Firstname"，逗号前是姓
            surname_part = name.split(',')[0].strip().lower()

            if surname_part not in surnames:
                continue

            chinese_name_rows.append(row)
            author_rows.setdefault(name, []).append(row)

    # 第二步：判断每个作者是否有海外地址记录
    authors_with_overseas = set()
    for name, rows in author_rows.items():
        for row in rows:
            address = row.get('address', '').strip()
            last_part = get_address_last_part(address)
            if not is_china_region(last_part):
                authors_with_overseas.add(name)
                break

    # 第三步：保留有海外地址的作者的所有记录
    kept_rows = []
    for row in chinese_name_rows:
        name = row.get('name', '').strip()
        if name in authors_with_overseas:
            kept_rows.append(row)

    # 第四步：输出到 CSV
    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as fout:
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        for row in kept_rows:
            writer.writerow(row)

    distinct_authors = len(authors_with_overseas)
    total_records = len(kept_rows)

    print(f'Total Chinese surname rows: {len(chinese_name_rows)}')
    print(f'Authors with overseas address: {distinct_authors}')
    print(f'Kept records (all rows for authors with overseas address): {total_records}')
    print(f'Output written to: {output_csv}')


if __name__ == '__main__':
    main()
