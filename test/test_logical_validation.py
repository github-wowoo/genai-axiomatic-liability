"""
逻辑验证单元测试
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../code"))

from logical_validation import test_consistency, test_independence, test_completeness

def test_full_logical_validation():
    consistency_pass = test_consistency()
    independence_pass = test_independence()
    completeness_pass = test_completeness()
    
    assert consistency_pass == True
    assert independence_pass == True
    assert completeness_pass == True
    print("🎉 逻辑验证所有测试通过！")

if __name__ == "__main__":
    test_full_logical_validation()