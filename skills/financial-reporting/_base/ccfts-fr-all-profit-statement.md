---
name: ccfts-fr-all-profit-statement
description: >
  中国施工企业利润表（利润指标表）编制规则——通用工作流基础（Base + SLOT 模式）。
  定义营业总收入→营业利润→利润总额→净利润的完整计算链。
  适用所有组织层级。触发条件：用户询问"利润表""损益表""P&L""净利润""营业收入"等。
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
  - ccfts-intel-mof-cas14-revenue
is_base: true
slots:
  - ENTITY_LABEL
  - ENTITY_ALIAS
  - INCOME_ACCOUNT
  - INCOME_NAME
  - COST_ACCOUNT
  - COST_NAME
  - HAS_INVESTMENT_INCOME
  - HAS_OTHER_INCOME
  - HAS_INCOME_TAX
  - IS_ROUNDING_MODE
  - NET_PROFIT_FORMULA
  - NET_PROFIT_VERIFICATION
triggers:
  - 利润表
  - 利润指标
  - 损益表
  - P&L
  - profit
  - 净利润
  - 营业收入
---

# 施工企业利润表编制规则（Base）

> **SLOT 说明**：本文件为通用工作流基础。其中 `{SLOT_XXX}` 为命名占位符，
> 由各组织层级的覆盖文件填充为具体值。

## 快速参考

| 项目 | {ENTITY_LABEL}（{ENTITY_ALIAS}） |
|---|---|
| 营业收入科目 | {INCOME_ACCOUNT} {INCOME_NAME} |
| 营业成本科目 | {COST_ACCOUNT} {COST_NAME} |
| 投资收益 | {HAS_INVESTMENT_INCOME} |
| 其他收益 | {HAS_OTHER_INCOME} |
| 所得税费用 | {HAS_INCOME_TAX} |
| 净利润公式 | {NET_PROFIT_FORMULA} |
| 净利润验证 | {NET_PROFIT_VERIFICATION} |
| 取整模式 | {IS_ROUNDING_MODE} |

## 一、利润计算链（通用框架）

```
                    营业收入科目 贷方发生额
  营业总收入      = {INCOME_ACCOUNT}
  —
                    营业成本科目 借方发生额
  营业成本        = {COST_ACCOUNT}
  —
  税金及附加      = 6403 借方发生额
  —
  财务费用        = 6603 借方净发生额（借—贷）
                    → 可为负数（利息收入 > 利息支出时）
  +
  其他收益        = 6605 贷方发生额（{HAS_OTHER_INCOME}）
  +
  投资收益        = 6111 贷方发生额（{HAS_INVESTMENT_INCOME}）
  —
  资产减值损失    = 6701 借方净发生额
  —
  信用减值损失    = 6702 借方净发生额
                    → Type B: 可为负（贷方发生额 > 借方时）
  =
  营业利润
  =
  利润总额        （无营业外收支时）
  —
  所得税费用      = 6801 借方发生额（{HAS_INCOME_TAX}）
  =
  净利润
```

## 二、科目映射详表

| 快报项目 | 科目 | 取数口径 | 符号处理 | 适用主体 |
|---|---|---|---|---|
| 营业总收入 | {INCOME_ACCOUNT} | 贷方发生额 | 正数 | {ENTITY_ALIAS} |
| 其中：主营业务收入 | 6001 | 贷方发生额 | 正数 | Type B |
| 营业成本 | {COST_ACCOUNT} | 借方发生额 | 正数 | {ENTITY_ALIAS} |
| 税金及附加 | 6403 | 借方发生额 | 正数 | 所有 |
| 财务费用 | 6603 | 借方净发生额（借-贷） | 可为负 | 所有 |
| 利息支出 | 6603-01 | 借方发生额 | 正数 | 所有 |
| 利息收入 | 6603-02 | 贷方发生额 | **取反**（正数填列） | 所有 |
| 其他收益 | 6605 | 贷方发生额 | 正数 | {HAS_OTHER_INCOME} |
| 投资收益 | 6111 | 贷方发生额 | 正数 | {HAS_INVESTMENT_INCOME} |
| 资产减值损失 | 6701 | 借方净发生额 | 利润指标表：正数 | 所有 |
| 信用减值损失 | 6702 | 借方净发生额 | Type B 可为负 | 所有 |
| 所得税费用 | 6801 | 借方发生额 | 正数 | {HAS_INCOME_TAX} |
| 利润总额 | 计算 | — | 正数 | 所有 |
| 净利润 | 计算 | — | 正数 | 所有 |

