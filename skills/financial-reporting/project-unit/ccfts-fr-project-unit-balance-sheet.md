---
name: ccfts-fr-project-unit-balance-sheet
description: >
  项目部/总包部（施工总承包类，Type B）资产负债表编制规则。填充 ccfts-fr-all-balance-sheet 的 SLOT。
  触发条件：总包部/项目部/施工总承包类的资产负债表编制。
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
  - ccfts-fr-all-entity-type-rules
references:
  - ccfts-fr-all-balance-sheet
is_base: false
fills_slots_for: ccfts-fr-all-balance-sheet
slots: []
triggers:
  - 总包部资产负债表
  - 项目部资产负债表
  - 施工总承包资产负债表
---

# 项目部/总包部（施工总承包类/Type B）资产负债表规则

> 填充 `ccfts-fr-all-balance-sheet` 的 SLOT 占位符。

## SLOT 填充表

| SLOT | 填充值 |
|---|---|
| `{ENTITY_LABEL}` | **施工总承包类** |
| `{ENTITY_ALIAS}` | **总包部/项目部** |
| `{BS_ROUNDING_MODE}` | **ROUND_DOWN**（截尾取整到万位，全部资产/负债行） |
| `{COMPONENT_ROUNDING_MODE}` | **ROUND_DOWN** |
| `{CONTRACT_ASSET_CALC}` | **ROUND_DOWN(1483) − ROUND_DOWN(1484)**（组件级 ROUND_DOWN 后相减） |
| `{OTHER_PAYABLES_CALC}` | **ROUND_DOWN(2241-01) + ROUND_DOWN(3001)** |
| `{HAS_CONTRACT_LIABILITIES}` | **有**（ROUND_DOWN(5801 贷方余额)） |
| `{HAS_LONG_TERM_PAYABLE}` | **有**（ROUND_DOWN(2701)） |
| `{HAS_ACCOUNTS_PAYABLE}` | **有**（ROUND_DOWN(2202) − ROUND_DOWN(1123)） |
| `{EQUITY_STRUCTURE_DESC}` | **≈ 0**（内部总包部结构，资产 = 负债） |
| `{HAS_EQUITY_ACCOUNTS}` | **无**（无 4001/4002/4101 等权益科目） |
| `{BALANCE_CHECK_FORMULA}` | **资产总计 ≈ 负债合计**（权益 ≈ 0，允许 ±1 万元取整噪音） |

## 项目部/总包部特有规则

### 全局 ROUND_DOWN

总包部资产负债表**所有行**使用 ROUND_DOWN（截尾取整到万位）。

**原因**：总包部作为内部管理单位（权益 ≈ 0，资产 = 负债），快报系统对 BS 各项目使用截尾取整，避免因四舍五入导致资产总额跨过整数阈值。

**影响**：资产和负债各科目均向下取整，合计值系统性略低于实际值。平衡关系不受影响（两侧同等 ROUND_DOWN）。

### 完整的负债侧科目

总包部有 SPV 没有的负债科目：

| 快报项目 | 计算 |
|---|---|
| 应付账款 | ROUND_DOWN(2202) − ROUND_DOWN(1123) |
| 合同负债 | ROUND_DOWN(5801 贷方余额) |
| 其他应付款 | ROUND_DOWN(2241-01) + ROUND_DOWN(3001) |
| 其他流动负债 | ROUND_DOWN(1126)（待结算进项税额） |
| 长期应付款 | ROUND_DOWN(2701) |

### 其他应付款：两科目合并

总包部的其他应付款由两部分组成，与 SPV 的倒推法完全不同：
```
其他应付款 = ROUND_DOWN(2241-01) + ROUND_DOWN(3001)
```
其中 3001（内部往来）是总包部特有的科目。

### 权益 ≈ 0

总包部无实收资本、资本公积、盈余公积等权益科目。权益合计填 0（或接近 0）。

### 平衡验证（简化）

```
资产总计 ≈ 负债合计
```

验证：Q4 2025 某总包部资产 = 负债 = 16863 万元。

## 自检清单

1. [ ] BS 所有行是否使用 ROUND_DOWN（非 ROUND_HALF_UP）？
2. [ ] 应付账款是否为 ROUND_DOWN(2202) − ROUND_DOWN(1123)？
3. [ ] 合同负债是否为 ROUND_DOWN(5801 贷方余额)？
4. [ ] 其他应付款是否为 ROUND_DOWN(2241-01) + ROUND_DOWN(3001)？
5. [ ] 权益合计是否 ≈ 0？
6. [ ] 资产总计 ≈ 负债总计？

## 免责声明

本规则基于已验证的总包部 M12 2025 资产负债表反推。
