# CCFTS 项目交接提示词

> 复制以下内容，粘贴给任何 AI（Claude、GPT、Gemini 等），即可继续开发。

---

## 项目概述

**名称**：CCFTS（China Construction Finance & Tax Skills）
**定位**：中国施工企业财税 AI 技能库——可被任何 AI agent 读取的 domain skills。
**适用范围**：仅限施工企业核心技能（CREC/CRCC/CSCEC 体系下的集团→工程局→工程公司→项目部→SPV 全链条），尚未延展至中国一般企业会计。

## 当前进度

- **Phase 0（架构）**：✅ 完成。目录结构、技能模板、验证脚本 v0.2.1、MCP 服务器 v0.2。
- **Phase 1（法规+操作）**：✅ 完成。12 个法规技能 + 8 个操作技能，24 文件 0 问题，交叉引用全有效。
- **Phase 2（扩展）**：🔄 进行中。Base+SLOT 试点已完成（取整规则），模式验证可行。

## 下一步任务：继续 Phase 2 Base+SLOT 拆分

将 `skills/china-construction/` 下的旧操作技能拆分为 Base + 层级覆盖文件，迁移到 `skills/financial-reporting/` 目录。

### 待拆分技能（按优先级）

| 序号 | 旧文件 | 新建 Base 文件 | 新建覆盖文件 |
|------|--------|---------------|-------------|
| 1 | `ccfts-entity-type-rules.md` | `financial-reporting/_base/ccfts-fr-all-entity-type-rules.md` | `spv/ccfts-fr-spv-entity-type-rules.md` + `project-unit/ccfts-fr-project-unit-entity-type-rules.md` |
| 2 | `ccfts-profit-statement.md` | `financial-reporting/_base/ccfts-fr-all-profit-statement.md` | 同上结构 |
| 3 | `ccfts-balance-sheet.md` | `financial-reporting/_base/ccfts-fr-all-balance-sheet.md` | 同上结构 |
| 4 | `ccfts-chart-of-accounts.md` | `financial-reporting/_base/ccfts-acct-all-chart-of-accounts.md` | 同上结构 |

### 已完成（参考范例）

- `financial-reporting/_base/ccfts-fr-all-rounding-rules.md` — Base 文件（10 个 SLOT）
- `financial-reporting/spv/ccfts-fr-spv-rounding-rules.md` — SPV 覆盖（Type A）
- `financial-reporting/project-unit/ccfts-fr-project-unit-rounding-rules.md` — 项目部覆盖（Type B）

## 关键设计决策（必须遵守）

### 1. Base + SLOT 模式

**Base 文件**（放 `_base/` 目录）：
- `is_base: true`
- 定义 `slots: [SLOT_NAME_1, SLOT_NAME_2, ...]`
- 正文中用 `{SLOT_NAME}` 占位符标记需要覆盖的值
- 包含通用工作流、原则、自检清单

**覆盖文件**（放对应层级目录）：
- `is_base: false`
- `fills_slots_for: <base-slug>`
- `slots: []`（空数组）
- 正文中包含"SLOT 填充表"，列出每个 SLOT 的填充值
- 可添加该层级特有的规则和例外

### 2. 目录结构

```
skills/
  financial-reporting/
    _base/           ← 通用工作流 + SLOT 占位符
    soe-group/       ← 央企集团/上市公司层级
    subsidiary/      ← 独立法人子公司/工程局层级
    branch/          ← 分公司（非法人）层级
    project-unit/    ← 项目部/总包部/代局指层级
    spv/             ← 项目公司SPV层级
  accounting/        ← 同上结构
  tax/               ← 同上结构
  analysis/          ← 同上结构
  management/        ← 同上结构
  intelligence/      ← 法规知识（按监管机构组织，不按层级）
  foundation/        ← 跨领域通用工作流
```

### 3. 命名规范

```
ccfts-{domain}-{level}-{topic}.md

domain: fr(报表) / acct(会计) / tax(税务) / anlys(分析) / mgmt(管理) / intel(法规)
level:  soe-group / subsidiary / branch / project-unit / spv / all(跨层级)
```

### 4. 脱敏原则

**绝对不能**出现真实的企业名称、项目名称、地名、具体金额。用"某项目公司""某总包部""某集团"替代。

### 5. 两种主体类型（目前仅覆盖这两种）

| 特征 | Type A（投资管理类/SPV） | Type B（施工总承包类/项目部） |
|------|--------------------------|------------------------------|
| 主营业务 | 投资管理、资产管理 | 建设施工总承包 |
| 收入科目 | 6051 其他业务收入 | 6001 主营业务收入 |
| 成本科目 | 6402 其他业务成本 | 6401 主营业务成本 |
| 合同结算(5801) | 无 | 有 |
| 内部往来(3001) | 无 | 有 |
| 权益结构 | 正常（实收资本+资本公积+盈余公积+未分配利润） | ≈ 0（资产=负债） |
| 资产负债表取整 | ROUND_HALF_UP | ROUND_DOWN |
| 利润表取整 | ROUND_HALF_UP | ROUND_HALF_UP |
| 其他应付款 | 倒推：负债合计-税费-薪酬 | 直接：2241-01 + 3001 |
| 净利润 | 利润总额 - 所得税费用 | = 利润总额（无所得税） |

