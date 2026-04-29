import pandas as pd
import folium
from branca.element import Template, MacroElement
import os

# 打印当前工作目录
print(f"当前工作目录: {os.getcwd()}")

# 1. 读取高度活跃学者数据
highly_productive_df = pd.read_csv('../csv/highly_productive_scholars.csv')
print(f"高度活跃学者数据读取完成，总行数: {len(highly_productive_df)}")
print("前5行高度活跃学者数据:")
print(highly_productive_df.head())

# 2. 读取作者国家数据
author_countries_df = pd.read_csv('../csv/author_countries.csv')
print(f"\n作者国家数据读取完成，总行数: {len(author_countries_df)}")
print("前5行作者国家数据:")
print(author_countries_df.head())

# 3. 将高度活跃学者与国家数据关联
# 需要处理作者名称的格式问题，去除引号等
# 先处理高度活跃学者的作者名称格式
highly_productive_df['Author'] = highly_productive_df['Author'].str.strip('"')

# 处理作者国家数据的作者名称格式
author_countries_df['Author'] = author_countries_df['Author'].str.strip('"')

# 关联数据，获取高度活跃学者的国家信息
active_author_countries = pd.merge(
    highly_productive_df[['Author']],
    author_countries_df,
    on='Author',
    how='inner'
)

print(f"\n关联完成，高度活跃学者的国家数据行数: {len(active_author_countries)}")
print("前5行关联数据:")
print(active_author_countries.head())

# 4. 统计每个国家的高度活跃学者数量
country_counts = active_author_countries['Country'].value_counts().reset_index()
country_counts.columns = ['Country', 'ActiveAuthorCount']
print(f"\n国家统计完成，有高度活跃学者的国家数量: {len(country_counts)}")
print("前10个国家的高度活跃学者数量:")
print(country_counts.head(10))

# 保存统计结果到CSV文件
country_counts.to_csv('../csv/active_author_country_counts.csv', index=False)
print("\n高度活跃学者国家统计已保存到 ../csv/active_author_country_counts.csv")

# 5. 创建国家代码映射
country_code_mapping = {
    'United States': 'USA',
    'Canada': 'CAN',
    'South Korea': 'KOR',
    'Australia': 'AUS',
    'Malaysia': 'MYS',
    'China': 'CHN',
    'Netherlands': 'NLD',
    'United Kingdom': 'GBR',
    'Taiwan': 'TWN',
    'Vietnam': 'VNM',
    'France': 'FRA',
    'Singapore': 'SGP',
    'Japan': 'JPN',
    'Germany': 'DEU',
    'India': 'IND',
    'Hong Kong': 'HKG',
    'New Zealand': 'NZL',
    'Denmark': 'DNK',
    'Norway': 'NOR',
    'Finland': 'FIN',
    'Switzerland': 'CHE',
    'Ireland': 'IRL',
    'Spain': 'ESP',
    'Sweden': 'SWE',
    'Italy': 'ITA',
    'Thailand': 'THA',
    'Israel': 'ISR',
    'Belgium': 'BEL',
    'Poland': 'POL',
    'Russia': 'RUS',
    'Turkey': 'TUR',
    'Qatar': 'QAT',
    'Saudi Arabia': 'SAU',
    'Bangladesh': 'BGD',
    'Kuwait': 'KWT',
    'Sri Lanka': 'LKA',
    'Iran': 'IRN',
    'Oman': 'OMN',
    'Philippines': 'PHL',
    'Cambodia': 'KHM',
    'Greece': 'GRC',
    'Portugal': 'PRT',
    'Iraq': 'IRQ',
    'Mexico': 'MEX',
    'Brazil': 'BRA',
    'Egypt': 'EGY',
    'South Africa': 'ZAF',
    'Argentina': 'ARG',
    'UAE': 'ARE',
    'Lebanon': 'LBN',
    'Jordan': 'JOR',
    'Chile': 'CHL',
    'Colombia': 'COL',
    'Peru': 'PER'
}

# 6. 创建包含国家代码的新数据框
country_data = []
for _, row in country_counts.iterrows():
    country = row['Country']
    count = row['ActiveAuthorCount']
    if country in country_code_mapping:
        country_data.append({
            'Country': country,
            'Code': country_code_mapping[country],
            'ActiveAuthorCount': count
        })

# 转换为DataFrame
country_data_df = pd.DataFrame(country_data)
print(f"\n映射后的国家数据数量: {len(country_data_df)}")
print("映射后的部分数据:")
print(country_data_df.head(10))

# 7. 创建地图
m = folium.Map(location=[20, 0], zoom_start=2)
print("\n地图对象创建完成")

# 8. 设置分组区间和颜色方案
max_count = country_data_df['ActiveAuthorCount'].max()
print(f"最大高度活跃学者数量: {max_count}")

# 根据数据分布设置合理的分组区间
bins = [0, 5, 10, 20, 50, 100, 200]
print(f"使用的分组区间: {bins}")

