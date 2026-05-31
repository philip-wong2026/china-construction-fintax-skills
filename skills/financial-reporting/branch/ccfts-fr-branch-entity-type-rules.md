---
name: ccfts-fr-branch-entity-type-rules
description: >
  分公司/非法人分支机构（branch）主体类型判定与详细规则。
  填充 ccfts-fr-all-entity-type-rules 的 SLOT 占位符。
  触发条件：分公司/区域分公司/非法人分支机构的规则应用。
version: 0.2
jurisdiction: CN
tax_year: 2025
category: financial-reporting
domains: [fr]
quality_tier: research-verified
verified_by: pending
entity_levels: [branch]
enterprise_scales: [large-soe]
depends_on:
  - ccfts-workflow-base
  - ccfts-fr-all-entity-type-rules
references:
  - ccfts-fr-all-entity-type-rules
is_base: false
fills_slots_for: ccfts-fr-all-entity-type-rules
slots: []
triggers:
  - 分公司
  - 区域分公司
  - 非法人
  - branch
---

# 分公司/非法人分支机构（branch）实体类型规则

> 填充 `ccfts-fr-all-entity-type-rules` 的 SLOT 占位符。
> 分公司是非法人经营单位，常见形式为区域分公司。

## SLOT 填充表

| SLOT | 填充值 |
|---|---|
| `{ENTITY_TYPE_LABEL}` | **分公司（非法人）** |
| `{ENTITY_TYPE_ALIAS}` | **分公司/区域分公司** |
| `{ENTITY_TYPE_CODE}` | **非法人分支机构**（类似 Type B） |
| `{PRIMARY_INCOME_ACCOUNT}` | **6001**（施工业务收入） |
| `{PRIMARY_INCOME_NAME}` | **主营业务收入** |
| `{PRIMARY_COST_ACCOUNT}` | **6401** |
| `{PRIMARY_COST_NAME}` | **主营业务成本** |
| `{HAS_CONTRACT_SETTLEMENT}` | **有** |
| `{HAS_CONTRACT_PERFORMANCE_COST}` | **有** |
| `{HAS_ACCOUNTS_PAYABLE}` | **有** |
| `{HAS_LONG_TERM_PAYABLE}` | **可能有** |
| `{HAS_INTERNAL_RECEIVABLES}` | **有**（与总部的往来，通常为 3001） |
| `{HAS_PENDING_INPUT_VAT}` | **有** |
| `{EQUITY_STRUCTURE}` | **≈ 0 或无**（非法人，权益归属总部）——通常仅内部往来科目代表总部投入 |
| `{BS_ROUNDING_MODE}` | **ROUND_DOWN**（类似总包部，内部管理单位） |
| `{IS_ROUNDING_MODE}` | **ROUND_HALF_UP** |
| `{CONTRACT_ASSET_CALC}` | **ROUND_DOWN(1483) − ROUND_DOWN(1484)** |
| `{OTHER_PAYABLES_CALC}` | **ROUND_DOWN(2241-01) + ROUND_DOWN(3001)** |
| `{NET_PROFIT_FORMULA}` | **= 利润总额**（非法人，所得税由总部统一缴纳） |

## 分公司特有规则

### 非法人地位的影响

分公司不具有独立法人资格，这决定了其财务特征：
- **权益 ≈ 0**：所有权益归属总部（工程局/集团）
- **所得税**：由总部统一汇算清缴，分公司不单独缴纳
- **内部往来 3001**：与总部的资金往来（比项目部更复杂，可能涉及利润上缴/资金下拨）
- **报表用途**：内部管理报表 + 汇总至总部的组成部分

### 与项目部（project-unit）的异同

| 特征 | 分公司（branch） | 项目部（project-unit） |
|------|-----------------|----------------------|
| 法人地位 | 非法人 | 非法人 |
| 权益结构 | ≈ 0 | ≈ 0 |
| 业务范围 | 可能管理多个项目 | 通常一个项目/线路 |
| 组织层级 | 介于工程局和项目部之间 | 最基层 |
| 持续时间 | 长期存在 | 项目周期（3-5年） |
| 3001 内部往来 | 有（含与总部和多项目的往来） | 有 |
| 报表复杂度 | 较高（需汇总下属项目） | 较低 |

### 分公司的管理职能

分公司通常具有以下管理职能：
- 区域市场经营开发
- 管理下属多个项目部/总包部
- 区域资源调配（设备、人员、资金）
- 区域税务协调（跨区域 VAT 预缴）

### 分公司的科目特征

分公司科目 = 自营项目科目 + 对下属项目部的汇总 + 管理费用

```
分公司 6001 = 自营施工收入 + Σ 下属项目部收入（如汇总上报）
分公司 3001 = 与总部的往来 + Σ 与下属项目部的往来
```

### 取整规则

分公司作为内部管理单位（非法人），一般采用类似 Type B 的取整方式：
- BS：ROUND_DOWN（内部管理报表，避免跨整数阈值）
- P&L：ROUND_HALF_UP
- 但具体取整模式可能因上级单位要求而异

## 自检清单

1. [ ] 是否确认非法人地位（权益 ≈ 0）？
2. [ ] 3001 内部往来是否正确反映了与总部及下属项目的关系？
3. [ ] 是否无所得税费用（6801 = 0，由总部统一缴纳）？
4. [ ] 是否需要汇总下属项目部的财务数据？
5. [ ] BS 是否使用 ROUND_DOWN？

## 免责声明

本规则基于典型的分公司结构总结。不同企业的分公司管理模式和科目设置可能有差异。
