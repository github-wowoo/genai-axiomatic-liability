
---

### 2. 核心代码文件（`code/` 文件夹）
#### `code/axiom_system.py`（公理系统核心定义）
```python
"""
Core Axiomatic System for GenAI Distributed Liability
Corresponds to Section 3.2 of the paper
"""
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Tuple

# --------------------------
# Core Enums & Data Structures
# --------------------------
class AxiomPriority(Enum):
    """Formal axiom priority ranking from the paper"""
    SUSTAINABILITY_PRIORITY = 0  # Absolute top priority
    REMEDY_PRIORITY = 1
    RISK_BENEFIT_MATCHING = 2
    TIERED_LIABILITY = 3
    FULL_LIFE_CYCLE_TRACEABILITY = 4

class StakeholderRole(Enum):
    """Core stakeholder roles from the GenAI lifecycle"""
    INFRASTRUCTURE_PROVIDER = "infrastructure_provider"
    MODEL_DEVELOPER = "model_developer"
    FINE_TUNER = "fine_tuner"
    SERVICE_OPERATOR = "service_operator"
    PROFESSIONAL_USER = "professional_user"
    NON_PROFESSIONAL_USER = "non_professional_user"

class LiabilityTier(Enum):
    """Tiered liability rules from Axiom 4"""
    STRICT_LIABILITY = "strict_liability"
    FAULT_LIABILITY = "fault_liability"
    LIMITED_LIABILITY = "limited_liability"

@dataclass
class Stakeholder:
    """Stakeholder entity with core attributes for liability calculation"""
    name: str
    role: StakeholderRole
    benefit_share: float  # 0-1, share of economic benefit from the system
    risk_control_capacity: float  # 0-1, ability to prevent/mitigate harm
    traceability_compliance: bool  # Whether the stakeholder met traceability duties
    is_commercial: bool = True

@dataclass
class HarmEvent:
    """Harm event details for liability attribution"""
    description: str
    causal_stakeholders: List[Stakeholder]
    harm_type: str  # copyright, defamation, privacy, fraud, misinformation
    is_cross_jurisdictional: bool = False
    is_open_source_context: bool = False

# --------------------------
# Core Axiom System Definition
# --------------------------
class GenAILiabilityAxiomSystem:
    def __init__(self):
        self.axiom_priority = AxiomPriority
        self.liability_tier_mapping = {
            StakeholderRole.MODEL_DEVELOPER: LiabilityTier.STRICT_LIABILITY,
            StakeholderRole.SERVICE_OPERATOR: LiabilityTier.STRICT_LIABILITY,
            StakeholderRole.FINE_TUNER: LiabilityTier.FAULT_LIABILITY,
            StakeholderRole.PROFESSIONAL_USER: LiabilityTier.FAULT_LIABILITY,
            StakeholderRole.NON_PROFESSIONAL_USER: LiabilityTier.LIMITED_LIABILITY,
            StakeholderRole.INFRASTRUCTURE_PROVIDER: LiabilityTier.FAULT_LIABILITY
        }

    def get_liability_tier(self, stakeholder: Stakeholder, open_source_adjustment: bool = False) -> LiabilityTier:
        """
        Apply Axiom 4 (Tiered Liability) with open-source adjustment rules
        """
        base_tier = self.liability_tier_mapping[stakeholder.role]
        
        # Open-source adjustment rules (Section 3.2 of the paper)
        if open_source_adjustment and not stakeholder.is_commercial:
            if stakeholder.role in [StakeholderRole.MODEL_DEVELOPER, StakeholderRole.FINE_TUNER]:
                return LiabilityTier.FAULT_LIABILITY
        
        return base_tier

    def calculate_liability_share(self, stakeholder: Stakeholder, harm_event: HarmEvent) -> float:
        """
        Core liability calculation based on all 5 axioms
        Returns liability share (0-1) for the stakeholder
        """
        # Axiom 1: Sustainability Priority (overarching filter)
        if self._violates_sustainability_principle(stakeholder, harm_event):
            return 1.0  # Full liability for sustainability violations
        
        # Axiom 5: Remedy Priority (joint liability flag)
        joint_liability_applicable = self._check_joint_liability(harm_event)
        
        # Axiom 2: Risk-Benefit Matching (core weight calculation)
        risk_benefit_weight = (stakeholder.benefit_share + stakeholder.risk_control_capacity) / 2
        
        # Axiom 4: Tiered Liability (multiplier adjustment)
        liability_tier = self.get_liability_tier(stakeholder, harm_event.is_open_source_context)
        tier_multiplier = self._get_tier_multiplier(liability_tier)
        
        # Axiom 3: Traceability (penalty for non-compliance)
        traceability_penalty = 1.2 if not stakeholder.traceability_compliance else 1.0
        
        # Final liability share calculation
        base_liability = risk_benefit_weight * tier_multiplier * traceability_penalty
        final_liability = min(max(base_liability, 0.0), 1.0)
        
        # Joint liability adjustment (full remedy access)
        if joint_liability_applicable and final_liability > 0:
            final_liability = max(final_liability, 0.1)  # Minimum 10% for joint liability
        
        return round(final_liability, 4)

    def _violates_sustainability_principle(self, stakeholder: Stakeholder, harm_event: HarmEvent) -> bool:
        """Axiom 1: Check if stakeholder action violates sustainable development principles"""
        # Intentional harm, systemic risk creation, or violation of vulnerable group protections
        if stakeholder.risk_control_capacity >= 0.8 and stakeholder.benefit_share >= 0.7 and not stakeholder.traceability_compliance:
            return True
        return False

    def _check_joint_liability(self, harm_event: HarmEvent) -> bool:
        """Axiom 5: Check if joint and several liability applies"""
        # Applies when multiple stakeholders contribute to the same harm
        return len(harm_event.causal_stakeholders) >= 2

    def _get_tier_multiplier(self, liability_tier: LiabilityTier) -> float:
        """Multiplier for tiered liability rules"""
        multiplier_mapping = {
            LiabilityTier.STRICT_LIABILITY: 1.0,
            LiabilityTier.FAULT_LIABILITY: 0.6,
            LiabilityTier.LIMITED_LIABILITY: 0.2
        }
        return multiplier_mapping[liability_tier]

    def resolve_liability_dispute(self, harm_event: HarmEvent) -> Tuple[Dict[str, float], bool]:
        """
        Resolve full liability dispute for a harm event
        Returns: (liability_shares_per_stakeholder, responsibility_gap_resolved)
        """
        liability_shares = {}
        total_liability = 0.0
        
        for stakeholder in harm_event.causal_stakeholders:
            share = self.calculate_liability_share(stakeholder, harm_event)
            liability_shares[stakeholder.name] = share
            total_liability += share
        
        # Normalize shares to 1.0 for joint liability
        if total_liability > 0:
            for name in liability_shares:
                liability_shares[name] = round(liability_shares[name] / total_liability, 4)
        
        # Check if responsibility gap is resolved (no unallocated liability)
        gap_resolved = total_liability >= 0.95  # 5% tolerance for rounding
        
        return liability_shares, gap_resolved