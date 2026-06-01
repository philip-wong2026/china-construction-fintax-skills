---
name: ccfts-workflow-base
description: >
  中国施工企业财务任务通用工作流基础 v0.2。定义：任务识别 → SLOT 层加载 → 实体类型判断 →
  数据读取 → 规则应用 → 自检 → 输出的 10 步标准流程。适配 Base+SLOT 架构。
  适用所有施工企业财务任务。触发条件：用户提到"快报""科目余额表""利润表""资产负债表"等。
version: 0.2
jurisdiction: CN
tax_year: 2025
category: foundation
domains: [fr]
quality_tier: research-verified
verified_by: pending
depends_on: []
entity_levels: [all]
triggers:
  - 快报
  - 财务快报
  - 科目余额表
  - 科目映射
  - 利润表
  - 资产负债表
  - 现金流量表
  - 取整
  - 期末调整
  - trial balance
  - quick report
---

# CCFTS 施工企业财务任务工作流基础 v0.2

## 快速参考

| 项目 | 值 |
|---|---|
| 适用管辖区 | 中国大陆（CN） |
| 适用行业 | 建筑施工（铁路、城轨、市政基础设施） |
| 适用会计准则 | 《企业会计准则》 |
| 金额单位规范 | 科目余额表 = 元；快报 = 万元 |
| 数据源优先级 | 原始科目余额表 > 审计报告 > 经济活动分析 > AI 摘要 |
| 技能架构 | **Base + SLOT**：加载 Base（通用工作流）→ 判定层级 → 加载覆盖文件（填充 SLOT） |
| 输出语言 | 中文 |
| 正式 Word/PDF 输出 | 需加载 `ccfts-formal-word-output-format` 并按中铁内部行文规范排版 |

## 一、Base+SLOT 加载机制（v0.2 新增）

### 加载顺序

```
Step 0: 加载对应 Base 文件（_base/ 目录，包含 {SLOT_XXX} 占位符）
   ↓
Step 2: 读取科目余额表，判定主体类型和组织层级
   ↓
Step 2.5: 加载对应层级的覆盖文件（fills_slots_for = <base-slug>）
   ↓
Step 3-9: 以填充后的 Base 规则执行任务
```

### Base + 覆盖文件映射表

| 任务 | Base 文件 | SPV 覆盖 | 项目部覆盖 |
|------|----------|----------|-----------|
| 取整规则 | `ccfts-fr-all-rounding-rules` | `ccfts-fr-spv-rounding-rules` | `ccfts-fr-project-unit-rounding-rules` |
| 实体类型判定 | `ccfts-fr-all-entity-type-rules` | `ccfts-fr-spv-entity-type-rules` | `ccfts-fr-project-unit-entity-type-rules` |
| 利润表 | `ccfts-fr-all-profit-statement` | `ccfts-fr-spv-profit-statement` | `ccfts-fr-project-unit-profit-statement` |
| 资产负债表 | `ccfts-fr-all-balance-sheet` | `ccfts-fr-spv-balance-sheet` | `ccfts-fr-project-unit-balance-sheet` |
| 快报映射 | `ccfts-fr-all-quick-report-mapping` | `ccfts-fr-spv-quick-report-mapping` | `ccfts-fr-project-unit-quick-report-mapping` |
| 期末调整 | `ccfts-fr-all-period-end-adjustments` | `ccfts-fr-spv-period-end-adjustments` | `ccfts-fr-project-unit-period-end-adjustments` |
| 科目表 | `ccfts-acct-all-chart-of-accounts` | `ccfts-acct-spv-chart-of-accounts` | `ccfts-acct-project-unit-chart-of-accounts` |

### 层级判定 → 覆盖文件选择

| 判定结果 | 组织层级 | 加载的覆盖文件前缀 |
|----------|---------|-------------------|
| Type A，独立法人，投资管理 | **spv** | `ccfts-fr-spv-*` / `ccfts-acct-spv-*` |
| Type B，非法人，施工总承包 | **project-unit** | `ccfts-fr-project-unit-*` / `ccfts-acct-project-unit-*` |
| Type A/B，工程局级独立法人 | **subsidiary** | `ccfts-fr-subsidiary-*` |
| 合并层面，集团/上市公司 | **soe-group** | `ccfts-fr-soe-group-*` |
| 非法人分支机构 | **branch** | `ccfts-fr-branch-*` |

