---
name: ccfts-fr-soe-group-entity-type-rules
description: >
  央企集团/上市公司合并层面（soe-group）主体类型判定与详细规则。
  填充 ccfts-fr-all-entity-type-rules 的 SLOT 占位符。
  触发条件：集团合并层面/上市公司合并层面的规则应用。
version: 0.2
jurisdiction: CN
tax_year: 2025
category: financial-reporting
domains: [fr]
quality_tier: research-verified
verified_by: pending
entity_levels: [soe-group]
enterprise_scales: [large-soe]
depends_on:
  - ccfts-workflow-base
  - ccfts-fr-all-entity-type-rules
references:
  - ccfts-fr-all-entity-type-rules
  - ccfts-intel-mof-cas33-consolidation
  - ccfts-fr-all-consolidation-workflow
is_base: false
fills_slots_for: ccfts-fr-all-entity-type-rules
slots: []
triggers:
  - 集团合并
  - 上市公司合并
  - 股份公司
  - 央企集团
  - soe-group
---

# 央企集团/上市公司合并层面（soe-group）实体类型规则

> 填充 `ccfts-fr-all-entity-type-rules` 的 SLOT 占位符。
> 本层为**合并层面**，加载前应先完成各子级的单户报表。

## SLOT 填充表

| SLOT | 填充值 |
|---|---|
| `{ENTITY_TYPE_LABEL}` | **集团合并层面** |
| `{ENTITY_TYPE_ALIAS}` | **央企集团/上市公司** |
| `{ENTITY_TYPE_CODE}` | **合并层面** |
| `{PRIMARY_INCOME_ACCOUNT}` | **合并营业收入**（各板块汇总） |
| `{PRIMARY_INCOME_NAME}` | **主营业务收入 + 其他业务收入** |
| `{PRIMARY_COST_ACCOUNT}` | **合并营业成本**（各板块汇总） |
| `{PRIMARY_COST_NAME}` | **主营业务成本 + 其他业务成本** |
| `{HAS_CONTRACT_SETTLEMENT}` | **有**（来自下属施工子企业） |
| `{HAS_CONTRACT_PERFORMANCE_COST}` | **有**（来自下属施工子企业） |
| `{HAS_ACCOUNTS_PAYABLE}` | **有**（合并层面，已抵销内部往来） |
| `{HAS_LONG_TERM_PAYABLE}` | **有**（合并层面） |
| `{HAS_INTERNAL_RECEIVABLES}` | **无**（已抵销）——合并层面内部往来全部抵销 |
| `{HAS_PENDING_INPUT_VAT}` | **有**（来自下属子企业） |
| `{EQUITY_STRUCTURE}` | **完整权益结构**（含少数股东权益）——实收资本+资本公积+盈余公积+未分配利润+少数股东权益 |
| `{BS_ROUNDING_MODE}` | **ROUND_HALF_UP** |
| `{IS_ROUNDING_MODE}` | **ROUND_HALF_UP** |
| `{CONTRACT_ASSET_CALC}` | **ROUND(1483合并) − ROUND(1484合并)**（合并层面组件级取整） |
| `{OTHER_PAYABLES_CALC}` | **直接取数**（合并层面内部往来已抵销，无倒推必要） |
| `{NET_PROFIT_FORMULA}` | **利润总额 − 所得税费用**（含少数股东损益） |

## 集团合并层面特有规则

### 合并层面特征

央企集团/上市公司是最高合并层面，具有以下特征：
- **合并范围**：含所有受控子企业（按 CAS 33 控制三要素判断）
- **内部往来已抵销**：3001 内部往来在合并层面为零
- **少数股东权益**：合并 B/S 中单独列示
- **少数股东损益**：合并 P&L 中单独列示
- **板块分部**：按基建建设、市政、勘察设计、工业制造、房地产、金融等分部披露

### 科目特征（合并后）

合并层面科目 = 各子企业科目汇总 − 内部抵销

| 科目 | 合并层面特征 |
|------|-------------|
| 3001 内部往来 | 抵销后 = 0 |
| 1483/1484 合同资产 | 含所有子企业的合同资产（含 PPP 项目） |
| 2202 应付账款 | 含所有子企业的应付（已抵销内部应付） |
| 4001 实收资本 | 仅母公司实收资本（子公司实收资本已抵销） |
| 少数股东权益 | 合并层面特有，单户层面无 |

### 不同于 SPV/项目部

集团合并层面**不是单一主体类型**：
- 下属包含 Type A（SPV、投资公司）和 Type B（项目部、工程公司）
- 合并层面需要同时理解和处理两种类型的科目来源
- 不能套用单一类型的取整或计算规则——需分别处理各子企业后合并

### 合并抵销对科目余额的影响

合并层面科目余额已是抵销后数据：
- 应收/应付内部款项 → 0
- 收入/成本内部交易 → 已抵销
- 长投/权益 → 已抵销
- 未实现内部损益 → 已抵销

## 自检清单

1. [ ] 合并范围是否按 CAS 33 逐一判断？
2. [ ] 内部往来是否全部抵销（3001 = 0）？
3. [ ] 少数股东权益是否正确计算？
4. [ ] PPP 项目公司是否按国资委要求原则性合并？
5. [ ] 板块分部数据是否正确归集？

## 免责声明

本规则基于央企集团合并报表实践总结。具体合并范围以审计确认为准。
