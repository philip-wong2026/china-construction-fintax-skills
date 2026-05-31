---
name: ccfts-fr-spv-entity-type-rules
description: >
  项目公司SPV（投资管理类，Type A）主体类型判定与详细规则。
  填充 ccfts-fr-all-entity-type-rules 的 SLOT 占位符。
  触发条件：判定为SPV/投资管理类/项目公司后的规则应用。
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
references:
  - ccfts-fr-all-entity-type-rules
is_base: false
fills_slots_for: ccfts-fr-all-entity-type-rules
slots: []
triggers:
  - SPV
  - 投资管理类
  - 项目公司
  - Type A
---

# SPV（投资管理类/Type A）实体类型规则

> 本文件填充 `ccfts-fr-all-entity-type-rules` 的 SLOT 占位符。
> 加载顺序：先加载 Base 文件获取决策树，判定为 Type A 后加载本文件获取具体规则。

## SLOT 填充表

| SLOT | 填充值 |
|---|---|
| `{ENTITY_TYPE_LABEL}` | **投资管理类** |
| `{ENTITY_TYPE_ALIAS}` | **项目公司SPV** |
| `{ENTITY_TYPE_CODE}` | **Type A** |
| `{PRIMARY_INCOME_ACCOUNT}` | **6051** |
| `{PRIMARY_INCOME_NAME}` | **其他业务收入**（贷方发生额） |
| `{PRIMARY_COST_ACCOUNT}` | **6402** |
| `{PRIMARY_COST_NAME}` | **其他业务成本**（借方发生额） |
| `{HAS_CONTRACT_SETTLEMENT}` | **无** |
| `{HAS_CONTRACT_PERFORMANCE_COST}` | **无** |
| `{HAS_ACCOUNTS_PAYABLE}` | **无**（填 0） |
| `{HAS_LONG_TERM_PAYABLE}` | **无** |
| `{HAS_INTERNAL_RECEIVABLES}` | **无** |
| `{HAS_PENDING_INPUT_VAT}` | **无** |
| `{EQUITY_STRUCTURE}` | **正常**（实收资本+资本公积+盈余公积+未分配利润） |
| `{BS_ROUNDING_MODE}` | **ROUND_HALF_UP** |
| `{IS_ROUNDING_MODE}` | **ROUND_HALF_UP** |
| `{CONTRACT_ASSET_CALC}` | **ROUND(1483) − ROUND(1484)**（分别 ROUND_HALF_UP 后相减） |
| `{OTHER_PAYABLES_CALC}` | **倒推：负债合计 − 应交税费 − 应付职工薪酬**（不直接取 2241） |
| `{NET_PROFIT_FORMULA}` | **利润总额 − 所得税费用**（净利润取 4105-14 本期贷方净发生额，不能取 4105 期末余额） |

## SPV 特有规则

### 权益结构

SPV 有完整的正常权益结构：4001（实收资本）、4002（资本公积）、4101（盈余公积）、4105-14（未分配利润）。

### 其他应付款：倒推法（关键）

SPV 的 2241 其他应付款**绝对不能直接取数**：

```
其他应付款 = 负债合计 − 应交税费(2221) − 应付职工薪酬(2211)
```

**原因**：直接取 2241 期末余额在临界值（末五位 X5000 元）时会产生 ±1 万元差异。Q4 2025 验证确认倒推结果与实际快报完全一致。

### 净利润取数口径

**正确**：取 4105-14 本期贷方净发生额（credit − debit）
**错误**：取 4105 期末余额

原因：4105 期末余额包含以前年度未分配利润和盈余公积转入，跨年度时会严重错误。

验证方法：净利润 = 利润总额 − 所得税费用，应与 4105-14 净发生额一致。

### 业务板块分配

- 利润指标表"基建建设"行 = 利润总额
- 利润指标表"市政"行 = 利润总额
- 营业收入/营业成本的明细行不填

### SPV 特有的科目

SPV 有以下科目区别于总包部：
- 6111 投资收益（有）
- 6605 其他收益（有）
- 6801 所得税费用（有）
- 递延所得税资产 1811（有）

## 自检清单

1. [ ] 是否确认无 5801/6001/6401/5601 科目？
2. [ ] 其他应付款是否正确使用了倒推法（不直接取 2241）？
3. [ ] 净利润是否取自 4105-14 净发生额而非 4105 余额？
4. [ ] 是否有正常权益结构（4001/4002/4101/4105-14 均存在）？
5. [ ] BS 和 P&L 是否使用了 ROUND_HALF_UP？

## 免责声明

本规则基于已验证的 SPV 项目公司实际快报数据反推。不同 SPV 的快报系统行为可能有差异。
