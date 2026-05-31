---
name: ccfts-fr-all-rounding-rules
description: >
  中国施工企业财务快报金额取整规则——通用工作流基础（Base + SLOT 模式）。
  定义元→万元转换、组件级取整、临界值诊断的通用流程。
  适用所有组织层级。触发条件：用户询问"取整""四舍五入""±1万元差异""ROUND"等。
version: 0.2
jurisdiction: CN
tax_year: 2025
category: financial-reporting
domains: [fr]
quality_tier: research-verified
verified_by: pending
entity_levels: [all]
enterprise_scales: [large-soe]
depends_on:
  - ccfts-workflow-base
references:
  - ccfts-intel-sasac-one-profit-five-rates
is_base: true
slots:
  - BS_ROUNDING_MODE
  - IS_ROUNDING_MODE
  - CF_ROUNDING_MODE
  - ENTITY_LABEL
  - ENTITY_ALIAS
  - COMPONENT_ROUNDING_MODE
  - CURRENCY_FUND_MODE
  - OTHER_RECEIVABLES_MODE
  - FIXED_ASSET_MODE
  - OTHER_PAYABLES_METHOD
triggers:
  - 取整
  - 四舍五入
  - ROUND
  - ±1万元
  - 临界值
  - rounding
  - floor
---

# 施工企业快报取整规则（Base）

> **SLOT 说明**：本文件为通用工作流基础。其中 `{SLOT_XXX}` 为命名占位符，
> 由各组织层级的覆盖文件填充为具体值。加载本文件时，必须同时加载对应层级
> 的覆盖文件以填充 SLOT。

## 快速参考

| 项目 | 规则 |
|---|---|
| 转换公式 | 万元值 = ROUND(元值 / 10000) |
| 默认取整模式 | ROUND_HALF_UP（四舍五入） |
| 备选取整模式 | ROUND_DOWN（截尾，去尾取整） |
| 适用主体 | {ENTITY_LABEL}（{ENTITY_ALIAS}） |
| 资产负债表取整 | {BS_ROUNDING_MODE} |
| 利润表取整 | {IS_ROUNDING_MODE} |
| 现金流量表取整 | {CF_ROUNDING_MODE} |

## 一、核心原则（所有主体通用）

### 原则 1：元→万元转换

```
万元值 = ROUND_HALF_UP(元值 / 10000)   ← 默认，但按 SLOT 覆盖
```

与中国企业会计准则一致的正常会计取整方式。

### 原则 2：组件级取整（最重要，所有主体适用）

**绝对不要对计算中间值取整后，再对结果取整。**

| 科目 | 正确做法 | 错误做法 |
|---|---|---|
| 合同资产净额 | {COMPONENT_ROUNDING_MODE}(1483-01) + {COMPONENT_ROUNDING_MODE}(1483-02) + ... − {COMPONENT_ROUNDING_MODE}(1484-01) − {COMPONENT_ROUNDING_MODE}(1484-02) − ... | ROUND(1483 合计 − 1484 合计) |
| 固定资产净额 | {FIXED_ASSET_MODE}(1601) − {FIXED_ASSET_MODE}(1602) | ROUND(1601 − 1602) |
| 其他应收款净额 | {OTHER_RECEIVABLES_MODE}(1221) − {OTHER_RECEIVABLES_MODE}(1231-02) | ROUND(1221 − 1231-02) |
| 货币资金合计 | {CURRENCY_FUND_MODE}(1002-子行1) + {CURRENCY_FUND_MODE}(1002-子行2) + ... | ROUND(1002 合计) |

**原因**：先汇总再取整，当各组件分别距 0.5 临界点时，合计后会产生累积偏差。

### 原则 3：资产负债表取整模式

{ENTITY_LABEL}的资产负债表所有行使用 **{BS_ROUNDING_MODE}**。

| Sheet | 取整模式 |
|---|---|
| 资产负债指标表 | {BS_ROUNDING_MODE} |
| 利润指标表 | {IS_ROUNDING_MODE} |
| 现金流量指标表 | {CF_ROUNDING_MODE} |

{ENTITY_ALIAS}的资产负债表使用 {BS_ROUNDING_MODE} 的原因见对应层级覆盖文件。

## 二、取整模式决策表

