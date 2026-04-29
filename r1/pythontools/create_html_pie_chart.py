import pandas as pd
import os

# 读取学科总数表
totals_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\subject_category_totals.csv'
df_totals = pd.read_csv(totals_file)

# 过滤掉No Papers类别（因为它有0个作者）
df_pie = df_totals[df_totals['Subject_Category'] != 'No Papers']

# 准备数据
labels = df_pie['Subject_Category'].tolist()
values = df_pie['Author_Count'].tolist()
colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FFB3E6']  # 不同颜色

# 创建HTML内容（回归到最原始的状态，没有悬停放大功能）
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

# 创建目标目录（如果不存在）
target_dir = r'f:\projects\nlp\NLP-Midterm\r1\maps\background'
os.makedirs(target_dir, exist_ok=True)

# 保存HTML文件
html_path = os.path.join(target_dir, 'author_subject_distribution.html')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"已回归到原始状态的HTML饼状图已保存到: {html_path}")
print("已移除所有鼠标放大功能，仅保留基本显示功能")
