---
name: ccfts-fr-spv-profit-statement
description: >
  SPV（投资管理类，Type A）利润表编制规则。填充 ccfts-fr-all-profit-statement 的 SLOT。
  触发条件：SPV/投资管理类/项目公司的利润表编制。
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
  - ccfts-fr-all-profit-statement
is_base: false
fills_slots_for: ccfts-fr-all-profit-statement
slots: []
triggers:
  - SPV利润表
  - 投资管理类利润表
  - 项目公司利润表
---

# SPV（投资管理类/Type A）利润表规则

> 填充 `ccfts-fr-all-profit-statement` 的 SLOT 占位符。

## SLOT 填充表

| SLOT | 填充值 |
|---|---|
| `{ENTITY_LABEL}` | **投资管理类** |
| `{ENTITY_ALIAS}` | **项目公司SPV** |
| `{INCOME_ACCOUNT}` | **6051** |
| `{INCOME_NAME}` | **其他业务收入** |
| `{COST_ACCOUNT}` | **6402** |
| `{COST_NAME}` | **其他业务成本** |
| `{HAS_INVESTMENT_INCOME}` | **有**（6111 贷方发生额） |
| `{HAS_OTHER_INCOME}` | **有**（6605 贷方发生额） |
| `{HAS_INCOME_TAX}` | **有**（6801 借方发生额） |
| `{IS_ROUNDING_MODE}` | **ROUND_HALF_UP** |
| `{NET_PROFIT_FORMULA}` | **利润总额 − 所得税费用** |
| `{NET_PROFIT_VERIFICATION}` | **取 4105-14 本期贷方净发生额（credit − debit），与 利润总额 − 所得税 交叉验证** |

## SPV 特有规则

### 净利润取数（最关键）

**正确**：取 4105-14 本期贷方净发生额（credit − debit）
**错误**：取 4105 期末余额

原因：4105 期末余额包含以前年度未分配利润和盈余公积转入，跨年度时严重错误。

验证：`净利润 ≈ 利润总额 − 所得税费用`，且 `≈ 4105-14 净发生额`。

### SPV 完整的损益链路

SPV 有完整的损益科目体系（6111 投资收益、6605 其他收益、6801 所得税费用），利润计算链比总包部更长：

```
营业总收入(6051) − 营业成本(6402) − 税金及附加(6403) − 财务费用(6603)
  + 其他收益(6605) + 投资收益(6111) − 资产减值损失(6701) − 信用减值损失(6702)
  = 利润总额 − 所得税费用(6801) = 净利润
```

### 资产减值损失

SPV 同时有 6701（资产减值损失）和 6702（信用减值损失），分别填列。

## 自检清单

1. [ ] 营业收入是否正确使用 6051 贷方发生额？
2. [ ] 净利润是否取自 4105-14 净发生额而非 4105 余额？
3. [ ] 所得税费用是否正确填列（6801 借方发生额）？
4. [ ] 利息收入是否已取反为正数？
5. [ ] 投资收益、其他收益是否已包含？

## 免责声明

本规则基于已验证的 SPV 项目公司 Q4 2025 利润表反推。
