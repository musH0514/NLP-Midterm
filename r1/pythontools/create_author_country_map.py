import pandas as pd
import folium
from mapclassify import FisherJenks
import os

# 打印当前工作目录
print(f"当前工作目录: {os.getcwd()}")

# 读取数据
df = pd.read_csv('../csv/author_countries.csv')
print(f"数据读取完成，总行数: {len(df)}")

# 移除没有国家的行
df = df[df['Country'].notna() & (df['Country'] != '')]
print(f"移除空国家后的数据行数: {len(df)}")

# 统计每个国家的作者数量（一个作者有多个国家时，每个国家都计数）
country_counts = df['Country'].value_counts().reset_index()
country_counts.columns = ['Country', 'AuthorCount']
print(f"国家统计完成，国家数量: {len(country_counts)}")
print("前10个国家的作者数量:")
print(country_counts.head(10))

# 保存统计结果到CSV文件
country_counts.to_csv('../csv/country_author_counts.csv', index=False)
print("国家作者数量统计已保存到 ../csv/country_author_counts.csv")

# 需要处理国家名称不匹配的问题
# Folium使用的是ISO 3166-1 alpha-3国家代码，所以需要将国家名称转换为代码
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

# 创建包含国家代码的新数据框
country_data = []
for _, row in country_counts.iterrows():
    country = row['Country']
    count = row['AuthorCount']
    if country in country_code_mapping:
        country_data.append({
            'Country': country,
            'Code': country_code_mapping[country],
            'AuthorCount': count
        })

# 转换为DataFrame
country_data_df = pd.DataFrame(country_data)
print(f"映射后的国家数据数量: {len(country_data_df)}")
print("映射后的部分数据:")
print(country_data_df.head(10))

# 创建地图
m = folium.Map(location=[20, 0], zoom_start=2)
print("地图对象创建完成")

# 直接使用手动设置的分组区间，确保覆盖所有数据
max_count = country_data_df['AuthorCount'].max()
print(f"最大作者数量: {max_count}")

# 优化分组区间，进一步区分800名以上的作者数量
bins = [0, 20, 100, 300, 800, 1000, 5500]  # 增加800-1000和1000+两个区间
print(f"使用优化的分组区间: {bins}")

# 创建自定义颜色方案，确保颜色差异明显，特别是800名以上的区间
custom_colors = {
    0: '#ffffff',      # 白色 - 没有作者
    1: '#ffffb2',      # 浅黄色 - 1-20名作者
    2: '#fecc5c',      # 黄色 - 21-100名作者
    3: '#fd8d3c',      # 橙色 - 101-300名作者
    4: '#e31a1c',      # 红色 - 301-800名作者
    5: '#bd0026',      # 深红色 - 801-1000名作者
    6: '#581845'       # 深紫色 - 1000名以上作者
}

# 使用替代方案：完全自定义的GeoJson图层，更好地控制图例
print("使用自定义GeoJson图层替代Choropleth，以获得更好的图例控制")
try:
    # 读取世界地图数据
    import json
    import requests
    response = requests.get('https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json')
    world_geojson = response.json()
    
    # 创建颜色映射函数，使用优化的区间
    def get_color(count):
        if count == 0:
            return custom_colors[0]
        elif count <= 20:
            return custom_colors[1]
        elif count <= 100:
            return custom_colors[2]
        elif count <= 300:
            return custom_colors[3]
        elif count <= 800:
            return custom_colors[4]
        elif count <= 1000:
            return custom_colors[5]
        else:
            return custom_colors[6]
    
    # 为每个国家添加作者数量信息
    country_dict = country_data_df.set_index('Code')['AuthorCount'].to_dict()
    for feature in world_geojson['features']:
        country_code = feature['id']
        feature['properties']['AuthorCount'] = country_dict.get(country_code, 0)
    
    # 添加GeoJson图层
    folium.GeoJson(
        world_geojson,
        style_function=lambda feature: {
            'fillColor': get_color(feature['properties']['AuthorCount']),
            'color': '#000000',
            'fillOpacity': 0.75,
            'weight': 0.2
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['name', 'AuthorCount'],
            aliases=['Country:', 'Number of Authors:'],
            localize=True
        )
    ).add_to(m)
    print("自定义GeoJson图层添加完成")
    
    # 创建自定义图例
    # 使用folium的Element方法手动创建HTML图例
    from branca.element import Template, MacroElement
    
    template = """{% macro html(this, kwargs) %}
    <div style="position: fixed;
                bottom: 50px;
                right: 50px;
                width: 200px;
                height: 290px;
                z-index:9999;
                font-size:14px;
                background-color: white;
                border:2px solid grey;
                padding: 10px;">
        <h4 style="margin-top: 0;">Number of Authors</h4>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <div style="width: 20px; height: 20px; background-color: {{this.custom_colors[0]}}; border: 1px solid black;"></div>
            <div style="margin-left: 10px;">0</div>
        </div>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <div style="width: 20px; height: 20px; background-color: {{this.custom_colors[1]}}; border: 1px solid black;"></div>
            <div style="margin-left: 10px;">1-20</div>
        </div>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <div style="width: 20px; height: 20px; background-color: {{this.custom_colors[2]}}; border: 1px solid black;"></div>
            <div style="margin-left: 10px;">21-100</div>
        </div>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <div style="width: 20px; height: 20px; background-color: {{this.custom_colors[3]}}; border: 1px solid black;"></div>
            <div style="margin-left: 10px;">101-300</div>
        </div>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <div style="width: 20px; height: 20px; background-color: {{this.custom_colors[4]}}; border: 1px solid black;"></div>
            <div style="margin-left: 10px;">301-800</div>
        </div>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <div style="width: 20px; height: 20px; background-color: {{this.custom_colors[5]}}; border: 1px solid black;"></div>
            <div style="margin-left: 10px;">801-1000</div>
        </div>
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <div style="width: 20px; height: 20px; background-color: {{this.custom_colors[6]}}; border: 1px solid black;"></div>
            <div style="margin-left: 10px;">1000+</div>
        </div>
    </div>
    {% endmacro %}
    """
    
    macro = MacroElement()
    macro._template = Template(template)
    macro.custom_colors = custom_colors
    m.get_root().add_child(macro)
    print("自定义图例添加完成")
    
except Exception as e:
    print(f"添加自定义图层和图例时出错: {e}")
    import traceback
    traceback.print_exc()


# 移除重复的提示信息代码，因为替代图层已经包含了此功能
print("替代图层已包含工具提示功能，跳过重复添加")


# 添加图层控制器
folium.LayerControl().add_to(m)
print("图层控制器添加完成")

# 保存地图
map_path = '../maps/active/author_country_map.html'
try:
    m.save(map_path)
    print(f"作者国家分布图已保存到 {map_path}")
    # 验证文件是否存在
    if os.path.exists(map_path):
        print(f"文件存在，大小: {os.path.getsize(map_path)} 字节")
    else:
        print("文件保存失败，文件不存在")
except Exception as e:
    print(f"保存地图时出错: {e}")
    import traceback
    traceback.print_exc()


