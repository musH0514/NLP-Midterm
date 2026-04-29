import re

print("修复机构类别分布图表...")

# 读取HTML文件
html_file = r'f:\projects\nlp\NLP-Midterm\r1\maps\background\institution_category_distribution.html'

with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 1. 修复图表配置中的双花括号问题
print("修复图表配置语法...")

# 将双花括号替换为单花括号
html_content = html_content.replace('{{', '{')
html_content = html_content.replace('}}', '}')

# 2. 将中文文本替换为英文
print("将中文替换为英文...")

# 中文到英文的映射
chinese_to_english = {
    # 页面标题
    '学者机构类别分布': 'Scholar Institution Category Distribution',
    '1. 主要机构类别分布': '1. Main Institution Category Distribution',
    '2. 所有机构类别分布': '2. All Institution Category Distribution',
    '3. 机构类别统计数据': '3. Institution Category Statistics',
    
    # 表格列名
    '机构类别': 'Institution Category',
    '主要机构类别人数': 'Main Category Count',
    '所有机构类别人数': 'All Categories Count',
    
    # 机构类别名称
    '高校': 'University',
    '其他': 'Other',
    '医疗机构': 'Medical Institution',
    '科研院所': 'Research Institution',
    '企业': 'Enterprise',
    
    # 图表配置
    '学者主要机构类别分布': 'Scholar Main Institution Category Distribution',
    '学者所有机构类别分布': 'Scholar All Institution Category Distribution',
    '人数': 'Number of Scholars'
}

# 替换所有中文文本
for chinese, english in chinese_to_english.items():
    html_content = html_content.replace(chinese, english)

# 3. 更新语言标签
html_content = html_content.replace('<html lang="zh-CN">', '<html lang="en">')

# 4. 更新页面标题标签
html_content = html_content.replace('<title>Scholar Institution Category Distribution</title>', '<title>Institution Category Distribution of Scholars</title>')

# 保存修复后的HTML文件
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"图表修复完成！")
print(f"修复后的文件：{html_file}")
print("\n修复内容：")
print("1. 修复了图表配置中的双花括号问题")
print("2. 将所有中文文本替换为英文")
print("3. 更新了页面语言标签为英文")
print("4. 更新了页面标题")
