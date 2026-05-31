---
name: ccfts-fr-spv-rounding-rules
description: >
  项目公司SPV（投资管理类，Type A）快报送整规则。
  填充 ccfts-fr-all-rounding-rules 的 SLOT 占位符。
  触发条件：用户询问SPV/投资管理类/项目公司的取整规则。
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
  - ccfts-entity-type-rules
references:
  - ccfts-fr-all-rounding-rules
is_base: false
fills_slots_for: ccfts-fr-all-rounding-rules
slots: []
triggers:
  - SPV取整
  - 投资管理类取整
  - 项目公司取整
---

# SPV（投资管理类/Type A）取整规则

> 本文件填充 `ccfts-fr-all-rounding-rules` 的 SLOT 占位符。
> 加载顺序：先加载 Base 文件获取通用工作流，再加载本文件获取具体参数。

## SLOT 填充表

| SLOT | 填充值 | 说明 |
|---|---|---|
| `{BS_ROUNDING_MODE}` | **ROUND_HALF_UP** | 资产负债表：四舍五入 |
| `{IS_ROUNDING_MODE}` | **ROUND_HALF_UP** | 利润表：四舍五入 |
| `{CF_ROUNDING_MODE}` | **ROUND_HALF_UP** | 现金流量表：四舍五入 |
| `{ENTITY_LABEL}` | **投资管理类** | 主体类型中文全称 |
| `{ENTITY_ALIAS}` | **项目公司SPV** | 主体类型中文简称 |
| `{COMPONENT_ROUNDING_MODE}` | **ROUND_HALF_UP** | 合同资产(1483/1484)组件取整 |
| `{CURRENCY_FUND_MODE}` | **ROUND_HALF_UP** | 货币资金(1002)子科目取整 |
| `{OTHER_RECEIVABLES_MODE}` | **ROUND_HALF_UP** | 其他应收款(1221/1231)取整 |
| `{FIXED_ASSET_MODE}` | **ROUND_HALF_UP** | 固定资产(1601/1602)取整 |
| `{OTHER_PAYABLES_METHOD}` | **倒推：负债合计 − 应交税费 − 应付职工薪酬**（不直接取2241） | 其他应付款取数方法 |

## SPV 特有规则

### 全局 ROUND_HALF_UP（含例外）

SPV（投资管理类项目公司）在绝大多数情况下使用 ROUND_HALF_UP。

**例外情况**：当原始元值恰好在 0.5 万元临界点（即元值末五位为 X5000）且实际快报使用 ROUND_DOWN 时，改用 ROUND_DOWN。这通常在 ±1 差异诊断中发现。

### 其他应付款：倒推法（重要）

SPV 的 2241 其他应付款**不能直接取数**，必须倒推：

```
其他应付款 = 负债合计 − 应交税费(2221) − 应付职工薪酬(2211)
```

**原因**：直接取 2241 期末余额在临界值（末五位 5000 元）时会产生 ±1 万元差异。
已验证：Q4 2025 实际快报中倒推结果与实际值完全一致。

### 例外科目处理

当出现 ±1 万元差异且诊断为临界值噪音时：
1. 差异科目从 ROUND_HALF_UP 切换为 ROUND_DOWN
2. 仅影响该科目，不改变全局取整模式
3. 在审核者摘要中记录切换原因

## 与其他 SPV 层级技能的关系

本文件是 SPV 层级快报编制的基础规则之一，与以下文件配合使用：
- `ccfts-entity-type-rules` → 判定为 Type A
- `ccfts-profit-statement` → 利润表映射（含 SPV 取整口径）
- `ccfts-balance-sheet` → 资产负债表映射（含倒推逻辑）

## 自检清单

1. [ ] SPV 全局是否使用了 ROUND_HALF_UP？
2. [ ] 其他应付款是否正确使用了倒推法（不直接取 2241）？
3. [ ] 组件级取整是否正确（1483/1484 子科目分别取整后相减）？
4. [ ] 固定资产净额是否为 1601 − 1602 分别取整后相减？
5. [ ] 出现 ±1 差异的科目是否执行了临界值诊断？

## 免责声明

本规则基于已验证的 SPV 项目公司 Q4 2025 实际快报数据反推。不同 SPV 的快报系统行为可能有差异。