## 二、10 步标准工作流（v0.2）

### 第 0 步：加载 Base 技能（v0.2 新增）
根据用户意图，加载对应的 Base 文件（`_base/` 目录）：
- `quick-report` → 加载 `ccfts-fr-all-quick-report-mapping`
- `entity-diagnosis` → 加载 `ccfts-fr-all-entity-type-rules`
- `account-mapping` → 加载 `ccfts-acct-all-chart-of-accounts`
- `rounding-check` → 加载 `ccfts-fr-all-rounding-rules`
- `profit-statement` → 加载 `ccfts-fr-all-profit-statement`
- `balance-sheet` → 加载 `ccfts-fr-all-balance-sheet`
- `period-end` → 加载 `ccfts-fr-all-period-end-adjustments`

Base 文件包含通用工作流和 `{SLOT_XXX}` 占位符，加载后所有 SLOT 为**未填充状态**。

### 第 1 步：确认任务类型
将用户意图映射到任务类别（同第 0 步），确认是否需要加载额外的关联 Base 文件。

### 第 2 步：确认实体类型与组织层级
读取科目余额表，判定主体类型和组织层级（详见 `ccfts-fr-all-entity-type-rules`）：
- **Type A（投资管理类）**：6051/6402，无 5801/5601/2202/2701/3001，正常权益
- **Type B（施工总承包类）**：6001/6401/5801/5601/2202/2701/3001，权益≈0

### 第 2.5 步：加载层级覆盖文件（v0.2 新增）
根据判定的组织层级，加载对应的覆盖文件（`fills_slots_for` 指向已加载的 Base）。
覆盖文件提供 SLOT 填充值，将 Base 中的占位符替换为具体参数。

**加载验证**：确认覆盖文件的 `fills_slots_for` 与已加载的 Base slug 一致。

### 第 3 步：加载数据
- 读取科目余额表（.xls 或 .xlsx）
- 列位识别：科目代码(col 1)、科目名称(col 3)、期初方向(col 6)、期初余额(col 7)、本期借方(col 8)、本期贷方(col 9)、期末方向(col 11)、期末余额(col 12)，数据从第 6 行开始
- 如有现金流量科目余额表，同格式加载 1002 子科目

### 第 4 步：确认期间类型
- 季度末（3/6/9/12 月）：正常模式
- 非季度末（1/2/4/5/7/8/10/11 月）：需考虑未结转科目
- 年末（12 月）：损益类科目借贷对冲后 `本期` = `本年累计`

### 第 5 步：应用取整规则
根据填充后的 SLOT 确定取整模式（详见 `ccfts-fr-all-rounding-rules` + 层级覆盖）：
- Type A SPV：全局 ROUND_HALF_UP
- Type B 项目部：资产负债表 ROUND_DOWN，利润表 ROUND_HALF_UP
- 绝对规则：1483/1484 组件级分别取整后相减（所有主体）

### 第 6 步：执行映射
按任务类型对应的技能文件（Base + 填充 SLOT），将科目余额映射到快报行项。

### 第 7 步：执行取整诊断（如出现 ±1 差异）
检查差异科目的元值是否在 X.5 万元临界点。若是，尝试备选取整模式；记录所有差异及根因。

### 第 8 步：19 项自检清单
输出前逐项检查：

