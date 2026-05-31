---
name: ccfts-fr-all-quick-report-mapping
description: >
  中国施工企业科目余额表 → 财务快报 Excel 完整映射流程——通用工作流基础（Base + SLOT 模式）。
  涵盖 6 张工作表结构、数据加载、Diff 对比、不填充项声明。
  适用所有组织层级。触发条件：用户需要编制快报、将科目余额表转换为快报格式。
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
  - ccfts-fr-all-profit-statement
  - ccfts-fr-all-balance-sheet
  - ccfts-fr-all-rounding-rules
is_base: true
slots:
  - ENTITY_LABEL
  - ENTITY_ALIAS
  - ENTITY_PROFIT_SKILL
  - ENTITY_BALANCE_SHEET_SKILL
  - ENTITY_TYPE_RULES_SKILL
  - ENTITY_CHART_OF_ACCOUNTS_SKILL
  - ENTITY_ROUNDING_SKILL
  - BS_ROUNDING_MODE
  - IS_ROUNDING_MODE
triggers:
  - 快报映射
  - 快报编制
  - 科目余额转快报
  - quick report mapping
---

# 施工企业快报映射流程（Base）

> **SLOT 说明**：本文件为通用工作流基础。`{SLOT_XXX}` 由各组织层级的覆盖文件填充。

## 快速参考

| 项目 | 值 |
|---|---|
| 源文件格式 | 科目余额表（.xls / .xlsx，数据从 row 6 开始） |
| 目标文件格式 | 快报导入模板（.xlsx，8 个内容 Sheet + 封面） |
| 金额转换 | 元 → 万元（÷10000） |
| 映射方式 | 按标签名匹配写入（非按固定行列号） |
| 适用主体 | {ENTITY_LABEL}（{ENTITY_ALIAS}） |
| 加载技能 | {ENTITY_TYPE_RULES_SKILL}、{ENTITY_PROFIT_SKILL}、{ENTITY_BALANCE_SHEET_SKILL}、{ENTITY_CHART_OF_ACCOUNTS_SKILL}、{ENTITY_ROUNDING_SKILL} |

## 一、科目余额表读取（通用）

### 列位

| 列 | 含义 |
|---|---|
| 1 | 科目编号 |
| 3 | 科目名称 |
| 6 | 期初方向（借/贷） |
| 7 | 期初余额（元） |
| 8 | 本期发生—借方（元） |
| 9 | 本期发生—贷方（元） |
| 11 | 期末方向（借/贷） |
| 12 | 期末余额（元） |

数据从第 6 行开始（前 5 行为表头/空行）。

如有现金流量科目余额表，同格式加载 1002 子科目。

## 二、快报 Sheet 结构（通用）

共 8 个内容 Sheet：
1. **利润指标表** — P&L 指标（含本年累计）
2. **资产负债指标表** — B/S 指标
3. **现金流量指标表** — 现金流指标
4. **合并抵销资料-内部往来及交易** — 本阶段不填
5. **业务板块表** — 利润分板块
6. **企业财务快报（2025）** — 按企业口径的快报
7. **财政部快报** — 按财政部口径的快报
8. **附报文档** — 不填

另有封面页（封面代码（国资委）、封面代码（财政部））和 HIDDENSHEETNAME，不写入。

### 列位（各指标表）

| 列 | 含义 |
|---|---|
| A | 序号 |
| B | 项目名称（标签） |
| C | 年度预算 |
| D | 本月数—境内 |
| E | 本月数—境外 |
| F | 本月数—合计 |
| G | 本年累计—境内 |

## 三、映射操作流程（通用）

1. **判定主体类型** → 加载 `{ENTITY_TYPE_RULES_SKILL}`，确定 {ENTITY_LABEL}
2. **加载科目表** → 加载 `{ENTITY_CHART_OF_ACCOUNTS_SKILL}`，确认科目结构
3. **加载取整规则** → 加载 `{ENTITY_ROUNDING_SKILL}`，确定 BS={BS_ROUNDING_MODE}、IS={IS_ROUNDING_MODE}
4. **加载模板** → 打开快报导入模板 .xlsx
5. **清除旧值** → 清空 6 张 Sheet 的 D-G 列（保留 A-C 列的标签和序号）
6. **逐 Sheet 写入** → 按 B 列标签名匹配，写入对应列的万元值
   - 利润指标表：加载 `{ENTITY_PROFIT_SKILL}`
   - 资产负债指标表：加载 `{ENTITY_BALANCE_SHEET_SKILL}`
   - 现金流量指标表：直接取现金流量科目余额表的 1002 子科目数据
   - 业务板块表：利润总额按业务板块分配
