---
name: ccfts-fr-spv-quick-report-mapping
description: >
  SPV（投资管理类，Type A）快报映射流程。填充 ccfts-fr-all-quick-report-mapping 的 SLOT。
  触发条件：SPV/投资管理类/项目公司的快报编制。
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
  - ccfts-fr-all-quick-report-mapping
is_base: false
fills_slots_for: ccfts-fr-all-quick-report-mapping
slots: []
triggers:
  - SPV快报
  - 投资管理类快报
  - 项目公司快报
---

# SPV（投资管理类/Type A）快报映射

> 填充 `ccfts-fr-all-quick-report-mapping` 的 SLOT 占位符。

## SLOT 填充表

| SLOT | 填充值 |
|---|---|
| `{ENTITY_LABEL}` | **投资管理类** |
| `{ENTITY_ALIAS}` | **项目公司SPV** |
| `{ENTITY_PROFIT_SKILL}` | `ccfts-fr-spv-profit-statement` |
| `{ENTITY_BALANCE_SHEET_SKILL}` | `ccfts-fr-spv-balance-sheet` |
| `{ENTITY_TYPE_RULES_SKILL}` | `ccfts-fr-spv-entity-type-rules` |
| `{ENTITY_CHART_OF_ACCOUNTS_SKILL}` | `ccfts-acct-spv-chart-of-accounts` |
| `{ENTITY_ROUNDING_SKILL}` | `ccfts-fr-spv-rounding-rules` |
| `{BS_ROUNDING_MODE}` | **ROUND_HALF_UP** |
| `{IS_ROUNDING_MODE}` | **ROUND_HALF_UP** |

## SPV 特有映射注意事项

### 利润表映射
- 营业总收入 = 6051 贷方发生额
- 营业成本 = 6402 借方发生额
- 含投资收益(6111)、其他收益(6605)、所得税费用(6801)
- 净利润 = 利润总额 − 所得税费用

### 资产负债表映射
- 全局 ROUND_HALF_UP
- 其他应付款使用倒推法（负债合计 − 税费 − 薪酬）
- 有完整权益结构（4001/4002/4101/4105-14）
- 货币资金区分内部财务公司 vs 外部金融机构

### 不填充项（SPV 特有）
- 合同负债（SPV 无 5801）
- 应付账款（SPV 无 2202，填 0）
- 长期应付款（SPV 无 2701）

## 自检清单

1. [ ] SPV 利润表是否正确加载 ccfts-fr-spv-profit-statement？
2. [ ] SPV 资产负债表是否正确加载 ccfts-fr-spv-balance-sheet？
3. [ ] 其他应付款是否使用倒推法？
4. [ ] 净利润是否 = 利润总额 − 所得税？

## 免责声明

本规则基于已验证的 SPV 项目公司实际快报编制反推。
