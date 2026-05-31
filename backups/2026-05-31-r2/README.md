# CCFTS 技能导航地图

## 技能目录总览

本技能库按**职能领域 → 组织层级**二维组织，共 **96 个有效技能文件**：

```
职能领域 (domain)
  ├── _base/           ← 通用工作流 + SLOT 占位符
  ├── soe-group/       ← 央企集团/上市公司层级
  ├── subsidiary/      ← 独立法人子公司/工程局层级
  ├── branch/          ← 分公司（非法人）层级
  ├── project-unit/    ← 项目部/总包部/代局指层级
  ├── spv/             ← 项目公司SPV层级
  ├── enterprise/      ← 企业级通用（跨层级）
  ├── small-enterprise/← 小型企业
  ├── intl/            ← 境外工程
  └── all-*.md         ← 跨层级通用技能
```

## 领域目录

| 领域 | 缩写 | 目录 | 文件数 | 说明 |
|------|------|------|--------|------|
| 财务报表 | `fr` | `financial-reporting/` | 29 | 快报编制、决算、合并报表 |
| 会计核算 | `acct` | `accounting/` | 14 | 收入确认、合同成本、科目表 |
| 税务申报 | `tax` | `tax/` | 12 | VAT、CIT、印花税 |
| 经济活动分析 | `anlys` | `analysis/` | 6 | 一利五率、预算偏差 |
| 管理办法 | `mgmt` | `management/` | 10 | 内控、成本控制、代局指 |
| 法规知识库 | `intel` | `intelligence/` | 16 | 按监管机构组织 |
| 工作流基础 | — | `foundation/` | 2 | 跨领域通用工作流 + 技能总索引 |

## 组织层级说明

| 层级 | 缩写 | 法人地位 | 典型代表 |
|------|------|---------|---------|
| 央企集团/上市公司 | `soe-group` | 独立法人 | 股份公司合并层面 |
| 独立法人子公司 | `subsidiary` | 独立法人 | 工程局、工程公司 |
| 分公司 | `branch` | 非法人 | 区域分公司 |
| 项目部/总包部 | `project-unit` | 非法人 | 项目部、局指、代局指 |
| 项目公司SPV | `spv` | 独立法人 | PPP/BOT项目公司 |
| 企业级通用 | `enterprise` | — | 跨层级企业级规则 |
| 小型企业 | `small-enterprise` | — | 中小企业、个体户 |
| 境外工程 | `intl` | — | 境外施工项目 |

## 命名规范

```
ccfts-{domain}-{level}-{topic}.md

domain: fr(报表) / acct(会计) / tax(税务) / anlys(分析) / mgmt(管理) / intel(法规)
level:  soe-group / subsidiary / branch / project-unit / spv / all / enterprise / small-enterprise / intl

示例：
  ccfts-fr-all-rounding-rules.md              → 跨层级取整规则 Base
  ccfts-fr-spv-rounding-rules.md              → SPV 层级取整覆盖
  ccfts-tax-all-vat-general-filing.md         → VAT 一般计税申报
  ccfts-intel-sta-vat-law-2026.md             → 2026年增值税法法规
  ccfts-anlys-soe-group-two-funds-analysis.md → 集团"两金"分析
  ccfts-acct-intl-foreign-currency-translation.md → 境外外币折算
```

## 技能质量等级

| 等级 | 含义 | 当前状态 |
|------|------|---------|
| `research-verified` | 基于权威来源起草，待会计师审核 | **所有 90 个文件** |
| `accountant-verified` | 持证CPA审核并署名 | 暂无（待 CPA 审核） |

## 当前状态（2026-05-31）

**96 个技能文件，0 个验证问题，6 个职能领域全覆盖。首次发布候选。**

- 法规层（intelligence）：SASAC(4) + MOF(6) + STA(4) + MOHURD(2) = 16
- 财务报表（financial-reporting）：_base(14) + 5层覆盖(15) = 29
- 会计核算（accounting）：_base(2) + enterprise(7) + intl(2) + 其他(3) = 14
- 税务申报（tax）：_base(6) + spv(1) + subsidiary(2) + enterprise(1) + small-enterprise(1) + intl(1) = 12
- 经济活动分析（analysis）：_base(2) + soe-group(2) + project-unit(2) = 6
- 管理办法（management）：_base(2) + soe-group(4) + project-unit(3) + small-enterprise(1) = 10
- 工作流基础（foundation）：2（workflow-base v0.2 + skill-index）
- 旧文件（china-construction）：7（保持向后兼容，MCP 别名映射）

所有文件均通过验证脚本 v0.3（含 filename==name 校验），MCP 前端解析器已升级至与验证器一致的逻辑。

## 快速查找

- "我要编快报" → `financial-reporting/_base/ccfts-fr-all-flash-report-workflow.md`
- "取整规则是什么" → `financial-reporting/_base/ccfts-fr-all-rounding-rules.md`（Base）+ 对应层级覆盖
- "我要算增值税" → `tax/_base/ccfts-tax-all-vat-general-filing.md`
- "我要做合并报表" → `financial-reporting/_base/ccfts-fr-all-consolidation-workflow.md`
- "一利五率怎么分析" → `analysis/_base/ccfts-anlys-all-one-profit-five-rates.md`
- "项目部怎么控制成本" → `management/project-unit/ccfts-mgmt-project-unit-cost-control.md`
- "质保金怎么处理" → `financial-reporting/_base/ccfts-fr-all-retention-money.md`
- "竣工结算流程" → `financial-reporting/_base/ccfts-fr-all-final-account-settlement.md`
- "EPC/专项债/PPP 有什么区别" → `financial-reporting/_base/ccfts-fr-all-project-delivery-modes.md`
- "SASAC 截止日期" → `intelligence/sasac/ccfts-intel-sasac-flash-report-deadlines.md`