1. [ ] 是否正确加载了 Base 文件和层级覆盖文件？
2. [ ] 覆盖文件的 fills_slots_for 是否与 Base slug 一致？
3. [ ] 实体类型判定是否有误？
4. [ ] 金额单位是否已从元转换为万元？
5. [ ] 取整模式是否正确（按 SLOT 填充值）？
6. [ ] 1483/1484 是否为组件级分别取整后相减？
7. [ ] 固定资产净额是否为原值和折旧分别取整后相减？
8. [ ] 其他应付款是否正确使用层级规定的方法？
9. [ ] 净利润取数口径是否正确（按层级规则）？
10. [ ] 利息收入是否为正数填列（取反）？
11. [ ] 资产减值损失在利润指标表是否为正数、主表是否为负数？
12. [ ] 利润板块分配是否正确？
13. [ ] 非季度末：是否应用了 --apply-open-period-adjustments？
14. [ ] None vs 0 处理是否正确？
15. [ ] 本月数、上年同期数是否标记为不填充？
16. [ ] 现金流量境内外拆分是否标记为不填充？
17. [ ] 职工人数、薪酬细项是否标记为不填充？
18. [ ] 封面代码是否保持原样不写入？
19. [ ] 如需生成正式 Word/PDF/报告正文，是否加载 `ccfts-formal-word-output-format` 并将来源、`source_path`、关键假设和未确认事项放在正文之外？

### 第 9 步：输出
按照具体技能文件要求的输出格式生成结果。包含审核者摘要模板。

若输出形态是正式 Word、PDF、报告、请示、情况说明、汇报材料、经济活动分析或其他可报送文本，应先加载 `ccfts-formal-word-output-format`。通过 CCFTS 技能形成的正式 Word/PDF 文档，默认遵守该技能中的中铁内部行文排版、正文边界和项目群财务报告口径；除非用户或外部通知明确指定其他模板。

## 三、分类体系

### 三级置信度
| 等级 | 含义 | 处理方式 |
|---|---|---|
| **Classified（确定）** | 科目明确、规则清晰，可自动处理 | 直接应用规则 |
| **Assumed（假设）** | 数据缺失或模糊，应用保守默认值 | 标记假设，供审核者确认 |
| **Needs Input（需要输入）** | 无法继续，必须向用户提问 | 提出一个针对性问题 |

### 保守默认原则
**不确定时宁可多算费用、少算收入。**

## 四、拒绝条件

- 非中国大陆企业（不适用中国企业会计准则）
- 非施工/建筑行业企业（科目体系不匹配）
- 仅提供聊天附件/摘要而无原始科目余额表
- 所需组织层级的覆盖文件尚未创建（目前覆盖：spv、project-unit）

## 五、已知局限性

- 仅覆盖已验证的组织层级：SPV（项目公司）和 project-unit（项目部/总包部）
- soe-group、subsidiary、branch 层级覆盖文件待创建
- 不填充：上年同期数、本月数（非本期发生口径部分）、现金流境内外拆分、职工人数
- 业务板块表、企业财务快报、财政部快报三个 Sheet 的完整映射逻辑待验证

## 六、审核者摘要模板

```
【审核摘要】
- Base 文件：[slug]
- 覆盖文件：[slug]（fills_slots_for: [base-slug]）
- 主体类型：[Type A / Type B]
- 组织层级：[spv / project-unit / subsidiary / soe-group / branch]
- 数据期间：[YYYYMM]
- 快报工作表数：[N]
- 已填充单元格数：[N]
- Classified：[N]  Assumed：[N]  Needs Input：[N]
- ±1 万元差异数：[N]（全为临界值噪音 / 含确实差异）
- 未确认事项：[列出]
- 审核者：[姓名]
- 审核日期：[YYYY-MM-DD]
```

## 七、版本变更

| 版本 | 日期 | 变更 |
|------|------|------|
| v0.2 | 2026-05-31 | 新增 Step 0（Base 加载）+ Step 2.5（SLOT 覆盖加载）；更新所有技能引用至新 Base+SLOT slug；新增层级判定→覆盖文件映射表 |
| v0.1 | 2026-05 | 初始版本，9 步工作流，旧 slug 引用 |

## 八、参考材料

- 本工作流基于实际快报数据验证（99.2% 匹配率）
- Base+SLOT 架构：5 个 Base 文件 + 10 个层级覆盖文件（spv、project-unit）
- 相关：`ccfts-fr-all-entity-type-rules`、`ccfts-fr-all-quick-report-mapping`

## 免责声明

本技能文件为面向 AI 代理的技术参考，不替代持证会计师的专业判断。所有输出应经人工审核后再用于正式报送。
