import pandas as pd
import os

print("开始基于CSV文件的作者合作分析...")

# 1. 读取作者总列表，获取高活跃度和低活跃度作者
subject_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\unique_authors_with_subject.csv'
print("正在读取作者总列表...")
df_subject = pd.read_csv(subject_file)

# 区分高活跃度和低活跃度作者
high_df = df_subject[df_subject['Total_Papers'] >= 4]
low_df = df_subject[df_subject['Total_Papers'] < 4]

print(f"高活跃度作者 (≥4篇论文): {len(high_df)} 位")
print(f"低活跃度作者 (<4篇论文): {len(low_df)} 位")
print(f"总作者数: {len(df_subject)} 位")

# 2. 分析作者发表论文数的分布
print("\n=== 作者发表论文数分析 ===")
print(f"高活跃度作者平均发表论文数: {high_df['Total_Papers'].mean():.2f}")
print(f"高活跃度作者发表论文数中位数: {high_df['Total_Papers'].median()}")
print(f"低活跃度作者平均发表论文数: {low_df['Total_Papers'].mean():.2f}")
print(f"低活跃度作者发表论文数中位数: {low_df['Total_Papers'].median()}")

# 3. 基于论文总数和作者总数估算合作情况
# 计算每篇论文的平均作者数
# 总论文数 (来自04表) = 12195
# 所有作者的论文总数 = sum(df_subject['Total_Papers'])
total_papers = 12195  # 从04表获取的总论文数
sum_author_papers = df_subject['Total_Papers'].sum()

if total_papers > 0:
    avg_authors_per_paper = sum_author_papers / total_papers
    print(f"\n=== 合作情况估算 ===")
    print(f"总论文数: {total_papers}")
    print(f"所有作者发表论文总数: {sum_author_papers}")
    print(f"每篇论文平均作者数: {avg_authors_per_paper:.2f}")
    
    # 估算合作率（作者数>1的论文比例）
    # 这是一个简化的估算方法
    estimated_collab_rate = 1 - (total_papers / sum_author_papers)
    print(f"估算的论文合作率: {estimated_collab_rate:.4f}")

# 4. 生成对比表格
print("\n=== 高活跃度与低活跃度作者对比 ===")
print(f"{'指标':<25} | {'高活跃度作者':<15} | {'低活跃度作者':<15}")
print("-" * 60)
print(f"{'作者数量':<25} | {len(high_df):<15} | {len(low_df):<15}")
print(f"{'平均发表论文数':<25} | {high_df['Total_Papers'].mean():<15.2f} | {low_df['Total_Papers'].mean():<15.2f}")
print(f"{'中位数发表论文数':<25} | {high_df['Total_Papers'].median():<15} | {low_df['Total_Papers'].median():<15}")
print(f"{'总发表论文数':<25} | {high_df['Total_Papers'].sum():<15} | {low_df['Total_Papers'].sum():<15}")
if total_papers > 0:
    print(f"{'估算论文合作率':<25} | {estimated_collab_rate:<15.4f} | {estimated_collab_rate:<15.4f}")

# 5. 保存对比结果
print("\n正在保存对比结果...")
comparison_data = {
    'Metric': ['Number of Authors', 'Average Papers per Author', 'Median Papers per Author', 'Total Papers Published'],
    'Highly Productive Authors': [len(high_df), round(high_df['Total_Papers'].mean(), 2), high_df['Total_Papers'].median(), high_df['Total_Papers'].sum()],
    'Low Productive Authors': [len(low_df), round(low_df['Total_Papers'].mean(), 2), low_df['Total_Papers'].median(), low_df['Total_Papers'].sum()]
}

if total_papers > 0:
    comparison_data['Metric'].append('Estimated Collaboration Rate')
    comparison_data['Highly Productive Authors'].append(round(estimated_collab_rate, 4))
    comparison_data['Low Productive Authors'].append(round(estimated_collab_rate, 4))

df_comparison = pd.DataFrame(comparison_data)
comparison_file = r'f:\projects\nlp\NLP-Midterm\r1\csv\collaboration_comparison_simple.csv'
df_comparison.to_csv(comparison_file, index=False, encoding='utf-8-sig')

print(f"对比结果已保存到: {comparison_file}")
print("\n=== 分析完成！ ===")
print("注意：由于直接读取大型Excel文件的性能问题，本次分析使用了简化的方法")
print("完整的作者层面合作率分析需要更复杂的处理")
print("如果需要更精确的合作率分析，请考虑使用更强大的计算资源")
