---
name: ccfts-fr-project-unit-period-end-adjustments
description: >
  项目部/总包部（施工总承包类，Type B）期末调整规则。填充 ccfts-fr-all-period-end-adjustments 的 SLOT。
  触发条件：总包部/项目部非季度末快报编制。
version: 0.2
jurisdiction: CN
tax_year: 2025
category: financial-reporting
domains: [fr]
quality_tier: research-verified
verified_by: pending
entity_levels: [project-unit]
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
  - 总包部期末调整
  - 项目部期末调整
---

# 项目部/总包部（施工总承包类/Type B）期末调整

> 填充 `ccfts-fr-all-period-end-adjustments` 的 SLOT 占位符。

## SLOT 填充表

| SLOT | 填充值 |
|---|---|
| `{ENTITY_LABEL}` | **施工总承包类** |
| `{ENTITY_ALIAS}` | **总包部/项目部** |
| `{HAS_WELFARE_PAYABLE}` | **有**（2211-02 福利费用，总包部应付职工薪酬子科目较多） |
| `{HAS_MANAGEMENT_EXPENSE}` | **有**（6602 管理费用） |
| `{ADJUSTMENT_BS_IMPACT}` | **其他非流动资产（ROUND_DOWN(1483) − ROUND_DOWN(1484)）等额增加** |
| `{ADJUSTMENT_IS_IMPACT}` | **管理费用恢复为 0**（已全部结转至合同资产），净利润 = 利润总额同步调整 |

## 项目部/总包部特有调整注意事项

### 取整模式影响

总包部 BS 使用 ROUND_DOWN，调整后的 1483/1484 增量也需使用 ROUND_DOWN：
```
调整后 1483 = ROUND_DOWN(原1483 + 调整金额)
调整后 1484 = ROUND_DOWN(原1484)
```

### 调整对净利润的影响

总包部无所得税核算（无 6801 科目），调整后：
- 管理费用变化 → 利润总额变化 → 净利润同步变化
- 净利润始终 = 利润总额

### 合同履约成本 vs 管理费用

总包部有 5601（合同履约成本），调整逻辑假设未结转福利费用全部计入管理费用（6602）。
如果企业将部分福利费用计入合同履约成本（5601），调整方式不同——此时需用户确认分配比例。

### 银行重分类

总包部的银行重分类涉及 1002 和 1221（其他应收款—资金集中管理款），与内部资金归集制度相关。
每次使用须用户显式确认。

## 自检清单

1. [ ] 是否确认非季度末（非 3/6/9/12 月）？
2. [ ] 调整后的 1483/1484 是否使用了 ROUND_DOWN？
3. [ ] 是否确认福利费用全部计入 6602（非 5601）？
4. [ ] 净利润是否仍 = 利润总额（调整后）？

## 免责声明

本规则基于总包部有限期间的实际操作经验。未结转福利费用计入管理费用的假设可能不适用所有项目部。
