"""
公理系统核心功能单元测试
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../code"))

from axiom_system import GenAILiabilityAxiomSystem, Stakeholder, StakeholderRole, HarmEvent

def test_axiom_system_initialization():
    """测试公理系统初始化"""
    system = GenAILiabilityAxiomSystem()
    assert system is not None
    assert len(system.liability_tier_mapping) == 6
    print("✅ 公理系统初始化测试通过")

def test_liability_tier_mapping():
    """测试责任层级映射"""
    system = GenAILiabilityAxiomSystem()
    
    # 测试模型开发者严格责任
    dev = Stakeholder("Test Dev", StakeholderRole.MODEL_DEVELOPER, 0.8, 0.9, True)
    tier = system.get_liability_tier(dev)
    assert tier.value == "strict_liability"
    
    # 测试普通用户有限责任
    user = Stakeholder("Test User", StakeholderRole.NON_PROFESSIONAL_USER, 0.1, 0.2, True)
    tier = system.get_liability_tier(user)
    assert tier.value == "limited_liability"
    
    print("✅ 责任层级映射测试通过")

def test_liability_calculation():
    """测试责任份额计算"""
    system = GenAILiabilityAxiomSystem()
    stakeholder = Stakeholder(
        name="Test Operator",
        role=StakeholderRole.SERVICE_OPERATOR,
        benefit_share=0.8,
        risk_control_capacity=0.9,
        traceability_compliance=True
    )
    harm_event = HarmEvent(
        description="Test Harm",
        causal_stakeholders=[stakeholder],
        harm_type="copyright"
    )
    
    liability_share = system.calculate_liability_share(stakeholder, harm_event)
    assert 0 <= liability_share <= 1
    print("✅ 责任份额计算测试通过")

def test_dispute_resolution():
    """测试责任纠纷解决"""
    system = GenAILiabilityAxiomSystem()
    stakeholder1 = Stakeholder("Dev", StakeholderRole.MODEL_DEVELOPER, 0.7, 0.8, True)
    stakeholder2 = Stakeholder("User", StakeholderRole.NON_PROFESSIONAL_USER, 0.3, 0.3, True)
    harm_event = HarmEvent(
        description="Test Dispute",
        causal_stakeholders=[stakeholder1, stakeholder2],
        harm_type="defamation"
    )
    
    liability_shares, resolved = system.resolve_liability_dispute(harm_event)
    assert resolved == True
    assert abs(sum(liability_shares.values()) - 1.0) < 0.01
    print("✅ 纠纷解决测试通过")

if __name__ == "__main__":
    test_axiom_system_initialization()
    test_liability_tier_mapping()
    test_liability_calculation()
    test_dispute_resolution()
    print("\n🎉 公理系统所有单元测试通过！")