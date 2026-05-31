---
name: ccfts-fr-all-balance-sheet
description: >
  中国施工企业资产负债表（资产负债指标表）编制规则——通用工作流基础（Base + SLOT 模式）。
  涵盖资产侧/负债侧/权益侧映射、净额计算、平衡验证。
  适用所有组织层级。触发条件：用户询问"资产负债表""资产负债""balance sheet""B/S"等。
version: 0.2
jurisdiction: CN
tax_year: 2025
category: financial-reporting
domains: [fr]
quality_tier: research-verified
verified_by: pending
entity_levels: [all]
enterprise_scales: [large-soe]
depends_on:
  - ccfts-workflow-base
  - ccfts-fr-all-entity-type-rules
references:
  - ccfts-intel-mof-cas33-consolidation
is_base: true
slots:
  - ENTITY_LABEL
  - ENTITY_ALIAS
  - BS_ROUNDING_MODE
  - COMPONENT_ROUNDING_MODE
  - CONTRACT_ASSET_CALC
  - OTHER_PAYABLES_CALC
  - HAS_CONTRACT_LIABILITIES
  - HAS_LONG_TERM_PAYABLE
  - HAS_ACCOUNTS_PAYABLE
  - EQUITY_STRUCTURE_DESC
  - HAS_EQUITY_ACCOUNTS
  - BALANCE_CHECK_FORMULA
triggers:
  - 资产负债表
  - 资产负债
  - balance sheet
  - B/S
  - 资产总计
  - 负债合计
---

# 施工企业资产负债表编制规则（Base）

> **SLOT 说明**：本文件为通用工作流基础。其中 `{SLOT_XXX}` 为命名占位符，
> 由各组织层级的覆盖文件填充为具体值。

## 快速参考

| 项目 | {ENTITY_LABEL}（{ENTITY_ALIAS}） |
|---|---|
| 取整模式 | {BS_ROUNDING_MODE} |
| 合同资产(1483/1484) | {CONTRACT_ASSET_CALC} |
| 其他应付款 | {OTHER_PAYABLES_CALC} |
| 合同负债 | {HAS_CONTRACT_LIABILITIES} |
| 长期应付款 | {HAS_LONG_TERM_PAYABLE} |
| 应付账款 | {HAS_ACCOUNTS_PAYABLE} |
| 权益合计 | {EQUITY_STRUCTURE_DESC} |
| 平衡验证 | {BALANCE_CHECK_FORMULA} |

## 一、资产侧映射

### 通用科目（所有主体）

| 快报项目 | 公式 | 注意 |
|---|---|---|
| 货币资金 | Σ {COMPONENT_ROUNDING_MODE}(1002 各子行) | 各子科目分别取整后汇总 |
| 预付账款 | {COMPONENT_ROUNDING_MODE}(1123 期末借方余额) | |
| 其他应收款 | {COMPONENT_ROUNDING_MODE}(1221) − {COMPONENT_ROUNDING_MODE}(1231-02) | 净额 = 账面 − 坏账准备 |
| 流动资产合计 | 以上各项合计 | |
| 合同资产 | {CONTRACT_ASSET_CALC} | 组件级分别取整后相减 |
| 其他非流动资产 | 合同资产 + {COMPONENT_ROUNDING_MODE}(1531净) | |
| 固定资产净额 | {COMPONENT_ROUNDING_MODE}(1601) − {COMPONENT_ROUNDING_MODE}(1602) | 原值 − 折旧，分项取整后相减 |
| 递延所得税资产 | {COMPONENT_ROUNDING_MODE}(1811 期末借方余额) | |
| 非流动资产合计 | 以上非流动项目合计 | |
| **资产总计** | 流动 + 非流动 | |

## 二、负债侧映射

### 通用科目（所有主体）

| 快报项目 | 公式 | 注意 |
|---|---|---|
| 应付职工薪酬 | {COMPONENT_ROUNDING_MODE}(2211 期末贷方余额) | |
| 应交税费 | {COMPONENT_ROUNDING_MODE}(2221 期末净额) | |

### 层级特定科目

| 快报项目 | 公式 | 适用 |
|---|---|---|
| 应付账款 | {COMPONENT_ROUNDING_MODE}(2202) − {COMPONENT_ROUNDING_MODE}(1123) | {HAS_ACCOUNTS_PAYABLE} |
| 合同负债 | {COMPONENT_ROUNDING_MODE}(5801 贷方余额) | {HAS_CONTRACT_LIABILITIES} |
| 其他应付款 | {OTHER_PAYABLES_CALC} | 所有 |
| 其他流动负债 | {COMPONENT_ROUNDING_MODE}(1126) | 如有 1126 |
| 长期应付款 | {COMPONENT_ROUNDING_MODE}(2701) | {HAS_LONG_TERM_PAYABLE} |
| 流动负债合计 | 以上各项合计 | 所有 |
| 非流动负债 | 长期应付款（如有） | 所有 |
| **负债合计** | 流动 + 非流动 | 所有 |

