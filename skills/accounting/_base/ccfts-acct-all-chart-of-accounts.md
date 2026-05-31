---
name: ccfts-acct-all-chart-of-accounts
description: >
  中国施工企业完整科目表——通用工作流基础（Base + SLOT 模式）。
  包含科目编号、名称、正常余额方向、财务报表分类。
  适用所有组织层级。触发条件：用户询问"科目表""科目编号""会计科目""chart of accounts"等。
version: 0.2
jurisdiction: CN
tax_year: 2025
category: accounting
domains: [acct]
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
  - HAS_CONTRACT_ACCOUNTS
  - HAS_AP
  - HAS_LTP
  - HAS_INTERNAL
  - HAS_PENDING_VAT
  - HAS_EQUITY
  - HAS_INVESTMENT_INCOME
  - HAS_OTHER_INCOME
  - HAS_INCOME_TAX
triggers:
  - 科目表
  - 科目编号
  - 会计科目
  - chart of accounts
  - COA
  - 1002
  - 1483
  - 4105
---

# 施工企业科目表（Base）

> **SLOT 说明**：本文件为通用工作流基础。其中 `{SLOT_XXX}` 为命名占位符，
> 由各组织层级的覆盖文件填充为具体值。

## 快速参考

| 项目 | {ENTITY_LABEL}（{ENTITY_ALIAS}） |
|---|---|
| 收入科目 | {INCOME_ACCOUNT} {INCOME_NAME} |
| 成本科目 | {COST_ACCOUNT} {COST_NAME} |
| 施工特有科目(58xx/56xx) | {HAS_CONTRACT_ACCOUNTS} |
| 应付账款(2202) | {HAS_AP} |
| 长期应付款(2701) | {HAS_LTP} |
| 内部往来(3001) | {HAS_INTERNAL} |
| 待结算进项税额(1126) | {HAS_PENDING_VAT} |
| 权益类科目(4xxx) | {HAS_EQUITY} |
| 投资收益(6111) | {HAS_INVESTMENT_INCOME} |
| 其他收益(6605) | {HAS_OTHER_INCOME} |
| 所得税费用(6801) | {HAS_INCOME_TAX} |

## 一、科目编码体系（中国企业会计准则，通用）

```
1xxx — 资产类
  1002 — 银行存款（含现金流量子科目）
  1123 — 预付账款
  1126 — 待结算进项税额（{HAS_PENDING_VAT}）
  1221 — 其他应收款
  1231 — 坏账准备
  1483 — 合同资产
  1484 — 合同资产减值准备
  1531 — 长期应收款
  1601 — 固定资产
  1602 — 累计折旧
  1811 — 递延所得税资产

2xxx — 负债类
  2202 — 应付账款（{HAS_AP}）
  2211 — 应付职工薪酬
  2221 — 应交税费
  2241 — 其他应付款
  2701 — 长期应付款（{HAS_LTP}）

3xxx — 内部往来类
  3001 — 内部往来（{HAS_INTERNAL}）

4xxx — 所有者权益类（{HAS_EQUITY}）
  4001 — 实收资本
  4002 — 资本公积
  4101 — 盈余公积
  4105 — 利润分配
     4105-14 — 未分配利润

5xxx — 施工/合同类科目（{HAS_CONTRACT_ACCOUNTS}）
  5601 — 合同履约成本
  5801 — 合同结算

6xxx — 损益类
  6001 — 主营业务收入（Type B）
  6051 — 其他业务收入（Type A）
  6111 — 投资收益（{HAS_INVESTMENT_INCOME}）
  6401 — 主营业务成本（Type B）
  6402 — 其他业务成本（Type A）
  6403 — 税金及附加
  6602 — 管理费用
  6603 — 财务费用
     6603-01 — 利息支出
     6603-02 — 利息收入
  6605 — 其他收益（{HAS_OTHER_INCOME}）
  6701 — 资产减值损失
  6702 — 信用减值损失
  6801 — 所得税费用（{HAS_INCOME_TAX}）
```

## 二、通用科目映射（所有主体共享）

### 资产侧

| 快报行 | 科目 | 取数口径 |
|---|---|---|
| 货币资金 | 1002 | 期末余额，各子科目分别取整后汇总 |
| 预付账款 | 1123 | 期末借方余额 |
| 其他应收款 | 1221 − 1231-02 | 净额，分别取整后相减 |
| 合同资产 | 1483 − 1484 | 净额，**分别取整后相减** |
| 其他非流动资产 | 1483 − 1484 + 1531 | 同上 + 1531净额 |
| 固定资产净额 | 1601 − 1602 | 原值减折旧，分项取整后相减 |
| 递延所得税资产 | 1811 | 期末借方余额 |

