---
name: ccfts-fr-project-unit-entity-type-rules
description: >
  项目部/总包部（施工总承包类，Type B）主体类型判定与详细规则。
  填充 ccfts-fr-all-entity-type-rules 的 SLOT 占位符。
  触发条件：判定为总包部/项目部/施工总承包类后的规则应用。
version: 0.2
jurisdiction: CN
tax_year: 2025
category: financial-reporting
domains: [fr]
quality_tier: research-verified
verified_by: pending
entity_levels: [project-unit]
enterprise_scales: [large-soe]
depends_on:
  - ccfts-workflow-base
references:
  - ccfts-fr-all-entity-type-rules
is_base: false
fills_slots_for: ccfts-fr-all-entity-type-rules
slots: []
triggers:
  - 总包部
  - 项目部
  - 施工总承包
  - Type B
---

# 项目部/总包部（施工总承包类/Type B）实体类型规则

> 本文件填充 `ccfts-fr-all-entity-type-rules` 的 SLOT 占位符。
> 加载顺序：先加载 Base 文件获取决策树，判定为 Type B 后加载本文件获取具体规则。

## SLOT 填充表

| SLOT | 填充值 |
|---|---|
| `{ENTITY_TYPE_LABEL}` | **施工总承包类** |
| `{ENTITY_TYPE_ALIAS}` | **总包部/项目部** |
| `{ENTITY_TYPE_CODE}` | **Type B** |
| `{PRIMARY_INCOME_ACCOUNT}` | **6001** |
| `{PRIMARY_INCOME_NAME}` | **主营业务收入**（贷方发生额） |
| `{PRIMARY_COST_ACCOUNT}` | **6401** |
| `{PRIMARY_COST_NAME}` | **主营业务成本**（借方发生额） |
| `{HAS_CONTRACT_SETTLEMENT}` | **有** |
| `{HAS_CONTRACT_PERFORMANCE_COST}` | **有** |
| `{HAS_ACCOUNTS_PAYABLE}` | **有**（需减去 1123 预付账款） |
| `{HAS_LONG_TERM_PAYABLE}` | **有** |
| `{HAS_INTERNAL_RECEIVABLES}` | **有** |
| `{HAS_PENDING_INPUT_VAT}` | **有** |
| `{EQUITY_STRUCTURE}` | **≈ 0**（内部总包部结构，资产 ≈ 负债） |
| `{BS_ROUNDING_MODE}` | **ROUND_DOWN** |
| `{IS_ROUNDING_MODE}` | **ROUND_HALF_UP** |
| `{CONTRACT_ASSET_CALC}` | **ROUND_DOWN(1483) − ROUND_DOWN(1484)**（组件级 ROUND_DOWN 后相减） |
| `{OTHER_PAYABLES_CALC}` | **ROUND_DOWN(2241-01) + ROUND_DOWN(3001)** |
| `{NET_PROFIT_FORMULA}` | **= 利润总额**（总包部通常无所得税费用科目 6801） |

## 项目部/总包部特有规则

### 权益 ≈ 0 结构

总包部作为内部管理单位，权益合计 ≈ 0，资产 = 负债。这是判定 Type B 的关键特征之一。
平衡验证简化为：**资产总计 ≈ 负债合计**（允许 ±1 万元取整噪音）。

### 施工特有科目

总包部有以下 SPV 没有的科目：
- 5801 合同结算 — 最可靠的 Type B 信号
- 5601 合同履约成本
- 2202 应付账款 — 需减去 1123 预付账款
- 2701 长期应付款
- 3001 内部往来 — 与其他内部单位的往来款项
- 1126 待结算进项税额

### 其他应付款：两科目合并

总包部的其他应付款由两部分组成：
```
其他应付款 = ROUND_DOWN(2241-01) + ROUND_DOWN(3001)
```
与 SPV 的倒推法不同，总包部直接取科目余额（但使用 ROUND_DOWN）。

### 资产负债表全局 ROUND_DOWN

总包部资产负债表所有行使用 ROUND_DOWN（截尾取整到万位）。
原因：作为内部管理单位，快报系统对 BS 各项目使用截尾取整，避免跨整数阈值。
利润表仍使用 ROUND_HALF_UP，两者独立。

### 净利润 = 利润总额

总包部不单独核算所得税（无 6801 科目），净利润直接等于利润总额。

### 信用减值损失可为负

Type B 总包部的 6702 信用减值损失可能为负（当年冲回大于计提），直接以净额填列。

## 自检清单

1. [ ] 是否确认有 5801/6001/6401/5601 中 ≥2 个科目？
2. [ ] 权益是否 ≈ 0（资产 ≈ 负债）？
3. [ ] BS 所有行是否使用了 ROUND_DOWN？
4. [ ] P&L 是否使用了 ROUND_HALF_UP（非 ROUND_DOWN）？
5. [ ] 其他应付款是否为 ROUND_DOWN(2241-01) + ROUND_DOWN(3001)？
6. [ ] 净利润是否 = 利润总额（无所得税）？

## 免责声明

本规则基于已验证的总包部 M12 2025 实际快报数据反推。不同项目部/总包部的快报系统行为可能有差异。
