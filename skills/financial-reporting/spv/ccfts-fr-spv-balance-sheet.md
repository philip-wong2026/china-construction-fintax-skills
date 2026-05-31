---
name: ccfts-fr-spv-balance-sheet
description: >
  SPV（投资管理类，Type A）资产负债表编制规则。填充 ccfts-fr-all-balance-sheet 的 SLOT。
  触发条件：SPV/投资管理类/项目公司的资产负债表编制。
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
  - ccfts-fr-all-balance-sheet
is_base: false
fills_slots_for: ccfts-fr-all-balance-sheet
slots: []
triggers:
  - SPV资产负债表
  - 投资管理类资产负债表
  - 项目公司资产负债表
---

# SPV（投资管理类/Type A）资产负债表规则

> 填充 `ccfts-fr-all-balance-sheet` 的 SLOT 占位符。

## SLOT 填充表

| SLOT | 填充值 |
|---|---|
| `{ENTITY_LABEL}` | **投资管理类** |
| `{ENTITY_ALIAS}` | **项目公司SPV** |
| `{BS_ROUNDING_MODE}` | **ROUND_HALF_UP** |
| `{COMPONENT_ROUNDING_MODE}` | **ROUND_HALF_UP** |
| `{CONTRACT_ASSET_CALC}` | **Σ ROUND(1483 各子行) − Σ ROUND(1484 各子行)**（组件级 ROUND_HALF_UP 后相减） |
| `{OTHER_PAYABLES_CALC}` | **倒推：负债合计 − 应交税费(2221) − 应付职工薪酬(2211)**（不直接取 2241） |
| `{HAS_CONTRACT_LIABILITIES}` | **无** |
| `{HAS_LONG_TERM_PAYABLE}` | **无**（非流动负债通常为 0） |
| `{HAS_ACCOUNTS_PAYABLE}` | **无**（填 0） |
| `{EQUITY_STRUCTURE_DESC}` | **正常权益结构**（实收资本+资本公积+盈余公积+未分配利润） |
| `{HAS_EQUITY_ACCOUNTS}` | **有**（4001/4002/4101/4105-14） |
| `{BALANCE_CHECK_FORMULA}` | **资产总计 ≈ 负债合计 + 实收资本 + 资本公积 + 盈余公积 + 未分配利润**（允许 ±1 万元取整噪音） |

## SPV 特有规则

### 其他应付款：倒推法（关键）

SPV 的 2241 其他应付款**绝对不能直接取数**：

```
其他应付款 = 负债合计 − 应交税费(2221) − 应付职工薪酬(2211)
```

**原因**：直接取 2241 期末余额在临界值（末五位 X5000 元）时会产生 ±1 万元差异。
Q4 2025 验证确认：2241 期末余额 265000 元恰在 0.5 万元临界点，倒推结果与实际快报完全一致。

### 货币资金：区分财务公司

SPV 的 1002 子科目需区分：
- 内部财务公司账户
- 外部金融机构账户

各子行分别 ROUND_HALF_UP 后汇总。快报中"其中：内部财务公司"和"其中：外部金融机构"分别填列。

### 完整权益结构

| 快报项目 | 科目 | 计算 |
|---|---|---|
| 实收资本 | 4001 | ROUND(4001 期末贷方余额) |
| 资本公积 | 4002 | ROUND(4002 期末贷方余额) |
| 盈余公积 | 4101 | ROUND(4101 期末贷方余额) |
| 未分配利润 | 4105-14 | ROUND(4105-14 期末贷方净额) |
| **权益合计** | — | 以上各项合计 |

### 平衡验证

```
资产总计 ≈ 负债合计 + 权益合计
```

允许 ±1 万元取整噪音。若差异 > ±1，优先排查：
1. 1483/1484 组件级取整是否正确
2. 其他应付款是否使用了倒推法
3. 固定资产是否分项取整

## 自检清单

1. [ ] 货币资金是否区分财务公司/外部金融机构？
2. [ ] 1483/1484 是否为组件级 ROUND_HALF_UP 后相减？
3. [ ] 其他应付款是否使用倒推法（不直接取 2241）？
4. [ ] 权益是否完整（4001/4002/4101/4105-14）？
5. [ ] 资产 = 负债 + 权益？（允许 ±1 噪音）

## 免责声明

本规则基于已验证的 SPV 项目公司 Q4 2025 资产负债表反推。