| 场景 | 取整模式 |
|---|---|
| {ENTITY_LABEL}，正常编制 | 资产负债表 {BS_ROUNDING_MODE}，利润表 {IS_ROUNDING_MODE} |
| {ENTITY_LABEL}，出现 ±1 差异且诊断为临界值 | 差异科目改用替代取整模式 |
| 所有主体，组件级计算（1483/1484、1601/1602、1221/1231-02） | 永远分别取整后相减，不先合并 |
| 所有主体，现金流量表 | {CF_ROUNDING_MODE} |

## 三、临界值诊断流程（所有主体通用）

当快报出现 ±1 万元差异时：

1. 列出所有差异科目
2. 检查每个差异科目的原始元值 ÷ 10000 后的小数部分
3. 若小数部分 == 0.5，则该差异为临界值噪音
4. 对这些科目改用备选取整模式重新计算
5. 若差异消除，确认该科目需要使用备选取整模式

### 已知临界科目

以下科目在验证中出现过 0.5 临界值（元值末五位 = X5000）：

| 科目 | 典型情形 |
|---|---|
| 1483/1484 合同资产及其子科目 | 组件级取整比净值取整多出 ±1 |
| 其他应付款 | {OTHER_PAYABLES_METHOD} |
| 资产总计 / 负债合计（传递值） | 上游科目的 ±1 累积到合计行 |

## 四、常见错误（所有主体通用）

| 错误 | 后果 | 修复 |
|---|---|---|
| 1483 净值先取整 | ±1 万元差异，且可能连锁到资产总计 | 组件级分别取整 |
| 资产负债表全局使用错误取整模式 | 与系统填报结果不一致 | 按本文件 SLOT 规则 |
| 未执行组件级取整 | ±1 万元差异 | 对 1483/1484/1601/1602 组件级取整 |

## 五、自检清单

1. [ ] 元→万元的除 10000 是否正确？
2. [ ] 1483/1484 是否分别取整后相减？
3. [ ] 固定资产是否分项取整后相减？
4. [ ] 资产负债表是否使用了正确的取整模式（{BS_ROUNDING_MODE}）？
5. [ ] 利润表是否使用了正确的取整模式（{IS_ROUNDING_MODE}）？
6. [ ] 出现 ±1 差异时，是否执行了临界值诊断？
7. [ ] 是否正确加载了对应组织层级的 SLOT 覆盖文件？

## 六、SLOT 填充参考

| SLOT | 含义 | 本文件中的默认值 |
|---|---|---|
| `{BS_ROUNDING_MODE}` | 资产负债表取整函数 | 由层级覆盖文件定义 |
| `{IS_ROUNDING_MODE}` | 利润表取整函数 | 由层级覆盖文件定义 |
| `{CF_ROUNDING_MODE}` | 现金流量表取整函数 | 由层级覆盖文件定义 |
| `{ENTITY_LABEL}` | 主体类型中文全称 | 由层级覆盖文件定义 |
| `{ENTITY_ALIAS}` | 主体类型中文简称 | 由层级覆盖文件定义 |
| `{COMPONENT_ROUNDING_MODE}` | 合同资产(1483/1484)组件取整 | 由层级覆盖文件定义 |
| `{CURRENCY_FUND_MODE}` | 货币资金(1002)子科目取整 | 由层级覆盖文件定义 |
| `{OTHER_RECEIVABLES_MODE}` | 其他应收款(1221/1231)取整 | 由层级覆盖文件定义 |
| `{FIXED_ASSET_MODE}` | 固定资产(1601/1602)取整 | 由层级覆盖文件定义 |
| `{OTHER_PAYABLES_METHOD}` | 其他应付款取数方法 | 由层级覆盖文件定义 |

## 七、参考材料

- 已通过 Q4 2025 实际快报验证：组件级取整消除了所有 ±1 实质性差异
- 全局 ROUND_DOWN 模式（在 SPV 测试）验证：利润表产生更多偏差，不推荐作为默认
- 本文件为 Base 层，对应覆盖文件：
  - `ccfts-fr-spv-rounding-rules` — 投资管理类（项目公司 SPV）
  - `ccfts-fr-project-unit-rounding-rules` — 施工总承包类（总包部/项目部）

## 免责声明

本规则基于已验证企业的快报系统行为反推，不同企业的填报系统可能有不同的取整行为。
各组织层级的覆盖文件提供了该层级的具体取整参数。