### 6. Skill Frontmatter 规范

```yaml
---
name: ccfts-{domain}-{level}-{topic}
description: 一句话描述 + 触发关键词
version: 0.2
jurisdiction: CN
tax_year: 2025
category: financial-reporting    # 或 accounting/tax/analysis/management/intelligence/foundation
domains: [fr]                    # 职能领域数组
quality_tier: research-verified  # 或 accountant-verified
verified_by: pending             # 或 CPA 姓名+执业编号
entity_levels: [spv]            # 适用组织层级
enterprise_scales: [large-soe]   # 企业规模
depends_on:                      # 前置依赖技能 slug 数组
  - ccfts-workflow-base
  - ccfts-entity-type-rules
references:                      # 引用的 intelligence 技能 slug 数组
  - ccfts-fr-all-rounding-rules
is_base: false                   # 是否为 Base 文件
fills_slots_for: ccfts-fr-all-rounding-rules  # 填充哪个 Base 的 SLOT（覆盖文件填）
slots: []                        # 定义的 SLOT 列表（Base 文件填）
triggers:                        # 触发关键词
  - 关键词1
  - 关键词2
---
```

### 7. 正文结构规范

每个技能文件应按以下结构组织：
1. **快速参考表** — 最核心的数值/规则一览
2. **主规则** — 按章节组织（一、二、三...）
3. **工作流/决策步骤** — 1-2-3-4 步骤化
4. **自检清单** — checkbox 格式（`1. [ ] ...`）
5. **审核者摘要模板** — 可选
6. **参考材料/引用来源** — 法规文号、验证数据来源
7. **免责声明**

### 8. 三阶段迁移策略

1. 旧技能（`china-construction/` 下）保持不变，新技能并行开发
2. 新技能齐备后，重构旧技能指向新 slug
3. MCP slug 别名映射旧 slug → 新 slug

## 工作流程（每做一个技能拆分）

```
1. 阅读旧文件（skills/china-construction/ccfts-xxx.md）
2. 识别 Type A vs Type B 的差异点 → 这些就是 SLOT
3. 写 Base 文件（_base/ 目录）
   - 抽取通用逻辑
   - 差异点用 {SLOT_NAME} 替代
   - is_base: true, 列出所有 slots
4. 写 SPV 覆盖文件（spv/ 目录）
   - 只含 SLOT 填充表 + 该层级特有规则
   - fills_slots_for: <base-slug>
5. 写 project-unit 覆盖文件（project-unit/ 目录）
   - 同上
6. 更新 skills/README.md 快速查找
7. 更新 MCP 服务器的 SLUG_ALIASES 和 intent catalogue
8. 运行验证：
   cd 项目根目录
   python3 scripts/validate-skills.py
   预期：PASSED: N files, 0 issues.
```

## MCP 服务器需要更新的位置

文件：`mcp/ccfts_mcp/server.py`

1. **SLUG_ALIASES** — 添加旧 slug → 新 slug 映射
2. **INTENT_CATALOGUE** — 更新相关 intent 的 `skills` 列表，使用新 slug

## 验证脚本注意事项

文件：`scripts/validate-skills.py`

已知已修复的坑：
- 多段连字符层级名（如 `project-unit`）需要渐进式匹配 `ALLOWED_LEVELS`
- `fills_slots_for: null` 的 YAML null 会被简单解析器识别为字符串 `"null"`，需过滤

## 项目文件路径

```
项目根目录: /Volumes/T7 Shield/AI workspace/10_projects/active/china-construction-fintax-skills/

核心目录:
  skills/                         ← 所有技能文件
  skills/financial-reporting/     ← Phase 2 新建文件放这里
  skills/china-construction/      ← Phase 1 旧文件（待迁移）
  skills/intelligence/            ← 法规知识（按监管机构分）
  skills/foundation/              ← 跨领域工作流基础
  mcp/ccfts_mcp/server.py         ← MCP 服务器
  scripts/validate-skills.py      ← 验证脚本
  notes/                          ← 项目文档和笔记
```

---

**给接手 AI 的指示**：

请按照上述规范，从优先级最高的 `ccfts-entity-type-rules` 开始拆分。先阅读旧文件理解内容，识别 Type A vs Type B 的差异点作为 SLOT，然后创建 Base + 2 个覆盖文件。每完成一个拆分就跑验证脚本确保通过。
