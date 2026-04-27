import csv
from collections import Counter, defaultdict


def main():
    input_file = 'chinesename_address_year.csv'
    output_file = 'activeauthors_timeperiod.csv'

    # 按年份分组存储作者名
    year_to_names = defaultdict(list)
    total_rows = 0

    with open(input_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_rows += 1
            name = row.get('name', '').strip()
            year_str = row.get('year', '').strip()
            if not name or not year_str:
                continue
            try:
                year = int(year_str)
            except ValueError:
                continue
            year_to_names[year].append(name)

    print(f"Total rows read: {total_rows}")

    if not year_to_names:
        print("No valid data found.")
        return

    min_year = min(year_to_names.keys())
    max_year = max(year_to_names.keys())
    print(f"Year range: {min_year} - {max_year}")

    # 窗口大小为5年，例如 1991-1995, 1992-1996, ...
    window_size = 5
    results = []
    distinct_authors = set()

    # 起始年份从 min_year 到 max_year - window_size + 1
    start = min_year
    end = max_year - window_size + 1

    for window_start in range(start, end + 1):
        window_end = window_start + window_size - 1
        # 收集这5年内的所有名字
        names_in_window = []
        for y in range(window_start, window_end + 1):
            names_in_window.extend(year_to_names.get(y, []))

        if not names_in_window:
            continue

        # 统计出现次数
        counter = Counter(names_in_window)
        time_period = f"{window_start}-{window_end}"

        for name, count in counter.items():
            if count >= 5:
                results.append((name, time_period))
                distinct_authors.add(name)

    # 按人名排序（同名记录会排在一起），再按时间段排序保证输出稳定
    results.sort(key=lambda item: (item[0], item[1]))

    # 写入结果CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'time_period'])
        writer.writerows(results)

    print(f"Output written to {output_file}")
    print(f"Total records: {len(results)}")
    print(f"Distinct authors count: {len(distinct_authors)}")


if __name__ == '__main__':
    main()
