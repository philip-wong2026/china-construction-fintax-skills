---
name: ccfts-acct-project-unit-chart-of-accounts
description: >
  项目部/总包部（施工总承包类，Type B）完整科目表。填充 ccfts-acct-all-chart-of-accounts 的 SLOT。
  触发条件：总包部/项目部/施工总承包类的科目查询和映射。
version: 0.2
jurisdiction: CN
tax_year: 2025
category: accounting
domains: [acct]
quality_tier: research-verified
verified_by: pending
entity_levels: [project-unit]
enterprise_scales: [large-soe]
depends_on:
  - ccfts-workflow-base
  - ccfts-fr-all-entity-type-rules
references:
  - ccfts-acct-all-chart-of-accounts
is_base: false
fills_slots_for: ccfts-acct-all-chart-of-accounts
slots: []
triggers:
  - 总包部科目表
  - 项目部科目
  - 施工总承包科目
---

# 项目部/总包部（施工总承包类/Type B）科目表

> 填充 `ccfts-acct-all-chart-of-accounts` 的 SLOT 占位符。

## SLOT 填充表

| SLOT | 填充值 |
|---|---|
| `{ENTITY_LABEL}` | **施工总承包类** |
| `{ENTITY_ALIAS}` | **总包部/项目部** |
| `{INCOME_ACCOUNT}` | **6001** |
| `{INCOME_NAME}` | **主营业务收入** |
| `{COST_ACCOUNT}` | **6401** |
| `{COST_NAME}` | **主营业务成本** |
| `{HAS_CONTRACT_ACCOUNTS}` | **有**（5801 合同结算 / 5601 合同履约成本） |
| `{HAS_AP}` | **有**（需减去 1123 预付账款） |
| `{HAS_LTP}` | **有**（融资租赁/分期付款采购设备） |
| `{HAS_INTERNAL}` | **有**（与其他内部单位往来） |
| `{HAS_PENDING_VAT}` | **有**（施工行业特有） |
| `{HAS_EQUITY}` | **无**（权益 ≈ 0，无 4001/4002/4101） |
| `{HAS_INVESTMENT_INCOME}` | **通常无** |
| `{HAS_OTHER_INCOME}` | **通常无** |
| `{HAS_INCOME_TAX}` | **通常无** |

## 项目部/总包部特有科目

### 施工特有科目（仅 Type B 有）

| 科目 | 名称 | 说明 |
|---|---|---|
| 5801 | 合同结算 | 最可靠的 Type B 信号，SPV 绝对没有 |
| 5601 | 合同履约成本 | 实际发生的建造成本 |
| 6001 | 主营业务收入 | 施工主业收入 |
| 6401 | 主营业务成本 | 施工主业成本 |
| 2202 | 应付账款 | 供应商/分包商应付款，需减去 1123 |
| 2701 | 长期应付款 | 融资租赁设备款等 |
| 3001 | 内部往来 | 与其他内部单位的往来款项（总包部特有） |
| 1126 | 待结算进项税额 | 施工行业待抵扣进项税 |

### 总包部没有的科目（区别于 SPV）

| 科目 | 名称 | 原因 |
|---|---|---|
| 6051 | 其他业务收入 | 非投资管理类 |
| 6402 | 其他业务成本 | 同上 |
| 6111 | 投资收益 | 内部单位不对外投资 |
| 6605 | 其他收益 | 内部单位无政府补助 |
| 6801 | 所得税费用 | 不单独核算所得税 |
| 4001/4002/4101 | 权益类 | 内部总包部结构，权益 ≈ 0 |

### 科目数量特征

总包部科目多于 SPV（含施工特有科目群：58xx/56xx/1126/3001），但损益类科目更少（无 6111/6605/6801）。

### 关键取数注意事项

| 科目 | 注意事项 |
|---|---|
| 1002 货币资金 | 各银行账户 ROUND_DOWN 后汇总 |
| 1483/1484 合同资产 | 组件级 ROUND_DOWN 后相减 |
| 2202 应付账款 | ROUND_DOWN(2202) − ROUND_DOWN(1123) |
| 2241 + 3001 其他应付款 | ROUND_DOWN(2241-01) + ROUND_DOWN(3001) |
| 5801 合同结算 | 贷方余额 = 合同负债 |
| 6702 信用减值损失 | 可为负（冲回大于计提时） |

## 自检清单

1. [ ] 是否确认有 5801/5601/6001/6401/2202/2701/3001/1126？
2. [ ] 是否确认无 4001/4002/4101 权益科目（权益 ≈ 0）？
3. [ ] 是否确认无 6801 所得税费用？
4. [ ] 其他应付款是否为 ROUND_DOWN(2241-01) + ROUND_DOWN(3001)？
5. [ ] 合同负债是否正确取自 5801 贷方余额？

## 免责声明

本科目表基于已验证的总包部 M12 2025 实际科目余额表编制。
