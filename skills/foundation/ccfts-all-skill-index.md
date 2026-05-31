---
name: ccfts-all-skill-index
description: >
  CCFTS 技能总索引——按任务场景快速路由到对应技能文件。
  加载本文件以了解全局技能分布和快速查找路径。触发条件：不知道加载哪个技能时先看这个。
version: 0.2
jurisdiction: CN
tax_year: 2025
category: foundation
domains: [foundation]
quality_tier: research-verified
verified_by: pending
entity_levels: [all]
enterprise_scales: [large-soe]
depends_on: []
references: []
is_base: false
fills_slots_for: null
slots: []
triggers:
  - 技能索引
  - 有哪些技能
  - skill index
  - 帮助
  - help
---

# CCFTS 技能总索引

> 按任务场景快速路由。每个场景列出推荐加载的技能 slug 列表，先 Base 文件再层级覆盖文件。

## 财务报告类

| 任务场景 | 推荐加载的技能 |
|---------|--------------|
| 编制月度财务快报 | `ccfts-workflow-base` → `ccfts-fr-all-flash-report-workflow` → `ccfts-fr-all-entity-type-rules` → 对应层级覆盖 |
| 编制利润表 | `ccfts-fr-all-profit-statement` → `ccfts-fr-all-entity-type-rules` → 对应层级覆盖 |
| 编制资产负债表 | `ccfts-fr-all-balance-sheet` → `ccfts-fr-all-entity-type-rules` → 对应层级覆盖 |
| 判定主体类型 | `ccfts-fr-all-entity-type-rules` → 对应层级覆盖 |
| 科目余额表映射到快报 | `ccfts-fr-all-quick-report-mapping` → `ccfts-acct-all-chart-of-accounts` |
| 取整规则/±1万诊断 | `ccfts-fr-all-rounding-rules` → 对应层级覆盖 |
| 非季度末调整 | `ccfts-fr-all-period-end-adjustments` → 对应层级覆盖 |
| 年度财务决算 | `ccfts-fr-all-annual-settlement-workflow` → `ccfts-intel-sasac-annual-settlement` |
| 合并报表编制 | `ccfts-fr-all-consolidation-workflow` → `ccfts-fr-all-consolidation-report` → `ccfts-intel-mof-cas33-consolidation` |
| 质保金处理 | `ccfts-fr-all-retention-money` → `ccfts-acct-enterprise-quality-guarantee` |
| 竣工结算流程 | `ccfts-fr-all-final-account-settlement` → `ccfts-fr-all-retention-money` |
| 项目交付模式选择（EPC/专项债/PPP） | `ccfts-fr-all-project-delivery-modes` → `ccfts-intel-mof-epc-accounting` → `ccfts-intel-mof-special-bond-project` |
| 政府补贴处理 | `ccfts-fr-all-government-subsidy-treatment` → `ccfts-intel-mof-government-subsidies` |

## 会计核算类

| 任务场景 | 推荐加载的技能 |
|---------|--------------|
| 合同履约成本归集/结转 | `ccfts-acct-all-contract-cost` → `ccfts-intel-mof-cas14-revenue` |
| 预计总成本调整/亏损合同 | `ccfts-acct-enterprise-contract-cost` → `ccfts-acct-all-contract-cost` |
| 安全生产费计提/使用分录 | `ccfts-acct-enterprise-safety-fund` → `ccfts-intel-mohurd-safety-fund-rates` |
| 关联交易处理 | `ccfts-acct-enterprise-related-party-transactions` → `ccfts-intel-mof-cas33-consolidation` |
| 变更索赔确认 | `ccfts-acct-enterprise-contract-variations-claims` → `ccfts-intel-mof-cas14-revenue` |
| 工程保险理赔 | `ccfts-acct-enterprise-insurance-claims` |
| 质保金分录实操 | `ccfts-acct-enterprise-quality-guarantee` → `ccfts-fr-all-retention-money` |
| 科目表查询 | `ccfts-acct-all-chart-of-accounts` → 对应层级覆盖 |
| 中型企业简化报表 | `ccfts-acct-enterprise-medium-simplified-reporting` → `ccfts-intel-mof-small-enterprise-standards` |
| 个体施工队/挂靠 | `ccfts-acct-small-enterprise-individual-contractor` → `ccfts-intel-mof-small-enterprise-standards` |
| 境外外币折算 | `ccfts-acct-intl-foreign-currency-translation` → `ccfts-intel-mof-cas33-consolidation` |
| 境外内外账调节 | `ccfts-acct-intl-dual-books-reconciliation` → `ccfts-acct-intl-foreign-currency-translation` |

## 税务申报类