### 负债侧

| 快报行 | 科目 | 取数口径 |
|---|---|---|
| 应付职工薪酬 | 2211 | 期末贷方余额 |
| 应交税费 | 2221 | 期末净额 |

### 损益类

| 快报项目 | 科目 | 取数口径 |
|---|---|---|
| 税金及附加 | 6403 | 借方发生额 |
| 财务费用 | 6603 | 借方净发生额（借-贷），可为负 |
| 利息支出 | 6603-01 | 借方发生额 |
| 利息收入 | 6603-02 | 贷方发生额取反（正数填列） |
| 资产减值损失 | 6701 + 6702 | 利润指标表填正数 |
| 信用减值损失 | 6702 | 本年累计净额 |

## 三、层级特定科目映射

### 收入与成本

| 快报项目 | 科目 | 取数口径 | 适用 |
|---|---|---|---|
| 营业总收入 | {INCOME_ACCOUNT} | 贷方发生额 | {ENTITY_ALIAS} |
| 营业成本 | {COST_ACCOUNT} | 借方发生额 | {ENTITY_ALIAS} |

### 权益类

| 快报项目 | 科目 | 取数口径 | 适用 |
|---|---|---|---|
| 实收资本 | 4001 | 期末贷方余额 | {HAS_EQUITY} |
| 资本公积 | 4002 | 期末贷方余额 | {HAS_EQUITY} |
| 盈余公积 | 4101 | 期末贷方余额 | {HAS_EQUITY} |
| 未分配利润 | 4105-14 | 期末贷方净额 | {HAS_EQUITY} |

## 四、特殊科目处理说明（所有主体通用）

### 1483/1484 合同资产（最重要）

**错误做法**：ROUND(1483各子科目合计 − 1484各子科目合计)
**正确做法**：各子科目分别取整后相减

### 4105-14 未分配利润

必须取 `4105-14` 净额，不能取 `4105` 期末余额（含以前年度留存收益）。

### 6603 财务费用

当利息收入大于利息支出时，净额为负数。快报中以负数列示。

## 五、自检清单

1. [ ] 1483/1484 是否做了组件级分别取整？
2. [ ] 收入科目是否正确（{INCOME_ACCOUNT}）？
3. [ ] 成本科目是否正确（{COST_ACCOUNT}）？
4. [ ] 利息收入是否已取反（正数填列）？
5. [ ] 是否正确加载了对应组织层级的 SLOT 覆盖文件？

## 六、SLOT 填充参考

| SLOT | 含义 | 由层级覆盖文件定义 |
|---|---|---|
| `{ENTITY_LABEL}` | 主体中文全称 | 投资管理类 / 施工总承包类 |
| `{ENTITY_ALIAS}` | 主体中文简称 | 项目公司SPV / 总包部/项目部 |
| `{INCOME_ACCOUNT}` | 营业收入科目编号 | 6051 / 6001 |
| `{INCOME_NAME}` | 营业收入科目名称 | 其他业务收入 / 主营业务收入 |
| `{COST_ACCOUNT}` | 营业成本科目编号 | 6402 / 6401 |
| `{COST_NAME}` | 营业成本科目名称 | 其他业务成本 / 主营业务成本 |
| `{HAS_CONTRACT_ACCOUNTS}` | 施工特有科目 | 无 / 有 |
| `{HAS_AP}` | 应付账款 | 无 / 有 |
| `{HAS_LTP}` | 长期应付款 | 无 / 有 |
| `{HAS_INTERNAL}` | 内部往来 | 无 / 有 |
| `{HAS_PENDING_VAT}` | 待结算进项税额 | 无 / 有 |
| `{HAS_EQUITY}` | 权益类科目 | 有 / 无 |
| `{HAS_INVESTMENT_INCOME}` | 投资收益 | 有 / 通常无 |
| `{HAS_OTHER_INCOME}` | 其他收益 | 有 / 通常无 |
| `{HAS_INCOME_TAX}` | 所得税费用 | 有 / 通常无 |

## 七、参考材料

- 某项目公司（投资管理类）2025Q4 科目余额表（211 个科目）
- 某总包部（施工总承包类）2025M12 科目余额表
- 中国企业会计准则——一般企业科目表
- 本文件为 Base 层，对应覆盖文件：
  - `ccfts-acct-spv-chart-of-accounts` — SPV（投资管理类）
  - `ccfts-acct-project-unit-chart-of-accounts` — 项目部/总包部（施工总承包类）

## 免责声明

本科目表基于已验证的实际企业科目结构编制，可能不覆盖所有施工企业的科目变体。