# 创建自定义颜色方案
custom_colors = {
    0: '#ffffff',      # 白色 - 没有作者
    1: '#ffffb2',      # 浅黄色 - 1-5名作者
    2: '#fed976',      # 黄色 - 6-10名作者
    3: '#feb24c',      # 橙色 - 11-20名作者
    4: '#fd8d3c',      # 深橙色 - 21-50名作者
    5: '#fc4e2a',      # 红色 - 51-100名作者
    6: '#800026'       # 深紫色 - 100名以上作者
}

# 9. 创建颜色映射函数
def get_color(count):
    if count == 0:
        return custom_colors[0]
    elif count <= 5:
        return custom_colors[1]
    elif count <= 10:
        return custom_colors[2]
    elif count <= 20:
        return custom_colors[3]
    elif count <= 50:
        return custom_colors[4]
    elif count <= 100:
        return custom_colors[5]
    else:
        return custom_colors[6]

# 10. 使用自定义GeoJson图层创建世界地图
import json
import requests

# 读取世界地图数据
response = requests.get('https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json')
world_geojson = response.json()

# 为每个国家添加高度活跃学者数量信息
country_dict = country_data_df.set_index('Code')['ActiveAuthorCount'].to_dict()
for feature in world_geojson['features']:
    country_code = feature['id']
    feature['properties']['ActiveAuthorCount'] = country_dict.get(country_code, 0)

# 添加GeoJson图层
folium.GeoJson(
    world_geojson,
    style_function=lambda feature: {
        'fillColor': get_color(feature['properties']['ActiveAuthorCount']),
        'color': '#000000',
        'fillOpacity': 0.75,
        'weight': 0.2
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['name', 'ActiveAuthorCount'],
        aliases=['Country:', 'Active Authors:'],
        localize=True
    )
).add_to(m)
print("自定义GeoJson图层添加完成")

# 11. 创建自定义图例
template = """{% macro html(this, kwargs) %}
<div style="position: fixed;
            bottom: 50px;
            right: 50px;
            width: 200px;
            height: 250px;
            z-index:9999;
            font-size:14px;
            background-color: white;
            border:2px solid grey;
            padding: 10px;">
    <h4 style="margin-top: 0;">Active Authors</h4>
    <div style="display: flex; align-items: center; margin: 5px 0;">
        <div style="width: 20px; height: 20px; background-color: {{this.custom_colors[0]}}; border: 1px solid black;"></div>
        <div style="margin-left: 10px;">0</div>
    </div>
    <div style="display: flex; align-items: center; margin: 5px 0;">
        <div style="width: 20px; height: 20px; background-color: {{this.custom_colors[1]}}; border: 1px solid black;"></div>
        <div style="margin-left: 10px;">1-5</div>
    </div>
    <div style="display: flex; align-items: center; margin: 5px 0;">
        <div style="width: 20px; height: 20px; background-color: {{this.custom_colors[2]}}; border: 1px solid black;"></div>
        <div style="margin-left: 10px;">6-10</div>
    </div>
    <div style="display: flex; align-items: center; margin: 5px 0;">
        <div style="width: 20px; height: 20px; background-color: {{this.custom_colors[3]}}; border: 1px solid black;"></div>
        <div style="margin-left: 10px;">11-20</div>
    </div>
    <div style="display: flex; align-items: center; margin: 5px 0;">
        <div style="width: 20px; height: 20px; background-color: {{this.custom_colors[4]}}; border: 1px solid black;"></div>
        <div style="margin-left: 10px;">21-50</div>
    </div>
    <div style="display: flex; align-items: center; margin: 5px 0;">
        <div style="width: 20px; height: 20px; background-color: {{this.custom_colors[5]}}; border: 1px solid black;"></div>
        <div style="margin-left: 10px;">51-100</div>
    </div>
    <div style="display: flex; align-items: center; margin: 5px 0;">
        <div style="width: 20px; height: 20px; background-color: {{this.custom_colors[6]}}; border: 1px solid black;"></div>
        <div style="margin-left: 10px;">100+</div>
    </div>
</div>
{% endmacro %}
"""

macro = MacroElement()
macro._template = Template(template)
macro.custom_colors = custom_colors
m.get_root().add_child(macro)
print("自定义图例添加完成")

# 12. 添加图层控制器
folium.LayerControl().add_to(m)
print("图层控制器添加完成")

# 13. 保存地图
map_path = '../maps/active/active_author_world_map.html'
try:
    m.save(map_path)
    print(f"\n高度活跃学者世界分布图已保存到 {map_path}")
    # 验证文件是否存在
    if os.path.exists(map_path):
        print(f"文件存在，大小: {os.path.getsize(map_path)} 字节")
    else:
        print("文件保存失败，文件不存在")
except Exception as e:
    print(f"保存地图时出错: {e}")
    import traceback
    traceback.print_exc()