7. **保持模板结构** → 不增删行、不改格式、不改封面

### D 列（本月数）处理

- 非年末月（1-11 月）：D 列 = 科目"本期发生"（借方或贷方）
- 部分年末（12 月）企业：本期 = 12 月单月（使用月度关账试算表）
- 另一部分年末企业：本期 = 全年累计（损益类借贷对冲后）
- 若不确定，标记为 Assumed 并注明假设

## 四、不填充的项目（通用）

以下项目无法从科目余额表单独确定，不参与填充和比对：
- 上年同期数（需上年度快报）
- 本月数的 D/E 分拆（境内外）
- 现金流量各行的境内外分拆
- 职工人数、从业人员数
- 薪酬总额中的细项（工资/社保/公积金分项）
- 封面代码页的任何字段
- 合并抵销资料 Sheet

## 五、比对（Diff）说明（通用）

### None vs 0 规则

实际快报中部分单元格为空（None），含义为该期间该项目为零或未填报。比对时将 None 等同于 0，按匹配处理。

### 模板版本差异

不同年度、不同批次的快报模板可能有行号偏移。比对应以标签名为准，非以行号为准。

## 六、特殊行规则（通用）

### 利润板块分配（业务板块表）

- 利润 = 利润总额（填至对应板块行）
- 营业收入/营业成本的明细行不按利润填
- 板块分类按固定行写入，不按标签模糊匹配

### 资产减值损失双重列示

- 利润指标表：以正数填列
- 资产负债指标表/主表：以负数填列（损失）

## 七、映射结果输出格式（通用）

### 映射结果标准格式

每行一个映射：行号 | 快报项目 | 科目编号 | 科目名称 | 取数口径 | 原始值（元） | 万元值 | 置信度 | 备注

### 差异分析标准格式

Sheet | 行 | 项目名称 | 生成值 | 实际值 | 差 | 根因 | 建议

## 八、审核者摘要模板（通用）

```
【审核摘要】
- 主体类型：{ENTITY_LABEL}（{ENTITY_ALIAS}）
- 数据期间：[YYYYMM]
- 快报工作表数：[N]
- 已填充单元格数：[N]
- Classified：[N]  Assumed：[N]  Needs Input：[N]
- ±1 万元差异数：[N]（全为临界值噪音 / 含确实差异）
- 未确认事项：[列出]
- 审核者：[姓名]
- 审核日期：[YYYY-MM-DD]
```

## 九、自检清单

1. [ ] 是否使用了正确的模板文件？
2. [ ] 旧值是否正确清除（D-G 列）？
3. [ ] 所有映射是否以标签名匹配（非固定行号）？
4. [ ] 金额是否已从元转换为万元？
5. [ ] 实体类型是否正确判定（{ENTITY_LABEL}）？
6. [ ] 封面是否保持原样？
7. [ ] 不填充的项目是否已标记？
8. [ ] 是否正确加载了对应层级的 SLOT 覆盖文件？

## 十、SLOT 填充参考

| SLOT | 含义 |
|---|---|
| `{ENTITY_LABEL}` | 主体中文全称 |
| `{ENTITY_ALIAS}` | 主体中文简称 |
| `{ENTITY_PROFIT_SKILL}` | 利润表技能 slug |
| `{ENTITY_BALANCE_SHEET_SKILL}` | 资产负债表技能 slug |
| `{ENTITY_TYPE_RULES_SKILL}` | 实体类型判定技能 slug |
| `{ENTITY_CHART_OF_ACCOUNTS_SKILL}` | 科目表技能 slug |
| `{ENTITY_ROUNDING_SKILL}` | 取整规则技能 slug |
| `{BS_ROUNDING_MODE}` | 资产负债表取整模式 |
| `{IS_ROUNDING_MODE}` | 利润表取整模式 |

## 十一、参考材料

- 本规则基于 Q3/Q4 2025 及 2026M05 实际快报编制验证
- 已验证匹配率：99.2%（123 个单元格，0 个实质性差异）

## 免责声明

本映射规则基于已验证的快报编制实践反推，不同企业的快报模板和填报系统可能有差异。
