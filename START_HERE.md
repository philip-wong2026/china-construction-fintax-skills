# CCFTS 从这里开始

> 本页是“已经大概知道 CCFTS 是什么，准备拿它做一次具体业务试用”的入口。所有输出都只是辅助分析，不能替代企业正式审批、注册会计师、税务师、律师或审计人员意见。

如果你第一次看到这个项目，请先读：

1. [README.md](README.md)：先理解项目价值和边界。
2. [docs/quick-start-10min.md](docs/quick-start-10min.md)：按 10 分钟路径试一次。
3. [docs/context-pack-template.md](docs/context-pack-template.md)：填写你的项目背景包。

如果你只会用豆包、马维斯这类桌面 AI 助手，请优先使用 [agent-packs/](agent-packs/) 中的场景包，不要一开始就研究全部 96 个 skill。

## 它怎么用

CCFTS 的核心是一批中文 Markdown 技能文件。你可以把它理解为“给 AI 看的施工企业财税作业指导书”。

最常见的使用方式有三种：

| 用法 | 适合谁 | 怎么做 |
| --- | --- | --- |
| 场景包 | 豆包、马维斯、手机端 AI 用户 | 上传 `agent-packs/` 里的一个场景包，再上传脱敏资料 |
| 直接读文件 | Codex、Claude Code、Cursor、Trae Solo 用户 | 让 AI 读取本仓库，并按本页选择相关 skill |
| MCP 接入 | 熟悉 AI agent 配置的高级用户 | 按 [mcp/SMOKE_TEST.md](mcp/SMOKE_TEST.md) 配置本地 MCP |

无论哪种方式，都建议同时提供 [项目背景包](docs/context-pack-template.md)。skill 只告诉 AI 行业方法，背景包才告诉 AI 你这次处理的具体主体、期间、资料和边界。

## 6 个常用场景

### 场景 1：检查施工企业财务快报资料

**适合**：项目财务、报表人员、财务共享中心、AI agent。

**先让 AI 读取这些 skill**：

1. `ccfts-workflow-base`：通用工作流。
2. `ccfts-fr-all-flash-report-workflow`：快报资料处理流程。
3. `ccfts-fr-all-entity-type-rules`：判断主体是项目部、项目公司、分公司、子公司还是集团层级。
4. 对应主体层级的规则文件，例如项目部用 `ccfts-fr-project-unit-entity-type-rules`，项目公司用 `ccfts-fr-spv-entity-type-rules`。
5. `ccfts-acct-all-chart-of-accounts`：科目表基础规则。
6. `ccfts-fr-all-profit-statement`、`ccfts-fr-all-balance-sheet`、`ccfts-fr-all-quick-report-mapping`：利润表、资产负债表和科目映射。

**你要提供**：

- 科目余额表或脱敏样表。
- 报表期间。
- 主体说明：项目部、项目公司、分公司、子公司或集团汇总层。
- 是否季度末、年末。
- 如有企业原报表结果，可以作为对照。

**希望 AI 输出**：

- 主体边界判断和判断依据。
- 科目到报表项目的映射思路。
- 利润表、资产负债表草稿或检查清单。
- 缺失资料、异常点、人工复核清单。

**必须人工复核**：

- 主体层级是否与实际组织架构一致。
- 报表口径是否符合本单位制度。
- 重大差异是否已经解释。
- AI 有没有把不确定事项说成确定结论。

### 场景 2：判断增值税一般计税、简易计税和跨区域预缴

**适合**：项目财务、税务岗、共享中心税务人员。

**先让 AI 读取这些 skill**：

1. `ccfts-intel-sta-vat-law-2026`：增值税法 2026 相关规则。
2. `ccfts-tax-all-vat-general-filing`：一般计税。
3. `ccfts-tax-all-vat-simplified-filing`：简易计税。
4. `ccfts-tax-all-vat-cross-region-prepayment`：跨区域预缴。
5. 如需子公司申报，再读取 `ccfts-tax-subsidiary-vat-filing`。

**你要提供**：

- 项目所在地和机构所在地。
- 纳税人身份：一般纳税人或小规模纳税人。
- 合同类型：纯施工、清包工、甲供、EPC、PPP 等。
- 合同日期、开票、收款、结算、分包扣除资料。

**希望 AI 输出**：

- 是否跨区域施工。
- 适用一般计税、简易计税或无法判断。
- 预缴税额测算和附加税费提示。
- 缺失信息、地方口径风险、人工复核清单。

**必须人工复核**：

- 合同事实是否支持简易计税。
- 项目所在地税务机关是否有特殊要求。
- 分包扣除凭证是否合规。
- 申报结果是否经过税务岗确认。

### 场景 3：判断企业所得税预缴和汇算风险

**适合**：子公司、工程局、工程公司财务和税务人员。

**先让 AI 读取这些 skill**：

1. `ccfts-intel-sta-cit-prepayment-rules`：企业所得税预缴规则。
2. `ccfts-tax-all-cit-prepayment-filing`：季度预缴和年度汇算。
3. `ccfts-tax-subsidiary-cit-filing`：子公司级申报。
4. `ccfts-fr-all-entity-type-rules`：确认是否为独立法人。

**你要提供**：

