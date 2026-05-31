---
name: ccfts-fr-project-unit-rounding-rules
description: >
  项目部/总包部（施工总承包类，Type B）快报送整规则。
  填充 ccfts-fr-all-rounding-rules 的 SLOT 占位符。
  触发条件：用户询问总包部/项目部/施工总承包类的取整规则。
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
  - ccfts-entity-type-rules
references:
  - ccfts-fr-all-rounding-rules
is_base: false
fills_slots_for: ccfts-fr-all-rounding-rules
slots: []
triggers:
  - 总包部取整
  - 项目部取整
  - 施工总承包取整
---

# 项目部/总包部（施工总承包类/Type B）取整规则

> 本文件填充 `ccfts-fr-all-rounding-rules` 的 SLOT 占位符。
> 加载顺序：先加载 Base 文件获取通用工作流，再加载本文件获取具体参数。

## SLOT 填充表

| SLOT | 填充值 | 说明 |
|---|---|---|
| `{BS_ROUNDING_MODE}` | **ROUND_DOWN** | 资产负债表：截尾取整 |
| `{IS_ROUNDING_MODE}` | **ROUND_HALF_UP** | 利润表：四舍五入 |
| `{CF_ROUNDING_MODE}` | **ROUND_DOWN** | 现金流量表：截尾取整 |
| `{ENTITY_LABEL}` | **施工总承包类** | 主体类型中文全称 |
| `{ENTITY_ALIAS}` | **总包部/项目部** | 主体类型中文简称 |
| `{COMPONENT_ROUNDING_MODE}` | **ROUND_DOWN** | 合同资产(1483/1484)组件取整 |
| `{CURRENCY_FUND_MODE}` | **ROUND_DOWN** | 货币资金(1002)子科目取整 |
| `{OTHER_RECEIVABLES_MODE}` | **ROUND_DOWN** | 其他应收款(1221/1231)取整 |
| `{FIXED_ASSET_MODE}` | **ROUND_DOWN** | 固定资产(1601/1602)取整 |
| `{OTHER_PAYABLES_METHOD}` | **ROUND_DOWN(2241-01) + ROUND_DOWN(3001)** | 其他应付款取数方法 |

## 项目部/总包部特有规则

### 资产负债表全局 ROUND_DOWN

施工总承包类（项目部/总包部）的资产负债表**所有行**使用 ROUND_DOWN（截尾取整到万位）。

**原因**：总包部作为内部管理单位（权益 ≈ 0，资产 = 负债），快报系统对资产负债表各项目使用截尾取整，避免因四舍五入导致资产总额跨过整数阈值。这是快报系统的实际行为，非会计准则要求。

**重要**：利润表仍使用 ROUND_HALF_UP，不因资产负债表模式而改变。

### 其他应付款：两科目合并

总包部的其他应付款由两部分组成：

```
其他应付款 = ROUND_DOWN(2241-01) + ROUND_DOWN(3001)
```

其中 3001（内部往来）是总包部特有的科目，SPV 无此科目。
与 SPV 的倒推法不同，总包部直接取科目余额（但使用 ROUND_DOWN 而非 ROUND_HALF_UP）。

### 权益 ≈ 0 的影响

由于总包部权益合计 ≈ 0（资产 = 负债），资产负债表平衡验证简化为：

```
资产总计 ≈ 负债合计（允许 ±1 万元取整噪音）
```

### ROUND_DOWN 的全局影响

| 影响范围 | 说明 |
|---|---|
| 资产和负债各科目 | 均向下取整，合计值系统性略低于实际值 |
| 平衡关系 | 资产 = 负债 仍然成立（ROUND_DOWN 对两侧同等影响） |
| 利润表 | **不受影响**，仍使用 ROUND_HALF_UP |
| 临界值科目 | 0.5 临界值天然向下取整，无 ±1 噪音（与 SPV 不同） |

## 与其他项目层级技能的关系

本文件是项目部/总包部层级快报编制的基础规则之一，与以下文件配合使用：
- `ccfts-entity-type-rules` → 判定为 Type B（检测 5801/6001/6401/3001 科目）
- `ccfts-profit-statement` → 利润表映射（ROUND_HALF_UP）
- `ccfts-balance-sheet` → 资产负债表映射（ROUND_DOWN 全局）

## 自检清单

1. [ ] 资产负债表所有行是否使用了 ROUND_DOWN？
2. [ ] 利润表是否使用了 ROUND_HALF_UP（非 ROUND_DOWN）？
3. [ ] 现金流量表是否使用了 ROUND_DOWN？
4. [ ] 其他应付款是否为 ROUND_DOWN(2241-01) + ROUND_DOWN(3001)？
5. [ ] 组件级取整是否正确（1483/1484 子科目 ROUND_DOWN 后相减）？
6. [ ] 资产总计 ≈ 负债总计？（权益 ≈ 0）

## 免责声明

本规则基于已验证的总包部 M12 2025 实际快报数据反推。不同项目部/总包部的快报系统行为可能有差异。