## 三、关键注意事项（所有主体适用）

### 1. 利息收入符号

6603-02 利息收入在科目余额表中通常为贷方发生额。填快报时须**取反为正数**。

### 2. 资产减值损失双重列示

| Sheet | 列示方式 | 符号 |
|---|---|---|
| 利润指标表 | 以正数填列 | + |
| 资产负债指标表 / 主表 | 以损失填列 | − |

### 3. 财务费用可为负

当利息收入（6603-02）大于利息支出（6603-01）时，净额为负数。快报中直接以负数列示。

## 四、业务板块分配（所有主体通用）

利润指标表中的"业务板块"sheet 的利润分配：

| 行 | 内容 | 取值 |
|---|---|---|
| 基建建设行 | 利润总额 | = 利润总额 |
| 市政行 | 利润总额 | = 利润总额 |
| 营业收入/营业成本明细行 | — | 不填（保持空白） |

**不按标签模糊匹配，按固定行号写入**。

## 五、非季度/非年末月处理

非季度末月（1/2/4/5/7/8/10/11 月）的损益类科目可能未完全结转。需结合 `ccfts-period-end-adjustments` 判断是否需要补结转调整。

## 六、自检清单

1. [ ] 营业收入是否使用了正确的科目（{INCOME_ACCOUNT}）？
2. [ ] 营业成本是否使用了正确的科目（{COST_ACCOUNT}）？
3. [ ] 净利润取数口径是否正确（{NET_PROFIT_VERIFICATION}）？
4. [ ] 利息收入是否已取反为正数？
5. [ ] 资产减值损失在利润指标表是否为正数？
6. [ ] 业务板块分配是否正确？（基建建设 + 市政）
7. [ ] D 列与 G 列逻辑是否正确？（非年末月 vs 年末月）
8. [ ] 是否正确加载了对应组织层级的 SLOT 覆盖文件？

## 七、SLOT 填充参考

| SLOT | 含义 | 由层级覆盖文件定义 |
|---|---|---|
| `{ENTITY_LABEL}` | 主体中文全称 | 投资管理类 / 施工总承包类 |
| `{ENTITY_ALIAS}` | 主体中文简称 | 项目公司SPV / 总包部/项目部 |
| `{INCOME_ACCOUNT}` | 营业收入科目编号 | 6051 / 6001 |
| `{INCOME_NAME}` | 营业收入科目名称 | 其他业务收入 / 主营业务收入 |
| `{COST_ACCOUNT}` | 营业成本科目编号 | 6402 / 6401 |
| `{COST_NAME}` | 营业成本科目名称 | 其他业务成本 / 主营业务成本 |
| `{HAS_INVESTMENT_INCOME}` | 是否有投资收益 | 有 / 通常无 |
| `{HAS_OTHER_INCOME}` | 是否有其他收益 | 有 / 通常无 |
| `{HAS_INCOME_TAX}` | 是否有所得税费用 | 有 / 通常无 |
| `{IS_ROUNDING_MODE}` | 利润表取整模式 | ROUND_HALF_UP |
| `{NET_PROFIT_FORMULA}` | 净利润公式 | 利润总额 − 所得税 / = 利润总额 |
| `{NET_PROFIT_VERIFICATION}` | 净利润验证方法 | 4105-14 净发生额 / 利润总额一致 |

## 八、参考材料

- 已验证的投资管理类项目公司 Q4 2025 利润表（99.2% 匹配率）
- 已验证的施工总承包类总包部 M12 2025 利润表
- 本文件为 Base 层，对应覆盖文件：
  - `ccfts-fr-spv-profit-statement` — SPV（投资管理类）
  - `ccfts-fr-project-unit-profit-statement` — 项目部/总包部（施工总承包类）

## 免责声明

本规则基于已验证企业实际快报数据反推。利润表取数口径可能因企业会计政策差异而不同。
