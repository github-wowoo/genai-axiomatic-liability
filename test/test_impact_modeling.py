"""
SDG测算单元测试
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../code"))

from impact_modeling import run_sdg_impact_calculation

def test_sdg_modeling():
    test_pass = run_sdg_impact_calculation()
    assert test_pass == True
    print("🎉 SDG测算所有单元测试通过！")

if __name__ == "__main__":
    test_sdg_modeling()