- 是否为独立法人。
- 当期利润表或利润测算。
- 是否有跨省施工项目。
- 安全生产费、资产减值、研发费用等纳税调整资料。

**希望 AI 输出**：

- 是否需要独立预缴。
- 季度预缴测算思路。
- 常见纳税调整清单。
- 汇算清缴风险提示和人工复核清单。

**必须人工复核**：

- 是否符合企业所得税优惠条件。
- 安全生产费、减值准备等税会差异是否准确。
- 跨省项目预缴是否足额。

### 场景 4：做项目经营分析、现金流分析和亏损预警

**适合**：项目财务、项目经理部、商务经营人员、公司经营分析岗。

**先让 AI 读取这些 skill**：

1. `ccfts-anlys-project-unit-profitability`：项目盈利能力分析。
2. `ccfts-anlys-project-unit-cashflow`：现金流分析。
3. `ccfts-anlys-all-budget-variance`：预算偏差分析。
4. `ccfts-mgmt-project-unit-cost-control`：责任成本控制。
5. `ccfts-acct-all-contract-cost`：合同履约成本归集。
6. `ccfts-acct-enterprise-contract-cost`：预计总成本和亏损合同。

**你要提供**：

- 责任成本预算。
- 实际成本、收入、结算、收款、付款资料。
- 已完工未结算、已结算未收款、分包结算等资料。

**希望 AI 输出**：

- 收入、成本、毛利、现金流、垫资、两金的分析框架。
- 预算偏差和异常项。
- 亏损风险、回款风险、下一步动作建议。

**必须人工复核**：

- 成本数据是否完整。
- 偏差原因是量差、价差、范围变化还是管理责任。
- 亏损合同是否需要正式计提预计损失。

### 场景 5：处理质保金、竣工结算和清收清欠

**适合**：项目部、商务、财务、清收清欠人员。

**先让 AI 读取这些 skill**：

1. `ccfts-fr-all-retention-money`：质保金处理。
2. `ccfts-acct-enterprise-quality-guarantee`：质保金会计处理。
3. `ccfts-fr-all-final-account-settlement`：竣工结算流程。
4. `ccfts-mgmt-project-unit-collection-clear-arrears`：清收清欠。

**你要提供**：

- 合同质保金条款。
- 竣工结算资料、审计审定资料、审减明细。
- 应收账款、合同资产、质保金台账。
- 已催收记录和责任部门。

**希望 AI 输出**：

- 质保金扣留、到期、回收和风险清单。
- 竣工结算差异和收入调整提示。
- 清收清欠分层清单和下一步动作。

**必须人工复核**：

- 质保金比例和缺陷责任期是否符合合同和法规。
- 审减争议是否已经形成正式依据。
- 红字发票、收入调整、坏账判断是否经过专业确认。

### 场景 6：做合并报表或集团层面分析

**适合**：集团财务、合并岗、上市公司财务、总部经营分析岗。

**先让 AI 读取这些 skill**：

1. `ccfts-fr-all-consolidation-workflow`：合并报表工作流。
2. `ccfts-fr-all-consolidation-report`：合并抵销。
3. `ccfts-intel-mof-cas33-consolidation`：企业会计准则第 33 号。
4. `ccfts-anlys-soe-group-kpi-dashboard`：集团经营看板。
5. `ccfts-anlys-soe-group-two-funds-analysis`：两金分析。
6. `ccfts-mgmt-soe-group-cash-pooling`：资金池。

**你要提供**：

- 母公司和子公司单户数据。
- 合并范围清单。
- 持股比例、控制判断依据。
- 内部往来、内部交易和项目公司资料。

**希望 AI 输出**：

- 合并范围判断清单。
- 抵销分录思路。
- 两金、资产负债率、经营指标分析。
- 需要人工确认的重大事项。

**必须人工复核**：

- 合并范围变更是否合理。
- 内部往来是否全额抵销。
- 项目公司是否需要纳入合并范围。
- 少数股东权益和损益是否正确。

## 每次使用都要问 AI 的 5 个问题

你可以把下面这段复制给 AI：

```text
请使用 CCFTS 的相关 skill 辅助处理本次资料。

输出前请先回答：
1. 你判断本次主体是什么？依据是什么？
2. 你还缺哪些资料？
3. 哪些结论是确定的，哪些只是推断？
4. 哪些风险必须人工复核？
5. 哪些内容不能用于正式报送或申报？
```

## 人工复核总则

所有场景的 AI 输出都必须人工复核。尤其是税务申报、审计资料、监管报送、财务报告、融资、招投标和重大经营决策，不能直接使用 AI 结论。

更多复核工具见：

- [docs/manual-review-template.md](docs/manual-review-template.md)：人工复核模板。
- [docs/evidence-levels.md](docs/evidence-levels.md)：可信度分级。
- [docs/validation-plan.md](docs/validation-plan.md)：验证计划。

## 快速索引

全部 skill 的技术索引见 [skills/README.md](skills/README.md) 和 `skills/foundation/ccfts-all-skill-index.md`。

## 免责声明

本项目仅用于辅助分析、资料整理、检查清单生成和 AI 工作流组织，不构成法律、税务、审计、会计、投资或合规意见。使用者必须结合最新法规、地方口径和企业制度进行人工复核。
