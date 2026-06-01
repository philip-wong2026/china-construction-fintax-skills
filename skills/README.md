# CCFTS 技能导航地图

本目录是 CCFTS 的核心：97 个给 AI 读取的施工企业财税 skill 文件。

如果你是普通业务用户，不建议从本目录开始。请先看 [../README.md](../README.md)、[../docs/quick-start-10min.md](../docs/quick-start-10min.md) 或 [../agent-packs/](../agent-packs/)。

## 目录怎么组织

这些 skill 按“业务领域 + 主体层级”组织。

业务领域包括：

| 领域 | 目录 | 说明 |
| --- | --- | --- |
| 财务报表 | `financial-reporting/` | 快报、决算、合并报表、报表映射 |
| 会计核算 | `accounting/` | 收入确认、合同成本、质保金、科目表 |
| 税务申报 | `tax/` | 增值税、企业所得税、印花税、跨境税务 |
| 经营分析 | `analysis/` | 盈利能力、现金流、两金、预算偏差 |
| 管理办法 | `management/` | 成本控制、清收清欠、资金池、内控 |
| 法规知识库 | `intelligence/` | 国资监管、财政部、税务、住建等公开规则 |
| 工作流基础 | `foundation/` | 通用工作流、技能索引和正式 Word 输出格式 |

主体层级包括：

| 层级目录 | 普通理解 |
| --- | --- |
| `soe-group/` | 集团、股份公司、上市公司合并层面 |
| `subsidiary/` | 独立法人子公司、工程局、工程公司 |
| `branch/` | 分公司、区域分支机构 |
| `project-unit/` | 项目部、总包部、局指、代局指 |
| `spv/` | 为项目设立的独立法人项目公司 |
| `enterprise/` | 企业级通用规则 |
| `small-enterprise/` | 小型企业或简化场景 |
| `intl/` | 境外工程 |
| `_base/` 或 `all` | 跨层级通用规则 |

## 文件名怎么看

文件名遵循这个结构：

```text
ccfts-{业务领域}-{主体层级}-{主题}.md
```

例如：

| 文件 | 普通理解 |
| --- | --- |
| `ccfts-fr-all-flash-report-workflow.md` | 施工企业财务快报处理流程 |
| `ccfts-fr-project-unit-balance-sheet.md` | 项目部/总包部资产负债表规则 |
| `ccfts-fr-spv-balance-sheet.md` | 项目公司资产负债表规则 |
| `ccfts-tax-all-vat-cross-region-prepayment.md` | 增值税跨区域预缴规则 |
| `ccfts-tax-all-cit-prepayment-filing.md` | 企业所得税预缴规则 |
| `ccfts-mgmt-project-unit-collection-clear-arrears.md` | 项目清收清欠管理 |

目录名里仍保留 `spv`、`vat`、`cit` 这类英文缩写，是为了保持文件名稳定，方便程序和 MCP 调用。面向普通用户的说明中，会尽量使用“项目公司”“增值税”“企业所得税”等中文表达。

## 什么时候加载哪个 skill

不要一次把全部 97 个文件都塞给 AI。更稳妥的方式是：

1. 先说清楚业务场景。
2. 让 AI 判断需要哪些 skill。
3. 每次只加载 3-8 个相关文件。
4. 同时提供项目背景包和脱敏业务资料。

常用入口：

| 你要做什么 | 优先看 |
| --- | --- |
| 检查财务快报资料 | `financial-reporting/_base/ccfts-fr-all-flash-report-workflow.md` |
| 判断主体是项目部还是项目公司 | `financial-reporting/_base/ccfts-fr-all-entity-type-rules.md` |
| 算或检查增值税 | `tax/_base/ccfts-tax-all-vat-general-filing.md` |
| 判断增值税跨区域预缴 | `tax/_base/ccfts-tax-all-vat-cross-region-prepayment.md` |
| 判断企业所得税预缴 | `tax/_base/ccfts-tax-all-cit-prepayment-filing.md` |
| 做项目盈利分析 | `analysis/project-unit/ccfts-anlys-project-unit-profitability.md` |
| 做项目现金流分析 | `analysis/project-unit/ccfts-anlys-project-unit-cashflow.md` |
| 做清收清欠 | `management/project-unit/ccfts-mgmt-project-unit-collection-clear-arrears.md` |
| 处理质保金 | `financial-reporting/_base/ccfts-fr-all-retention-money.md` |
| 做竣工结算 | `financial-reporting/_base/ccfts-fr-all-final-account-settlement.md` |
| 做合并报表 | `financial-reporting/_base/ccfts-fr-all-consolidation-workflow.md` |

更完整的场景选择见 [../START_HERE.md](../START_HERE.md)。

## 当前质量状态

当前版本是公开试验版。

- 97 个 skill 均通过结构检查。
- 当前质量等级为 `research-verified`：基于公开法规、公开行业资料和脱敏实务经验整理。
- 尚未形成持证注册会计师、税务师或企业专家逐条签署的正式审核记录。
- 不能直接替代正式财税意见、审计意见、纳税申报或企业审批。

建议把它当成：

- AI 辅助资料整理工具。
- 财税检查清单生成工具。
- 新人学习和复核辅助工具。
- 企业内部 AI 知识库的专业素材。

不要把它当成：

- 自动报税软件。
- 自动出具财务报表的软件。
- 不需要人工判断的合规系统。

## 验证方式

如果你会使用命令行，可以运行：

```bash
python3 scripts/validate-skills.py
python3 tests/test_demo_contracts.py
python3 tests/test_skill_integrity.py
python3 tests/test_mcp_loading.py
```

如果你不会使用命令行，只需要记住：正式使用前请结合 [../docs/manual-review-template.md](../docs/manual-review-template.md) 做人工复核。
