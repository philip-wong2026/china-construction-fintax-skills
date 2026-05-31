---
name: ccfts-rounding-rules
description: >
  中国施工企业财务快报编制中的金额取整规则。元转万元，ROUND_HALF_UP vs ROUND_DOWN 选择，
  组件级 vs 净值级取整，临界值诊断。当出现 ±1 万元差异、需要决策取整模式时触发。
version: 0.1
jurisdiction: CN
tax_year: 2025
category: financial-reporting
domains: [fr]
quality_tier: research-verified
verified_by: pending
depends_on:
  - ccfts-workflow-base
  - ccfts-entity-type-rules
entity_levels: [investment-company, construction-epc]
triggers:
  - 取整
  - 四舍五入
  - ROUND
  - ±1万元
  - 临界值
  - rounding
  - floor
---

# CCFTS — 取整规则

## 快速参考

| 项目 | 规则 |
|---|---|
| 转换公式 | 万元值 = ROUND(元值 / 10000) |
| 默认取整模式 | ROUND_HALF_UP（四舍五入） |
| 备选取整模式 | ROUND_DOWN（截尾，去尾取整） |
| Type A 取整规则 | 全局 ROUND_HALF_UP |
| Type B 取整规则 | 资产负债表 ROUND_DOWN，利润表 ROUND_HALF_UP |

## 一、核心原则

### 规则 1：元→万元默认四舍五入

```
万元值 = ROUND_HALF_UP(元值 / 10000)
```

与《企业会计准则》一致，是正常的会计取整方式。

### 规则 2：组件级取整（最重要）

**绝对不要对计算中间值取整后，再对结果取整**。

| 科目 | 正确做法 | 错误做法 |
|---|---|---|
| 合同资产净额 | ROUND(1483-01) + ROUND(1483-02) + ... — ROUND(1484-01) — ROUND(1484-02) — ... | ROUND(1483 合计 — 1484 合计) |
| 固定资产净额 | ROUND(1601) — ROUND(1602) | ROUND(1601 — 1602) |
| 其他应收款净额 | ROUND(1221) — ROUND(1231-02) | ROUND(1221 — 1231-02) |
| 货币资金合计 | ROUND(1002-子行1) + ROUND(1002-子行2) + ... | ROUND(1002 合计) |

**原因**：先汇总再取整的方式，当各组件分别距 0.5 临界点时，合计后会产生累积偏差。

### 规则 3：Type B 资产负债表用 ROUND_DOWN

施工总承包类（Type B）的资产负债表所有行使用 ROUND_DOWN。

| Sheet | 取整模式 |
|---|---|
| 资产负债指标表 | ROUND_DOWN（截尾） |
| 利润指标表 | ROUND_HALF_UP（四舍五入） |
| 现金流量指标表 | ROUND_DOWN |

**原因**：总包部作为内部管理单位，快报系统对资产负债表各项目使用截尾取整，避免因四舍五入导致资产总额跨过整数阈值。

### 规则 4：Type A 全局 ROUND_HALF_UP（含例外）

投资管理类项目公司（Type A）在绝大多数情况下使用 ROUND_HALF_UP。

例外情况——当原始元值恰好在 0.5 万元临界点（即元值末五位为 X5000）且实际快报使用 ROUND_DOWN 时，改用 ROUND_DOWN。这通常在 ±1 差异诊断中发现。

## 二、临界值诊断流程

当快报出现 ±1 万元差异时：

1. 列出所有差异科目
2. 检查每个差异科目的原始元值 ÷ 10000 后的小数部分
3. 若小数部分 == 0.5，则该差异为临界值噪音
4. 对这些科目改用 ROUND_DOWN 重新计算
5. 若差异消除，确认该科目需要 ROUND_DOWN

### 已知临界科目

以下科目在验证中出现过 0.5 临界值（元值末五位 = X5000）：

| 科目 | 典型情形 |
|---|---|
| 1483/1484 合同资产及其子科目 | 组件级取整比净值取整多出 ±1 |
| 2241 其他应付款（Type A 直接取数） | 直接取 2241 在临界值时偏离倒推结果 |
| 资产总计 / 负债合计（传递值） | 上游科目的 ±1 累积到合计行 |

**注意**：Type A 的 2241 推荐用倒推而非直接取数，从根本上避免了临界值问题。

## 三、取整模式决策表

| 场景 | 取整模式 |
|---|---|
| Type A，正常编制 | 全局 ROUND_HALF_UP |
| Type A，出现 ±1 差异且诊断为临界值 | 差异科目改用 ROUND_DOWN |
| Type B，资产负债表 | 全局 ROUND_DOWN |
| Type B，利润表 | 全局 ROUND_HALF_UP |
| 两种主体，现金流量表 | Type A: ROUND_HALF_UP; Type B: ROUND_DOWN |
| 组件级计算（1483/1484、1601/1602、1221/1231-02） | 永远分别取整后相减，不先合并 |

## 四、常见错误

| 错误 | 后果 | 修复 |
|---|---|---|
| 1483 净值先取整 | ±1 万元差异，且可能连锁到资产总计 | 组件级分别取整 |
| Type A 全局 ROUND_DOWN | 利润表大面积偏差 | 只用 ROUND_HALF_UP（除非经验证的例外） |
| Type B 资产负债表用 ROUND_HALF_UP | 与系统填报结果不一致 | 改用 ROUND_DOWN |
| 直接取 2241 期末余额（Type A） | 临界值时 ±1 万元 | 使用倒推公式 |

## 五、自检清单

1. [ ] 元→万元的除 10000 是否正确？
2. [ ] 1483/1484 是否分别取整后相减？
3. [ ] 固定资产是否分项取整后相减？
4. [ ] Type B 资产负债表是否用了 ROUND_DOWN？
5. [ ] Type B 利润表是否用了 ROUND_HALF_UP？
6. [ ] 出现 ±1 差异时，是否执行了临界值诊断？

## 六、参考材料

- 已通过 Q4 2025 实际快报验证：组件级取整消除了所有 ±1 实质性差异
- 全局 ROUND_DOWN 模式（Type A 测试）验证：利润表产生更多偏差，不推荐作为默认

## 免责声明

本规则基于已验证企业的快报系统行为反推，不同企业的填报系统可能有不同的取整行为。
