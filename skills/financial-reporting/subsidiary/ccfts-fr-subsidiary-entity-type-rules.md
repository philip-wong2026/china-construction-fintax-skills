---
name: ccfts-fr-subsidiary-entity-type-rules
description: >
  独立法人子公司/工程局层级（subsidiary）主体类型判定与详细规则。
  填充 ccfts-fr-all-entity-type-rules 的 SLOT 占位符。
  触发条件：工程局级/独立法人子公司的规则应用。
version: 0.2
jurisdiction: CN
tax_year: 2025
category: financial-reporting
domains: [fr]
quality_tier: research-verified
verified_by: pending
entity_levels: [subsidiary]
enterprise_scales: [large-soe]
depends_on:
  - ccfts-workflow-base
  - ccfts-fr-all-entity-type-rules
references:
  - ccfts-fr-all-entity-type-rules
  - ccfts-intel-mof-cas33-consolidation
is_base: false
fills_slots_for: ccfts-fr-all-entity-type-rules
slots: []
triggers:
  - 工程局
  - 子公司
  - 独立法人
  - subsidiary
---

# 独立法人子公司/工程局层级（subsidiary）实体类型规则

> 填充 `ccfts-fr-all-entity-type-rules` 的 SLOT 占位符。
> 工程局是大型建筑央企体系中的核心中间层级，具有独立法人资格。

## SLOT 填充表

| SLOT | 填充值 |
|---|---|
| `{ENTITY_TYPE_LABEL}` | **工程局级独立法人** |
| `{ENTITY_TYPE_ALIAS}` | **工程局/独立法人子公司** |
| `{ENTITY_TYPE_CODE}` | **独立法人**（可能为 Type A 或 Type B） |
| `{PRIMARY_INCOME_ACCOUNT}` | **6001 或 6051**（取决于主营业务性质） |
| `{PRIMARY_INCOME_NAME}` | **主营业务收入**（施工类）/ **其他业务收入**（投资类） |
| `{PRIMARY_COST_ACCOUNT}` | **6401 或 6402** |
| `{PRIMARY_COST_NAME}` | **主营业务成本 / 其他业务成本** |
| `{HAS_CONTRACT_SETTLEMENT}` | **可能有**（如有自营施工项目） |
| `{HAS_CONTRACT_PERFORMANCE_COST}` | **可能有** |
| `{HAS_ACCOUNTS_PAYABLE}` | **有** |
| `{HAS_LONG_TERM_PAYABLE}` | **有** |
| `{HAS_INTERNAL_RECEIVABLES}` | **有**（与集团/其他工程局/下属单位的往来） |
| `{HAS_PENDING_INPUT_VAT}` | **可能有** |
| `{EQUITY_STRUCTURE}` | **完整权益结构**（独立法人，有注册资本）——实收资本+资本公积+盈余公积+未分配利润 |
| `{BS_ROUNDING_MODE}` | **ROUND_HALF_UP**（独立法人通常使用四舍五入） |
| `{IS_ROUNDING_MODE}` | **ROUND_HALF_UP** |
| `{CONTRACT_ASSET_CALC}` | **ROUND(1483) − ROUND(1484)**（组件级 ROUND_HALF_UP 后相减） |
| `{OTHER_PAYABLES_CALC}` | **按实际情况**：有倒推条件的使用倒推，否则直接取 2241 |
| `{NET_PROFIT_FORMULA}` | **利润总额 − 所得税费用**（独立法人独立纳税） |

## 工程局层级特有规则

### 混合业务模式

工程局可能同时经营多种业务，需分业务板块判断：
- **自营施工业务**：有 6001/6401/5801/5601（类似 Type B）
- **投资管理业务**：下属 SPV 项目公司（类似 Type A）
- **对下属单位的管理费收入**：6051 其他业务收入

### 对下属单位的科目特征

工程局对其下属项目部/总包部的往来通过 3001（内部往来）核算：
```
工程局 3001 = Σ 各下属总包部/项目部的 3001
```

### 独立纳税义务

工程局作为独立法人，具有独立的纳税义务：
- 有所得税费用（6801）
- 独立申报 VAT 和 CIT
- 跨区域项目需预缴增值税（2% 一般计税 / 3% 简易计税）

### 与 SPV 的差异

| 特征 | 工程局（subsidiary） | 项目公司SPV |
|------|---------------------|------------|
| 是否有施工业务 | 通常有 | 通常无 |
| 是否有 5801/5601 | 可能有（如有自营项目） | 无 |
| 是否有下属单位 | 有（项目部/总包部） | 可能有（但较少） |
| 内部往来 3001 | 有（双向：对上和对下） | 无 |
| 权益结构 | 完整 | 完整 |

### 与项目部的差异

| 特征 | 工程局（subsidiary） | 项目部（project-unit） |
|------|---------------------|------------------------|
| 法人地位 | 独立法人 | 非法人 |
| 权益结构 | 完整 | ≈ 0 |
| 所得税 | 独立缴纳 | 不单独缴纳 |
| 报表用途 | 法定报表 | 内部管理报表 |

## 自检清单

1. [ ] 是否区分了自营施工 vs 投资管理业务板块？
2. [ ] 3001 内部往来是否正确包含了对上和对下两个方向？
3. [ ] 是否有独立纳税义务（6801 所得税费用）？
4. [ ] 下属项目部的财务数据是否正确归集？
5. [ ] 是否有需要合并的下属子企业？

## 免责声明

本规则基于典型的工程局层级结构总结。不同工程局的具体组织架构和科目设置可能有差异。
