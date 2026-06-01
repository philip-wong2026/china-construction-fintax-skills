# Demo: 项目部/总包部资料检查

## 目的

演示 AI 在处理项目部或总包部资料前，如何先识别主体边界、资料范围和人工复核事项。

这个 demo 不是为了说明“检查报表口径本身有多大管理价值”，而是为了说明：AI 如果把非法人项目部当成独立法人公司处理，后面的收入、成本、权益、税务义务和责任主体判断都会偏。

## 场景

某总包部是企业内部设立的项目管理单位，不是独立法人。它需要整理月度经营和财务资料，用于内部管理、项目分析和上级复核。

这个场景重点不是“做一张漂亮报表”，而是让 AI 先识别：

- 这是项目部/总包部，不是独立法人公司。
- 它更强调项目履约、成本、回款、内部往来和责任边界。
- 输出结果只能作为内部检查草稿，不能替代正式报表和人工判断。

## 输入文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 科目余额表 | `input/trial-balance.csv` | 脱敏教学样例，含施工特有科目 |
| 期望利润表 | `expected/quick-report-pnl.csv` | 基于样例余额表手工整理的 expected 输出 |
| 期望资产负债表 | `expected/quick-report-bs.csv` | 基于样例余额表手工整理的 expected 输出，资产≈负债 |

## 应加载的技能（按顺序）

1. `ccfts-workflow-base`
2. `ccfts-fr-all-flash-report-workflow`
3. `ccfts-fr-all-entity-type-rules` → `ccfts-fr-project-unit-entity-type-rules`
4. `ccfts-acct-all-chart-of-accounts` → `ccfts-acct-project-unit-chart-of-accounts`
5. `ccfts-fr-all-rounding-rules` → `ccfts-fr-project-unit-rounding-rules`
6. `ccfts-fr-all-profit-statement` → `ccfts-fr-project-unit-profit-statement`
7. `ccfts-fr-all-balance-sheet` → `ccfts-fr-project-unit-balance-sheet`
8. `ccfts-fr-all-quick-report-mapping` → `ccfts-fr-project-unit-quick-report-mapping`

## 期望输出

| 输出项 | 内容 |
|--------|------|
| 主体边界判断 | 项目部/总包部，属于非法人内部管理单位，不应简单按独立法人公司处理 |
| 利润表 | 营业收入(6001)→利润总额(=净利润)→无所得税 |
| 资产负债表 | 资产=负债（权益≈0，允许 ±1 万噪音） |
| 审核者摘要 | 主体边界/期间/资料缺口/差异分析/人工复核点 |

## 如何判断结果合理

- 利润表：净利润 = 利润总额（无 6801 所得税费用）
- 资产负债表：资产总计 ≈ 负债总计（权益 ≈ 0）
- 取整：资产负债表所有行 ROUND_DOWN（截尾），利润表 ROUND_HALF_UP
- 其他应付款：ROUND_DOWN(2241-01) + ROUND_DOWN(3001)，非倒推
- 应付账款：ROUND_DOWN(2202) − ROUND_DOWN(1123)

## 当前限制

- 本 demo 全部数据均为脱敏教学样例，只用于演示流程。
- 输入科目余额表为简化演示数据，用于演示规则和测试 expected 表内等式；尚未覆盖完整国资委快报模板。
- 总包部的 12 月本月数（D 列）逻辑取决于具体结账方式，demo 暂按"本期=全年累计"处理。
