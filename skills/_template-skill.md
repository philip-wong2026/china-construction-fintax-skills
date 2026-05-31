---
name: ccfts-{domain}-{level}-{topic}
description: >
  一句话描述该技能何时触发。包含触发关键词（中文和英文）。
version: 0.1
jurisdiction: CN
tax_year: 2025
category: financial-reporting
quality_tier: research-verified
verified_by: pending
domains: [financial-reporting]         # 职能领域
entity_levels: [project-unit]         # 适用组织层级
enterprise_scales: [large-soe]        # 企业规模
depends_on:                           # 依赖的技能文件
  - ccfts-workflow-base
references:                           # 引用的法规知识（从 intelligence/ 加载）
  - ccfts-intel-sta-vat-law-2026
is_base: false                         # 是否为 _base/ 工作流？
fills_slots_for: null                  # 如果填充SLOTs，指明base slug
slots: []                              # 如果定义了SLOTs，列出SLOT名
triggers:
  - 触发词1
  - 触发词2
---

  （技能正文）
-->

<!--
## 如何创建一个新技能

### 1. 确定位置
- domain: fr(报表) / acct(会计) / tax(税务) / anlys(分析) / mgmt(管理) / intel(法规)
- level: soe-group / subsidiary / branch / project-unit / spv / all(跨层级)
- topic: 连字符分隔的描述性短名

### 2. 填写 frontmatter
- `domains`: 所属职能领域（数组，可跨领域）
- `entity_levels`: 适用的组织层级（数组）
- `depends_on`: 必须加载的前置技能slug
- `references`: 引用的intelligence技能slug（自动加载法规上下文）
- `is_base`: true = 包含SLOTs占位符的工作流基础文件
- `fills_slots_for`: 指明填充哪个base文件的SLOTs

### 3. 正文结构
- 快速参考表（最核心的数值/规则一览）
- 主规则（按章节组织）
- 工作流步骤（1-2-3-4...）
- 自检清单（checkbox格式）
- 审核者摘要模板
- 参考材料/引用来源
- 免责声明

### 4. 遵守脱敏原则
**绝对不能**出现真实的企业名称、项目名称、地名、具体金额。
策略：用"某项目公司""某总包部""某集团"替代。

### 5. 运行验证
```bash
python3 scripts/validate-skills.py
```
-->
