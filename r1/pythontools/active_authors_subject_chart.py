import pandas as pd
import matplotlib.pyplot as plt
import os

print("Starting to count subject distribution of active authors...")

# 读取高活跃度作者表
highly_productive_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\highly_productive_scholars.csv'
df_highly = pd.read_csv(highly_productive_file)

print(f"Total number of active authors: {len(df_highly)}")

# 读取作者学科分类表
subject_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\unique_authors_with_subject.csv'
df_subject = pd.read_csv(subject_file)

# 合并两个表，获取高活跃度作者的学科信息
merged_df = pd.merge(df_highly, df_subject, on='Author', how='left')

print(f"Number of merged data rows: {len(merged_df)}")

# 检查是否有作者没有匹配到学科信息
missing_subject = merged_df[merged_df['Main_Subject'].isna()]
if not missing_subject.empty:
    print(f"Warning: There are {len(missing_subject)} active authors without subject information")
    print("They are:")
    for author in missing_subject['Author']:
        print(f"  - {author}")

# 统计每个学科的高活跃度Number of Authors
print("\nCounting the number of active authors in each subject...")
subject_counts = merged_df['Main_Subject'].value_counts()
print("Subject distribution:")
print(subject_counts)

# 生成柱状图
print("\nGenerating bar chart...")

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 创建图表
plt.figure(figsize=(10, 6))
subject_counts.plot(kind='bar', color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'])

# 添加标题和标签
plt.title('Subject Distribution of Active Authors', fontsize=16)
plt.xlabel('Subject Category', fontsize=12)
plt.ylabel('Number of Authors', fontsize=12)

# 旋转x轴标签
plt.xticks(rotation=45, ha='right')

# 在柱子上显示数值
for i, v in enumerate(subject_counts):
    plt.text(i, v + 0.5, str(v), ha='center', va='bottom', fontweight='bold')

# 添加网格线
plt.grid(axis='y', alpha=0.3)

# 调整布局
plt.tight_layout()

# 保存图表
output_dir = r'f:\projects\nlp\NLP-Midterm\r1\maps\background'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_file = os.path.join(output_dir, 'active_authors_subject_distribution.png')
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Bar chart saved to: {output_file}")

# 生成HTML版本的柱状图
print("\nGenerating HTML version of the bar chart...")

# 准备数据
labels = list(subject_counts.index)
values = [int(v) for v in subject_counts.values]
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']

# 创建HTML内容
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
            <div class="total-count">Total number of active authors: {total_authors}</div>
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
html_output_file = os.path.join(output_dir, 'active_authors_subject_distribution.html')
with open(html_output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"HTMLBar chart saved to: {html_output_file}")
print("\nStatistics and chart generation completed!")
