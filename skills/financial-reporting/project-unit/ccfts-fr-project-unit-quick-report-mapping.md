---
name: ccfts-fr-project-unit-quick-report-mapping
description: >
  项目部/总包部（施工总承包类，Type B）快报映射流程。填充 ccfts-fr-all-quick-report-mapping 的 SLOT。
  触发条件：总包部/项目部/施工总承包类的快报编制。
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
  - ccfts-fr-all-quick-report-mapping
is_base: false
fills_slots_for: ccfts-fr-all-quick-report-mapping
slots: []
triggers:
  - 总包部快报
  - 项目部快报
  - 施工总承包快报
---

# 项目部/总包部（施工总承包类/Type B）快报映射

> 填充 `ccfts-fr-all-quick-report-mapping` 的 SLOT 占位符。

## SLOT 填充表

| SLOT | 填充值 |
|---|---|
| `{ENTITY_LABEL}` | **施工总承包类** |
| `{ENTITY_ALIAS}` | **总包部/项目部** |
| `{ENTITY_PROFIT_SKILL}` | `ccfts-fr-project-unit-profit-statement` |
| `{ENTITY_BALANCE_SHEET_SKILL}` | `ccfts-fr-project-unit-balance-sheet` |
| `{ENTITY_TYPE_RULES_SKILL}` | `ccfts-fr-project-unit-entity-type-rules` |
| `{ENTITY_CHART_OF_ACCOUNTS_SKILL}` | `ccfts-acct-project-unit-chart-of-accounts` |
| `{ENTITY_ROUNDING_SKILL}` | `ccfts-fr-project-unit-rounding-rules` |
| `{BS_ROUNDING_MODE}` | **ROUND_DOWN** |
| `{IS_ROUNDING_MODE}` | **ROUND_HALF_UP** |

## 项目部/总包部特有映射注意事项

### 利润表映射
- 营业总收入 = 6001 贷方发生额
- 营业成本 = 6401 借方发生额
- 无投资收益、其他收益、所得税费用
- 净利润 = 利润总额（无所得税）
- 信用减值损失可为负（冲回大于计提时）

### 资产负债表映射
- 全部资产/负债行使用 ROUND_DOWN
- 应付账款 = ROUND_DOWN(2202) − ROUND_DOWN(1123)
- 合同负债 = ROUND_DOWN(5801 贷方余额)
- 其他应付款 = ROUND_DOWN(2241-01) + ROUND_DOWN(3001)
- 其他流动负债 = ROUND_DOWN(1126)
- 长期应付款 = ROUND_DOWN(2701)
- 权益合计 ≈ 0

### 不填充项（总包部特有）
- 权益类行（实收资本/资本公积/盈余公积/未分配利润，填 0 或空白）
- 投资收益、其他收益、所得税费用（无对应科目）

## 自检清单

1. [ ] 总包部利润表是否正确加载 ccfts-fr-project-unit-profit-statement？
2. [ ] 总包部资产负债表是否正确加载 ccfts-fr-project-unit-balance-sheet？
3. [ ] BS 所有行是否使用 ROUND_DOWN？
4. [ ] 权益是否 ≈ 0？
5. [ ] 应付账款是否扣除了预付账款(1123)？

## 免责声明

本规则基于已验证的总包部 M12 2025 实际快报编制反推。
