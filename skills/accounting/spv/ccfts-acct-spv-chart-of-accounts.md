---
name: ccfts-acct-spv-chart-of-accounts
description: >
  SPV（投资管理类，Type A）完整科目表。填充 ccfts-acct-all-chart-of-accounts 的 SLOT。
  触发条件：SPV/投资管理类/项目公司的科目查询和映射。
version: 0.2
jurisdiction: CN
tax_year: 2025
category: accounting
domains: [acct]
quality_tier: research-verified
verified_by: pending
entity_levels: [spv]
enterprise_scales: [large-soe]
depends_on:
  - ccfts-workflow-base
  - ccfts-fr-all-entity-type-rules
references:
  - ccfts-acct-all-chart-of-accounts
is_base: false
fills_slots_for: ccfts-acct-all-chart-of-accounts
slots: []
triggers:
  - SPV科目表
  - 投资管理类科目
  - 项目公司科目
---

# SPV（投资管理类/Type A）科目表

> 填充 `ccfts-acct-all-chart-of-accounts` 的 SLOT 占位符。

## SLOT 填充表

| SLOT | 填充值 |
|---|---|
| `{ENTITY_LABEL}` | **投资管理类** |
| `{ENTITY_ALIAS}` | **项目公司SPV** |
| `{INCOME_ACCOUNT}` | **6051** |
| `{INCOME_NAME}` | **其他业务收入** |
| `{COST_ACCOUNT}` | **6402** |
| `{COST_NAME}` | **其他业务成本** |
| `{HAS_CONTRACT_ACCOUNTS}` | **无**（无 5801/5601） |
| `{HAS_AP}` | **无**（填 0） |
| `{HAS_LTP}` | **无** |
| `{HAS_INTERNAL}` | **无** |
| `{HAS_PENDING_VAT}` | **无** |
| `{HAS_EQUITY}` | **有**（4001/4002/4101/4105-14） |
| `{HAS_INVESTMENT_INCOME}` | **有**（6111） |
| `{HAS_OTHER_INCOME}` | **有**（6605） |
| `{HAS_INCOME_TAX}` | **有**（6801） |

## SPV 特有科目

### SPV 独有的科目

以下科目仅 Type A（SPV）有：

| 科目 | 名称 | 说明 |
|---|---|---|
| 6051 | 其他业务收入 | 投资管理业务收入（非施工收入） |
| 6402 | 其他业务成本 | 投资管理业务成本 |
| 6111 | 投资收益 | 对外投资项目收益 |
| 6605 | 其他收益 | 政府补助等 |
| 6801 | 所得税费用 | 独立核算所得税 |
| 1811 | 递延所得税资产 | 暂时性差异 |
| 4001 | 实收资本 | 完整权益结构 |
| 4002 | 资本公积 | |
| 4101 | 盈余公积 | |
| 4105-14 | 未分配利润 | |

### SPV 没有的科目（区别于总包部）

| 科目 | 名称 | 原因 |
|---|---|---|
| 5801 | 合同结算 | 非施工企业，无建造合同 |
| 5601 | 合同履约成本 | 同上 |
| 6001 | 主营业务收入 | 非施工主业 |
| 6401 | 主营业务成本 | 同上 |
| 2202 | 应付账款 | 投资管理类无供应商应付款 |
| 2701 | 长期应付款 | 无融资租赁/分期付款采购 |
| 3001 | 内部往来 | 非内部管理单位 |
| 1126 | 待结算进项税额 | 非施工行业特有 |

### 科目数量特征

SPV 科目约 211 个（含明细），比总包部少（无施工特有科目群）。

### 关键取数注意事项

| 科目 | 注意事项 |
|---|---|
| 1002 货币资金 | 区分内部财务公司 vs 外部金融机构子科目 |
| 2241 其他应付款 | **不使用直接取数**，使用倒推法 |
| 4105-14 未分配利润 | 取本期贷方净发生额，不取期末余额 |
| 6603-02 利息收入 | 取反为正数填列 |

## 自检清单

1. [ ] 是否确认无 5801/5601/6001/6401/2202/2701/3001/1126？
2. [ ] 是否确认有 4001/4002/4101/4105-14 权益科目？
3. [ ] 其他应付款是否使用倒推法？
4. [ ] 净利润是否取自 4105-14 净发生额？

## 免责声明

本科目表基于已验证的 SPV 项目公司实际科目余额表编制。
