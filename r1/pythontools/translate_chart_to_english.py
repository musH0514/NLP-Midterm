import pandas as pd
import os

print("开始将图表文本从中文转换为英文...")

# 读取高活跃度作者表
highly_productive_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\highly_productive_scholars.csv'
df_highly = pd.read_csv(highly_productive_file)

# 读取作者学科分类表
subject_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\unique_authors_with_subject.csv'
df_subject = pd.read_csv(subject_file)

# 合并两个表，获取高活跃度作者的学科信息
merged_df = pd.merge(df_highly, df_subject, on='Author', how='left')

# 统计每个学科的高活跃度作者数量
subject_counts = merged_df['Main_Subject'].value_counts()

# 准备数据
labels = list(subject_counts.index)
values = [int(v) for v in subject_counts.values]
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']

print(f"数据标签: {labels}")
print(f"数据值: {values}")
print(f"颜色: {colors}")

# 创建全英文的HTML内容
html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Subject Distribution of Active Authors</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .chart-container {
            position: relative;
            height: 400px;
            margin: 30px 0;
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
            border-radius: 3px;
            margin-right: 8px;
        }
        .legend-text {
            font-size: 14px;
            color: #333;
        }
        .stats {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 5px;
        }
        .total-count {
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Subject Distribution of Active Authors</h1>
        <div class="chart-container">
            <canvas id="activeSubjectChart"></canvas>
        </div>
        <div class="legend">
            {legend_items}
        </div>
        <div class="stats">
            <div class="total-count">Total Active Authors: {total_authors}</div>
        </div>
    </div>
    <script>
        const ctx = document.getElementById('activeSubjectChart').getContext('2d');
        const activeSubjectChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: {labels},
                datasets: [{
                    label: 'Number of Authors',
                    data: {values},
                    backgroundColor: {colors},
                    borderWidth: 1,
                    borderColor: '#ffffff',
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return 'Number of Authors: ' + context.parsed.y;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                },
                animation: {
                    duration: 1000,
                    easing: 'easeOutBounce'
                }
            }
        });
    </script>
</body>
</html>'''

# 生成图例项
legend_items = []
for label, color in zip(labels, colors):
    legend_items.append(f'<div class="legend-item"><div class="legend-color" style="background-color: {color}"></div><div class="legend-text">{label}</div></div>')
legend_html = '\n            '.join(legend_items)

# 替换HTML中的占位符
html_content = html_content.replace('{labels}', str(labels).replace("'", '"'))
html_content = html_content.replace('{values}', str(values))
html_content = html_content.replace('{colors}', str(colors).replace("'", '"'))
html_content = html_content.replace('{legend_items}', legend_html)
html_content = html_content.replace('{total_authors}', str(len(df_highly)))

# 保存HTML文件
output_dir = r'f:\projects\nlp\NLP-Midterm\r1\maps\background'
html_output_file = os.path.join(output_dir, 'active_authors_subject_distribution.html')

with open(html_output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"英文版本HTML柱状图已保存到: {html_output_file}")

# 同时更新active_authors_subject_chart.py文件为英文版本
print("\n更新源脚本文件为英文版本...")
source_file = r'f:\projects\nlp\NLP-Midterm\r1\pythontools\active_authors_subject_chart.py'

with open(source_file, 'r', encoding='utf-8') as f:
    source_content = f.read()

# 替换中文文本为英文
source_content = source_content.replace('开始统计高活跃度作者的学科分布...', 'Starting to count subject distribution of active authors...')
source_content = source_content.replace('高活跃度作者总数:', 'Total number of active authors:')
source_content = source_content.replace('合并后的数据行数:', 'Number of merged data rows:')
source_content = source_content.replace('统计各学科的高活跃度作者数量...', 'Counting the number of active authors in each subject...')
source_content = source_content.replace('学科分布:', 'Subject distribution:')
source_content = source_content.replace('警告: 有', 'Warning: There are')
source_content = source_content.replace('位高活跃度作者没有学科信息', 'active authors without subject information')
source_content = source_content.replace('他们是:', 'They are:')
source_content = source_content.replace('生成柱状图...', 'Generating bar chart...')
source_content = source_content.replace('高活跃度作者学科分布', 'Subject Distribution of Active Authors')
source_content = source_content.replace('学科类别', 'Subject Category')
source_content = source_content.replace('作者数量', 'Number of Authors')
source_content = source_content.replace('柱状图已保存到:', 'Bar chart saved to:')
source_content = source_content.replace('生成HTML版本的柱状图...', 'Generating HTML version of the bar chart...')
source_content = source_content.replace('高活跃度作者学科分布', 'Subject Distribution of Active Authors')
source_content = source_content.replace('作者数量', 'Number of Authors')
source_content = source_content.replace('HTML柱状图已保存到:', 'HTML bar chart saved to:')
source_content = source_content.replace('统计和图表生成完成！', 'Statistics and chart generation completed!')

# 替换HTML模板中的中文
source_content = source_content.replace('<!DOCTYPE html>\n<html lang="zh-CN">', '<!DOCTYPE html>\n<html lang="en">')
source_content = source_content.replace('<title>高活跃度作者学科分布</title>', '<title>Subject Distribution of Active Authors</title>')
source_content = source_content.replace('<h1>高活跃度作者学科分布</h1>', '<h1>Subject Distribution of Active Authors</h1>')
source_content = source_content.replace('label: \'作者数量\',', 'label: \'Number of Authors\',')
source_content = source_content.replace('return \'作者数量: \' + context.parsed.y;', 'return \'Number of Authors: \' + context.parsed.y;')
source_content = source_content.replace('<div class="total-count">高活跃度作者总数: {total_authors}</div>', '<div class="total-count">Total Active Authors: {total_authors}</div>')

with open(source_file, 'w', encoding='utf-8') as f:
    f.write(source_content)

print(f"源脚本文件已更新为英文版本: {source_file}")
print("\n图表文本已成功转换为英文！")
