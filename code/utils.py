"""
通用工具函数
"""
import pandas as pd

def export_results_to_excel(results_dict, filename="paper_results.xlsx"):
    """将所有结果导出为Excel文件，用于论文补充材料"""
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        for sheet_name, df in results_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f"所有结果已导出至 {filename}")

def validate_liability_sum(liability_shares):
    """验证责任份额总和为1（归一化校验）"""
    total = sum(liability_shares.values())
    return abs(total - 1.0) < 0.01

def format_citation(authors, title, journal, year, doi):
    """格式化论文引用，与参考文献格式一致"""
    return f"{authors}. {title}. {journal}, {year}. https://doi.org/{doi}"