## 三、权益侧映射

### 权益科目

| 快报项目 | 科目 | 取数口径 | 适用 |
|---|---|---|---|
| 实收资本 | 4001 | 期末贷方余额 | {HAS_EQUITY_ACCOUNTS} |
| 资本公积 | 4002 | 期末贷方余额 | {HAS_EQUITY_ACCOUNTS} |
| 盈余公积 | 4101 | 期末贷方余额 | {HAS_EQUITY_ACCOUNTS} |
| 未分配利润 | 4105-14 | 期末贷方净额 | {HAS_EQUITY_ACCOUNTS} |
| **权益合计** | 以上合计 | — | {EQUITY_STRUCTURE_DESC} |

## 四、平衡验证（所有主体通用）

```
资产总计 = 负债合计 + 所有者权益合计
```

| 主体 | 验证方式 |
|---|---|
| {ENTITY_LABEL} | {BALANCE_CHECK_FORMULA} |

若不满足平衡，排查顺序：
1. 1483/1484 是否做了组件级分项取整？
2. 其他应付款是否正确使用了本层级的方法？
3. 取整模式是否正确（{BS_ROUNDING_MODE}）？
4. 固定资产是否为 1601 − 1602 分项取整后相减？

## 五、自检清单

1. [ ] 货币资金是否为各子行分别取整后汇总？
2. [ ] 1483/1484 是否为组件级取整（{CONTRACT_ASSET_CALC}）？
3. [ ] 其他应付款取数方法是否正确（{OTHER_PAYABLES_CALC}）？
4. [ ] 资产负债表所有行是否使用了正确的取整模式（{BS_ROUNDING_MODE}）？
5. [ ] 固定资产是否为 1601 − 1602 分项取整后相减？
6. [ ] 资产 = 负债 + 权益？（允许 ±1 取整噪音）
7. [ ] 是否正确加载了对应组织层级的 SLOT 覆盖文件？

## 六、SLOT 填充参考

| SLOT | 含义 | 由层级覆盖文件定义 |
|---|---|---|
| `{ENTITY_LABEL}` | 主体中文全称 | 投资管理类 / 施工总承包类 |
| `{ENTITY_ALIAS}` | 主体中文简称 | 项目公司SPV / 总包部/项目部 |
| `{BS_ROUNDING_MODE}` | 资产负债表取整 | ROUND_HALF_UP / ROUND_DOWN |
| `{COMPONENT_ROUNDING_MODE}` | 组件级取整函数 | ROUND_HALF_UP / ROUND_DOWN |
| `{CONTRACT_ASSET_CALC}` | 合同资产净额计算 | 组件级分别取整后相减 |
| `{OTHER_PAYABLES_CALC}` | 其他应付款计算方式 | 倒推 / 直接取数 |
| `{HAS_CONTRACT_LIABILITIES}` | 是否有合同负债(5801) | 无 / 有 |
| `{HAS_LONG_TERM_PAYABLE}` | 是否有长期应付款(2701) | 无 / 有 |
| `{HAS_ACCOUNTS_PAYABLE}` | 是否有应付账款(2202) | 无（填 0）/ 有 |
| `{EQUITY_STRUCTURE_DESC}` | 权益结构描述 | 正常权益 / ≈ 0 |
| `{HAS_EQUITY_ACCOUNTS}` | 是否有权益类科目 | 有（4001/4002/4101/4105-14）/ 无 |
| `{BALANCE_CHECK_FORMULA}` | 平衡验证公式 | 资产 = 负债 + 权益 / 资产 ≈ 负债 |

## 七、参考材料

- 已验证的投资管理类项目公司 Q4 2025 资产负债表（完美平衡）
- 已验证的施工总承包类总包部 M12 2025 资产负债表（资产 = 负债 = 16863 万元）
- 本文件为 Base 层，对应覆盖文件：
  - `ccfts-fr-spv-balance-sheet` — SPV（投资管理类）
  - `ccfts-fr-project-unit-balance-sheet` — 项目部/总包部（施工总承包类）

## 免责声明

本规则基于已验证企业实际快报数据反推。不同企业的科目结构和快报系统行为可能有差异。
