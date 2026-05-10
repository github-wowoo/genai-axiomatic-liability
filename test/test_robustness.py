"""
稳健性测试单元测试
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../code"))

from robustness_test import run_full_robustness_test

def test_robustness():
    test_pass = run_full_robustness_test()
    assert test_pass == True
    print("🎉 稳健性测试所有单元测试通过！")

if __name__ == "__main__":
    test_robustness()