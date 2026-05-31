---
name: ccfts-fr-spv-period-end-adjustments
description: >
  SPV（投资管理类，Type A）期末调整规则。填充 ccfts-fr-all-period-end-adjustments 的 SLOT。
  触发条件：SPV/投资管理类非季度末快报编制。
version: 0.2
jurisdiction: CN
tax_year: 2025
category: financial-reporting
domains: [fr]
quality_tier: research-verified
verified_by: pending
entity_levels: [spv]
enterprise_scales: [large-soe]
depends_on:
  - ccfts-workflow-base
  - ccfts-fr-all-entity-type-rules
references:
  - ccfts-fr-all-period-end-adjustments
is_base: false
fills_slots_for: ccfts-fr-all-period-end-adjustments
slots: []
triggers:
  - SPV期末调整
  - 投资管理类期末调整
---

# SPV（投资管理类/Type A）期末调整

> 填充 `ccfts-fr-all-period-end-adjustments` 的 SLOT 占位符。

## SLOT 填充表

| SLOT | 填充值 |
|---|---|
| `{ENTITY_LABEL}` | **投资管理类** |
| `{ENTITY_ALIAS}` | **项目公司SPV** |
| `{HAS_WELFARE_PAYABLE}` | **有**（2211-02 福利费用） |
| `{HAS_MANAGEMENT_EXPENSE}` | **有**（6602 管理费用，含约 50 个明细子科目） |
| `{ADJUSTMENT_BS_IMPACT}` | **其他非流动资产（1483-1484 净额）等额增加** |
| `{ADJUSTMENT_IS_IMPACT}` | **管理费用恢复为 0**（已全部结转至合同资产），净利润相应变化 |

## SPV 特有调整注意事项

### 2211 应付职工薪酬子科目

SPV 的 2211 有约 19 个子科目，其中 2211-02 为福利费用。调整前需确认该子科目是否存在借方余额。

### 6602 管理费用

SPV 的管理费用有约 50 个明细子科目。调整 1（2211-02 → 6602）和调整 2（6602 → 1483）是连锁的——先做调整 1，再做调整 2。

### 调整对净利润的影响

SPV 有完整的所得税核算（6801），调整后：
- 管理费用变化 → 利润总额变化 → 所得税费用变化 → 净利润变化
- 验证：调整后净利润应接近 4105-14 净发生额

### 已验证案例

2026M05 某项目公司：调整前净利润显示为 86 万元（错误取 4105 余额），应用调整后恢复为 31 万元（正确取 4105-14 净发生额）。

## 自检清单

1. [ ] 是否确认非季度末（非 3/6/9/12 月）？
2. [ ] 2211-02 是否有借方余额？
3. [ ] 6602 结转金额是否含 2211-02 转入部分？
4. [ ] 调整后 1483/1484 净额是否正确增加？

## 免责声明

本规则基于 SPV 项目公司 2026M05 实际调整经验。
