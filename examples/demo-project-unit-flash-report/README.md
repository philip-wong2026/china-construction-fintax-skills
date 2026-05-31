# Demo: 项目部/总包部（施工总承包类）快报编制

## 目的

验证 CCFTS 技能对 Type B（施工总承包类/总包部）主体从科目余额表→财务快报的完整编制流程。

## 场景

某总包部（非法人内部管理单位）需要在月末编制内部管理用财务快报。该主体有完整施工科目（5801/5601/2202/2701/3001/1126），权益≈0（资产=负债）。

## 输入文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 科目余额表 | `input/trial-balance-sample.xlsx` | 标准列位格式，含施工特有科目 |
| 快报模板 | `input/quick-report-template.xlsx` | SASAC 快报导入模板 |

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
| 主体类型判定 | Type B（施工总承包类），置信度 ≥ 90%（检测到 5801/6001/6401） |
| 利润表 | 营业收入(6001)→利润总额(=净利润)→无所得税 |
| 资产负债表 | 资产=负债（权益≈0，允许 ±1 万噪音） |
| 审核者摘要 | 主体类型/期间/填充统计/差异分析 |

## 如何判断结果合理

- 利润表：净利润 = 利润总额（无 6801 所得税费用）
- 资产负债表：资产总计 ≈ 负债总计（权益 ≈ 0）
- 取整：资产负债表所有行 ROUND_DOWN（截尾），利润表 ROUND_HALF_UP
- 其他应付款：ROUND_DOWN(2241-01) + ROUND_DOWN(3001)，非倒推
- 应付账款：ROUND_DOWN(2202) − ROUND_DOWN(1123)

## 当前限制

- **All data in this demo is synthetic, generated for pipeline validation only.**
- 输入科目余额表为简化演示数据，总包部实际权益≈0、资产≈负债。
- 总包部的 12 月本月数（D 列）逻辑取决于具体结账方式，demo 暂按"本期=全年累计"处理。
