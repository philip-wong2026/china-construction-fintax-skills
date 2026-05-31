---
name: ccfts-fr-all-flash-report-workflow
description: >
  月度财务快报编制完整工作流编排。串联：实体判定→科目加载→取整→利润表→资产负债表→快报映射→输出。
  适用所有组织层级。触发条件：用户需要编制月度快报、提交SASAC/财政部快报。
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
  - ccfts-fr-all-entity-type-rules
references:
  - ccfts-fr-all-quick-report-mapping
  - ccfts-fr-all-profit-statement
  - ccfts-fr-all-balance-sheet
  - ccfts-fr-all-rounding-rules
  - ccfts-fr-all-period-end-adjustments
  - ccfts-acct-all-chart-of-accounts
  - ccfts-intel-sasac-flash-report-deadlines
is_base: true
slots:
  - ENTITY_LABEL
  - ENTITY_ALIAS
  - ORG_LEVEL
  - DEADLINE_SASAC
  - DEADLINE_MOF
  - QUICK_REPORT_SKILL
  - PROFIT_SKILL
  - BALANCE_SHEET_SKILL
  - ENTITY_TYPE_SKILL
  - CHART_OF_ACCOUNTS_SKILL
  - ROUNDING_SKILL
  - PERIOD_END_SKILL
triggers:
  - 编制快报
  - 月度快报
  - 快报流程
  - flash report workflow
  - 快报编制流程
---

# 月度财务快报编制工作流

> **SLOT 说明**：本文件为快报编制的完整工作流编排。加载本文件后，根据判定的组织层级加载对应的覆盖文件填充 SLOT。

## 快速参考

| 项目 | 值 |
|---|---|
| 适用层级 | {ORG_LEVEL}（{ENTITY_LABEL} / {ENTITY_ALIAS}） |
| SASAC 截止日 | {DEADLINE_SASAC} |
| 财政部截止日 | {DEADLINE_MOF} |
| 加载技能 | {ENTITY_TYPE_SKILL}、{CHART_OF_ACCOUNTS_SKILL}、{ROUNDING_SKILL}、{PROFIT_SKILL}、{BALANCE_SHEET_SKILL}、{PERIOD_END_SKILL}、{QUICK_REPORT_SKILL} |

## 一、快报编制完整流程

```
第 1 步：加载工作流基础
  → 加载 ccfts-workflow-base（10 步标准流程）

第 2 步：判定主体类型与层级
  → 加载 {ENTITY_TYPE_SKILL}
  → 读取科目余额表
  → 判定 Type A/B 和 {ORG_LEVEL}

第 3 步：加载层级技能
  → 加载 {CHART_OF_ACCOUNTS_SKILL}（科目结构确认）
  → 加载 {ROUNDING_SKILL}（取整参数）
  → 加载 {PROFIT_SKILL}（利润表映射）
  → 加载 {BALANCE_SHEET_SKILL}（资产负债表映射）

第 4 步：确认期间类型
  → 季度末？正常模式
  → 非季度末？加载 {PERIOD_END_SKILL}，检查是否需要期末调整

第 5 步：读取与映射
  → 读取科目余额表（列位标准格式）
  → 应用取整规则（按 SLOT 填充值）
  → 执行利润表映射
  → 执行资产负债表映射
  → 执行现金流量表映射（如有现金流量科目余额表）

第 6 步：输出快报
  → 加载 {QUICK_REPORT_SKILL}
  → 打开快报模板
  → 逐 Sheet 写入
  → 执行 Diff 对比（如有实际快报对照）

第 7 步：自检
  → 运行 18 项自检清单
  → ±1 差异诊断（如有）
  → 生成审核者摘要
```

## 二、关键时间节点

### SASAC 月度快报

| 层级 | 内部截止 |
|---|---|
| 项目部/总包部 → 工程公司 | 每月 5 日前 |
| 工程公司 → 工程局 | 每月 7 日前 |
| 工程局 → 集团总部 | 每月 8 日前 |
| 集团总部 → SASAC | 每月 9 日前（正式快报）/ 5 日前（预览） |
| 财政部快报 | 每月 10 日前 |

### 季度补充附表（季度末次月 15 日前）
- 境外子企业财务情况表
- 对外捐赠支出情况表
- 债务风险监测表
- 债券发行及持有情况表
- 金融衍生品业务情况表

## 三、SASAC vs 财政部快报差异

| 项目 | SASAC 快报 | 财政部快报 |
|---|---|---|
| 报送系统 | SASAC 财务监管系统 | 财政部统一报表平台 czbtybb.mof.gov.cn |
| 截止日 | 每月 9 日 | 每月 10 日 |
| 报告类型代码 | 0-9（单户/集团差额/金融/境外/事业/基建/集团合并） | — |
| "两金"附表 | 有（应收+存货） | 无 |
| 经济运行分析 | 可选 | 必需（文字说明） |

## 四、输出清单

编制完成后应输出：
1. 完整快报 Excel（8 Sheet + 封面保持原样）
2. 审核者摘要（主体类型、期间、填充统计、差异分析）
3. 映射明细表（每行科目→快报的完整追溯）
4. 差异分析表（如有实际快报对照）

## 五、自检清单

1. [ ] 主体类型是否正确判定？
2. [ ] 是否使用了正确的层级覆盖文件？
3. [ ] 期间类型是否正确（季度末/非季度末/年末）？
4. [ ] 取整模式是否正确应用？
5. [ ] 利润表计算链是否完整（收入→净利润）？
6. [ ] 资产负债表是否平衡？
7. [ ] 不填充项是否正确标记？
8. [ ] Diff 差异是否全部诊断（±1 临界值 vs 实质性差异）？
9. [ ] 封面是否保持原样？
10. [ ] 是否生成了审核者摘要？

## 六、SLOT 填充参考

| SLOT | 含义 |
|---|---|
| `{ENTITY_LABEL}` | 主体中文全称 |
| `{ENTITY_ALIAS}` | 主体中文简称 |
| `{ORG_LEVEL}` | 组织层级标签 |
| `{DEADLINE_SASAC}` | SASAC 内部截止日 |
| `{DEADLINE_MOF}` | 财政部内部截止日 |
| `{QUICK_REPORT_SKILL}` | 快报映射技能 slug |
| `{PROFIT_SKILL}` | 利润表技能 slug |
| `{BALANCE_SHEET_SKILL}` | 资产负债表技能 slug |
| `{ENTITY_TYPE_SKILL}` | 实体类型判定技能 slug |
| `{CHART_OF_ACCOUNTS_SKILL}` | 科目表技能 slug |
| `{ROUNDING_SKILL}` | 取整规则技能 slug |
| `{PERIOD_END_SKILL}` | 期末调整技能 slug |

## 免责声明

本工作流基于已验证企业的快报编制实践总结。不同企业的内部流程和系统可能有差异。
