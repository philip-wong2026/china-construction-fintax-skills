# Demo: SPV（项目公司/投资管理类）快报编制

## 目的

验证 CCFTS 技能对 Type A（投资管理类/SPV）主体从科目余额表→财务快报的完整编制流程。

## 场景

某项目公司 SPV 需要在月末编制 SASAC 月度财务快报。该公司为独立法人，主营投资管理，科目余额表不含施工类科目（5801/5601/2202）。

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
| 主体类型判定 | Type A（投资管理类），置信度 ≥ 90% |
| 利润表 | 营业收入(6051)→净利润 完整计算链 |
| 资产负债表 | 资产=负债+权益（允许 ±1 万噪音） |
| 审核者摘要 | 主体类型/期间/填充统计/差异分析 |

## 如何判断结果合理

- 利润表：净利润 = 利润总额 − 所得税费用；净利润 ≈ 4105-14 净发生额
- 资产负债表：资产总计 = 负债合计 + 所有者权益合计（±1 万）
- 取整：全局 ROUND_HALF_UP
- 其他应付款：使用倒推法（负债合计 − 税费 − 薪酬），非直接取 2241

## 当前限制

- **All data in this demo is synthetic, generated for pipeline validation only.**
- 输入科目余额表为简化演示数据，用于演示规则和测试 expected 表内等式；尚未覆盖完整 SASAC 快报模板。
- 本 demo 未覆盖：现金流量表、业务板块表、财政部快报 Sheet。

## 参考

- 已验证匹配率：某项目公司 Q4 2025 快报 99.2% 匹配（123 单元格，0 实质性差异）
