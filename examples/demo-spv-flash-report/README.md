# Demo: 项目公司资料检查

## 目的

演示 AI 在处理项目公司资料时，如何先识别它是“为项目设立的独立法人公司”，而不是项目部或总包部。

本 demo 讲的是**项目公司/投资管理类主体**，重点是独立法人公司的责任边界。

## 场景

某项目公司是为投资建设某个项目设立的独立法人公司。它和项目部不同，通常要关注资产、负债、权益、融资、投资回收、税务义务和公司治理。

这个场景重点不是比较两套表有什么不同，而是让 AI 先识别：

- 它是独立法人项目公司，不是项目部。
- 它有自己的资产、负债、权益和税务义务。
- 它的分析重点不应只停留在施工履约，还要关注资本投入、债务、现金流和公司层面风险。

## 输入文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 科目余额表 | `input/trial-balance.csv` | 脱敏教学样例（科目代码/名称/期初方向/期初余额/本期借方/本期贷方/期末方向/期末余额） |
| 期望利润表 | `expected/quick-report-pnl.csv` | 基于样例余额表手工整理的 expected 输出 |
| 期望资产负债表 | `expected/quick-report-bs.csv` | 基于样例余额表手工整理的 expected 输出，资产=负债+权益 |

## 应加载的技能（按顺序）

1. `ccfts-workflow-base`
2. `ccfts-fr-all-flash-report-workflow`
3. `ccfts-fr-all-entity-type-rules` → `ccfts-fr-spv-entity-type-rules`
4. `ccfts-acct-all-chart-of-accounts` → `ccfts-acct-spv-chart-of-accounts`
5. `ccfts-fr-all-rounding-rules` → `ccfts-fr-spv-rounding-rules`
6. `ccfts-fr-all-profit-statement` → `ccfts-fr-spv-profit-statement`
7. `ccfts-fr-all-balance-sheet` → `ccfts-fr-spv-balance-sheet`
8. `ccfts-fr-all-quick-report-mapping` → `ccfts-fr-spv-quick-report-mapping`

## 期望输出

| 输出项 | 内容 |
|--------|------|
| 主体边界判断 | 项目公司/投资管理类主体，属于独立法人，不应按项目部口径处理 |
| 利润表 | 营业收入(6051)→净利润 完整计算链 |
| 资产负债表 | 资产=负债+权益（允许 ±1 万噪音） |
| 审核者摘要 | 主体边界/期间/资料缺口/差异分析/人工复核点 |

## 如何判断结果合理

- 利润表：净利润 = 利润总额 − 所得税费用；净利润 ≈ 4105-14 净发生额
- 资产负债表：资产总计 = 负债合计 + 所有者权益合计（±1 万）
- 取整：全局 ROUND_HALF_UP
- 其他应付款：使用倒推法（负债合计 − 税费 − 薪酬），非直接取 2241

## 当前限制

- 本 demo 全部数据均为脱敏教学样例，只用于演示流程。
- 输入科目余额表为简化演示数据，用于演示规则和测试 expected 表内等式；尚未覆盖完整国资委快报模板。
- 本 demo 未覆盖：现金流量表、业务板块表、财政部快报 Sheet。

## 参考

- 本 demo 是入门样例。更有管理深度的验证案例，应继续补充资金计划、投资回收、融资约束和公司治理风险。
