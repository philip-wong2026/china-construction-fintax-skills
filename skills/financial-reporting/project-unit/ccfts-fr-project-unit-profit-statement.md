---
name: ccfts-fr-project-unit-profit-statement
description: >
  项目部/总包部（施工总承包类，Type B）利润表编制规则。填充 ccfts-fr-all-profit-statement 的 SLOT。
  触发条件：总包部/项目部/施工总承包类的利润表编制。
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
  - ccfts-fr-all-profit-statement
is_base: false
fills_slots_for: ccfts-fr-all-profit-statement
slots: []
triggers:
  - 总包部利润表
  - 项目部利润表
  - 施工总承包利润表
---

# 项目部/总包部（施工总承包类/Type B）利润表规则

> 填充 `ccfts-fr-all-profit-statement` 的 SLOT 占位符。

## SLOT 填充表

| SLOT | 填充值 |
|---|---|
| `{ENTITY_LABEL}` | **施工总承包类** |
| `{ENTITY_ALIAS}` | **总包部/项目部** |
| `{INCOME_ACCOUNT}` | **6001** |
| `{INCOME_NAME}` | **主营业务收入** |
| `{COST_ACCOUNT}` | **6401** |
| `{COST_NAME}` | **主营业务成本** |
| `{HAS_INVESTMENT_INCOME}` | **通常无** |
| `{HAS_OTHER_INCOME}` | **通常无** |
| `{HAS_INCOME_TAX}` | **通常无**（总包部不单独核算所得税） |
| `{IS_ROUNDING_MODE}` | **ROUND_HALF_UP** |
| `{NET_PROFIT_FORMULA}` | **= 利润总额** |
| `{NET_PROFIT_VERIFICATION}` | **净利润 = 利润总额**（无所得税，直接一致） |

## 项目部/总包部特有规则

### 简化损益链路

总包部作为内部管理单位，损益链路比 SPV 短：

```
营业总收入(6001) − 营业成本(6401) − 税金及附加(6403) − 财务费用(6603)
  − 信用减值损失(6702)
  = 利润总额 = 净利润
```

无投资收益、其他收益、所得税费用科目。

### 净利润 = 利润总额

总包部不单独核算所得税（无 6801 科目），净利润直接等于利润总额。这是与 SPV 的关键差异。

### 信用减值损失可为负

Type B 总包部的 6702 信用减值损失可能为负（当年冲回大于计提时），直接以净额填列。

### 营业收入明细

6001 主营业务收入中，基建建设（城轨等）填同值。

### 取整：利润表用 ROUND_HALF_UP

虽然资产负债表用 ROUND_DOWN，但利润表仍使用 ROUND_HALF_UP。两者独立，不互相影响。

## 自检清单

1. [ ] 营业收入是否正确使用 6001 贷方发生额？
2. [ ] 营业成本是否正确使用 6401 借方发生额？
3. [ ] 净利润是否 = 利润总额（无所得税）？
4. [ ] 信用减值损失是否为净额（可为负数）？
5. [ ] 利润表是否使用 ROUND_HALF_UP（非 ROUND_DOWN）？
6. [ ] 利息收入是否已取反为正数？

## 免责声明

本规则基于已验证的总包部 M12 2025 利润表反推。