| 任务场景 | 推荐加载的技能 |
|---------|--------------|
| VAT 月度申报（一般计税） | `ccfts-tax-all-vat-general-filing` → `ccfts-intel-sta-vat-law-2026` |
| 跨区域 VAT 预缴 | `ccfts-tax-all-vat-cross-region-prepayment` → `ccfts-intel-sta-vat-law-2026` |
| 简易计税（清包工） | `ccfts-tax-all-vat-simplified-filing` → `ccfts-intel-sta-vat-law-2026` |
| CIT 预缴/汇算 | `ccfts-tax-all-cit-prepayment-filing` → `ccfts-intel-sta-cit-prepayment-rules` |
| 印花税（施工合同） | `ccfts-tax-all-stamp-tax` |
| 全电发票开票/红冲 | `ccfts-tax-all-e-invoice-operations` → `ccfts-intel-sta-e-invoice-mandate` |
| 小规模纳税人 VAT | `ccfts-tax-enterprise-small-scale-taxpayer` |
| 小型微利 CIT 优惠 | `ccfts-tax-small-enterprise-cit-micro` |
| SPV 房产税/土地使用税 | `ccfts-tax-spv-property-tax` |
| 子公司 VAT 月度申报 | `ccfts-tax-subsidiary-vat-filing` → `ccfts-tax-all-vat-general-filing` |
| 子公司 CIT 汇算清缴 | `ccfts-tax-subsidiary-cit-filing` → `ccfts-tax-all-cit-prepayment-filing` |
| 境外预提税/税收抵免 | `ccfts-tax-intl-cross-border-withholding` → `ccfts-acct-intl-foreign-currency-translation` |

## 经济活动分析类

| 任务场景 | 推荐加载的技能 |
|---------|--------------|
| 一利五率指标分析 | `ccfts-anlys-all-one-profit-five-rates` → `ccfts-intel-sasac-one-profit-five-rates` |
| 预算偏差分析 | `ccfts-anlys-all-budget-variance` → `ccfts-mgmt-project-unit-cost-control` |
| 集团经营看板 | `ccfts-anlys-soe-group-kpi-dashboard` |
| "两金"结构分析 | `ccfts-anlys-soe-group-two-funds-analysis` → `ccfts-fr-all-retention-money` |
| 项目盈利能力分析 | `ccfts-anlys-project-unit-profitability` → `ccfts-mgmt-project-unit-cost-control` |
| 项目现金流分析 | `ccfts-anlys-project-unit-cashflow` → `ccfts-intel-sasac-one-profit-five-rates` |

## 管理办法类

| 任务场景 | 推荐加载的技能 |
|---------|--------------|
| 内部控制框架 | `ccfts-mgmt-all-internal-control` |
| 代局指管理 | `ccfts-mgmt-all-delegated-headquarters` → `ccfts-acct-enterprise-related-party-transactions` |
| 资金池管理 | `ccfts-mgmt-soe-group-cash-pooling` → `ccfts-acct-enterprise-related-party-transactions` |
| 国家审计配合 | `ccfts-mgmt-soe-group-government-audit` |
| 全面预算管理 | `ccfts-mgmt-soe-group-budget-approval` → `ccfts-intel-sasac-one-profit-five-rates` |
| 国有资本经营预算 | `ccfts-mgmt-soe-group-state-capital-budget` → `ccfts-intel-sasac-state-capital-budget` |
| 项目成本控制 | `ccfts-mgmt-project-unit-cost-control` → `ccfts-acct-all-contract-cost` |
| 分包管理 | `ccfts-mgmt-project-unit-subcontract` |
| 清收清欠 | `ccfts-mgmt-project-unit-collection-clear-arrears` → `ccfts-fr-all-retention-money` |
| 小型企业内控 | `ccfts-mgmt-small-enterprise-internal-control-lite` |

## 法规查询类

| 任务场景 | 推荐加载的技能 |
|---------|--------------|
| SASAC 快报截止日期 | `ccfts-intel-sasac-flash-report-deadlines` |
| 一利五率考核指标 | `ccfts-intel-sasac-one-profit-five-rates` |
| 国有资本经营预算政策 | `ccfts-intel-sasac-state-capital-budget` |
| 年度决算要求 | `ccfts-intel-sasac-annual-settlement` |
| CAS 14 收入准则 | `ccfts-intel-mof-cas14-revenue` |
| CAS 33 合并准则 | `ccfts-intel-mof-cas33-consolidation` |
| 小企业会计准则 | `ccfts-intel-mof-small-enterprise-standards` |
| EPC 会计处理 | `ccfts-intel-mof-epc-accounting` |
| 专项债项目政策 | `ccfts-intel-mof-special-bond-project` |
| 政府补贴准则 | `ccfts-intel-mof-government-subsidies` |
| 增值税法 2026 | `ccfts-intel-sta-vat-law-2026` |
| 金税四期 | `ccfts-intel-sta-golden-tax-phase4` |
| 全电发票规定 | `ccfts-intel-sta-e-invoice-mandate` |
| CIT 预缴规则 | `ccfts-intel-sta-cit-prepayment-rules` |
| 建筑业资质体系 | `ccfts-intel-mohurd-qualification-system` |
| 安全生产费计提标准 | `ccfts-intel-mohurd-safety-fund-rates` |

## 免责声明

本索引文件为任务场景路由参考。实际技能加载可能因具体项目情况不同而需要组合更多或更少的文件。
