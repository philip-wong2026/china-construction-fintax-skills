---
name: ccfts-fr-all-entity-type-rules
description: >
  中国施工企业财务快报主体类型判定——通用工作流基础（Base + SLOT 模式）。
  定义判定决策树、分类置信度、混合场景处理的通用流程。
  适用所有组织层级。触发条件：用户提供科目余额表、需要确定主体类型时。
version: 0.2
jurisdiction: CN
tax_year: 2025
category: financial-reporting
domains: [fr]
quality_tier: research-verified
verified_by: pending
entity_levels: [all]
enterprise_scales: [large-soe]
depends_on:
  - ccfts-workflow-base
references:
  - ccfts-intel-mof-cas14-revenue
is_base: true
slots:
  - ENTITY_TYPE_LABEL
  - ENTITY_TYPE_ALIAS
  - ENTITY_TYPE_CODE
  - PRIMARY_INCOME_ACCOUNT
  - PRIMARY_INCOME_NAME
  - PRIMARY_COST_ACCOUNT
  - PRIMARY_COST_NAME
  - HAS_CONTRACT_SETTLEMENT
  - HAS_CONTRACT_PERFORMANCE_COST
  - HAS_ACCOUNTS_PAYABLE
  - HAS_LONG_TERM_PAYABLE
  - HAS_INTERNAL_RECEIVABLES
  - HAS_PENDING_INPUT_VAT
  - EQUITY_STRUCTURE
  - BS_ROUNDING_MODE
  - IS_ROUNDING_MODE
  - CONTRACT_ASSET_CALC
  - OTHER_PAYABLES_CALC
  - NET_PROFIT_FORMULA
triggers:
  - 企业类型
  - 主体类型
  - 投资公司
  - 总包部
  - 施工企业
  - entity type
---

# 施工企业快报主体类型判定（Base）

> **SLOT 说明**：本文件为通用工作流基础。其中 `{SLOT_XXX}` 为命名占位符，
> 由各组织层级的覆盖文件填充为具体值。加载本文件时，必须同时加载对应层级
> 的覆盖文件以填充 SLOT。

## 快速参考

| 项目 | {ENTITY_TYPE_CODE} — {ENTITY_TYPE_LABEL} |
|---|---|
| 主营业务 | {ENTITY_TYPE_LABEL} |
| 主营收入科目 | {PRIMARY_INCOME_ACCOUNT} {PRIMARY_INCOME_NAME} |
| 主营成本科目 | {PRIMARY_COST_ACCOUNT} {PRIMARY_COST_NAME} |
| 合同结算科目(5801) | {HAS_CONTRACT_SETTLEMENT} |
| 合同履约成本(5601) | {HAS_CONTRACT_PERFORMANCE_COST} |
| 应付账款(2202) | {HAS_ACCOUNTS_PAYABLE} |
| 长期应付款(2701) | {HAS_LONG_TERM_PAYABLE} |
| 内部往来(3001) | {HAS_INTERNAL_RECEIVABLES} |
| 待结算进项税额(1126) | {HAS_PENDING_INPUT_VAT} |
| 权益结构 | {EQUITY_STRUCTURE} |
| 资产负债表取整 | {BS_ROUNDING_MODE} |
| 利润表取整 | {IS_ROUNDING_MODE} |
| 合同资产净额计算 | {CONTRACT_ASSET_CALC} |
| 其他应付款计算 | {OTHER_PAYABLES_CALC} |
| 利润总额 = 净利润？ | {NET_PROFIT_FORMULA} |

## 一、判定决策树（所有主体通用）

```
读取科目余额表科目列表
    │
    ├── 有 5801（合同结算）？ ──YES──→ Type B（施工总承包类）
    │
    ├── 有 6001（主营业务收入）？ ──YES──→ Type B
    │
    ├── 有 6401（主营业务成本）？ ──YES──→ Type B
    │
    ├── 有 3001（内部往来）？ ──YES──→ Type B
    │
    ├── 有 6051（其他业务收入）且无 6001？ ──YES──→ Type A（投资管理类）
    │
    └── 仍不确定？ → 列出可能的科目特征，请求用户确认
```

**关键判定信号（按优先级）**：
1. **5801 合同结算** — 最可靠的 Type B 信号。投资管理类绝对没有此科目。
2. **6001 vs 6051** — 主营收入科目直接区分业务性质。
3. **权益结构** — 权益≈零（资产 = 负债）→ Type B。正常权益 → Type A。
4. **2202 应付账款** — Type A 无（填 0）；Type B 有，需减去 1123 预付账款。

## 二、{ENTITY_TYPE_CODE} — {ENTITY_TYPE_LABEL} 详细规则

### 科目特征

{ENTITY_TYPE_LABEL}（{ENTITY_TYPE_ALIAS}）的科目特征：
- 收入：{PRIMARY_INCOME_ACCOUNT} {PRIMARY_INCOME_NAME}
- 成本：{PRIMARY_COST_ACCOUNT} {PRIMARY_COST_NAME}
- 5801 合同结算：{HAS_CONTRACT_SETTLEMENT}
- 5601 合同履约成本：{HAS_CONTRACT_PERFORMANCE_COST}
- 2202 应付账款：{HAS_ACCOUNTS_PAYABLE}
- 2701 长期应付款：{HAS_LONG_TERM_PAYABLE}
- 3001 内部往来：{HAS_INTERNAL_RECEIVABLES}
- 1126 待结算进项税额：{HAS_PENDING_INPUT_VAT}
- 权益结构：{EQUITY_STRUCTURE}

### 资产负债表关键计算

| 快报项目 | 计算方式 | 注意 |
|---|---|---|
| 货币资金 | 各子行分别取整后汇总 | 区分内部财务公司 vs 外部金融机构 |
| 预付账款 | 1123 期末借方余额 | 直接取 |
| 其他应收款 | 净额计算 | 按本层级取整规则 |
| 固定资产净额 | 原值 − 折旧 | 分项取整后相减 |
| 合同资产净额 | {CONTRACT_ASSET_CALC} | 组件级分别取整 |
| 其他应付款 | {OTHER_PAYABLES_CALC} | 按本层级方法 |

### 利润表关键计算

- 利润总额 = 营业收入 − 营业成本 − 税金及附加 − 财务费用 + 其他收益 + 投资收益 − 资产减值损失 − 信用减值损失
- 净利润 = {NET_PROFIT_FORMULA}

### 业务板块分配

- 利润指标表对应业务板块行填列利润总额
- 营业收入/营业成本的明细行不填

### 取整规则

- 资产负债表：{BS_ROUNDING_MODE}
- 利润表：{IS_ROUNDING_MODE}

## 三、分类置信度（所有主体通用）

| 科目信号数 | 置信度 | 处理方式 |
|---|---|---|
| ≥3 个信号一致 | Classified | 直接确定类型 |
| 1-2 个信号 | Assumed | 标记假设，列出推断依据 |
| 0 个信号或信号矛盾 | Needs Input | 列出科目特征，请求用户确认 |

## 四、混合场景处理（所有主体通用）

如果同一套系统下存在不同主体类型（如一家项目公司和一家总包部），**必须分别处理、分别编制快报**，不能交叉引用对方的科目映射规则。

## 五、自检清单

1. [ ] 科目列表中是否搜索了 5801/6001/6401/6051/6402？
2. [ ] 是否检查了权益结构（资产 vs 负债）？
3. [ ] 判定结果是否有 ≥2 个独立信号支持？
4. [ ] 取整规则是否正确关联到实体类型（{BS_ROUNDING_MODE}）？
5. [ ] 是否对混合场景做了分别处理？
6. [ ] 是否正确加载了对应组织层级的 SLOT 覆盖文件？

## 六、SLOT 填充参考

| SLOT | 含义 | 由层级覆盖文件定义 |
|---|---|---|
| `{ENTITY_TYPE_LABEL}` | 主体类型中文全称 | 投资管理类 / 施工总承包类 |
| `{ENTITY_TYPE_ALIAS}` | 主体类型中文简称 | 项目公司SPV / 总包部/项目部 |
| `{ENTITY_TYPE_CODE}` | 类型代码 | Type A / Type B |
| `{PRIMARY_INCOME_ACCOUNT}` | 主营收入科目编号 | 6051 / 6001 |
| `{PRIMARY_INCOME_NAME}` | 主营收入科目名称 | 其他业务收入 / 主营业务收入 |
| `{PRIMARY_COST_ACCOUNT}` | 主营成本科目编号 | 6402 / 6401 |
| `{PRIMARY_COST_NAME}` | 主营成本科目名称 | 其他业务成本 / 主营业务成本 |
| `{HAS_CONTRACT_SETTLEMENT}` | 是否有 5801 | 无 / 有 |
| `{HAS_CONTRACT_PERFORMANCE_COST}` | 是否有 5601 | 无 / 有 |
| `{HAS_ACCOUNTS_PAYABLE}` | 是否有 2202 | 无（填 0）/ 有 |
| `{HAS_LONG_TERM_PAYABLE}` | 是否有 2701 | 无 / 有 |
| `{HAS_INTERNAL_RECEIVABLES}` | 是否有 3001 | 无 / 有 |
| `{HAS_PENDING_INPUT_VAT}` | 是否有 1126 | 无 / 有 |
| `{EQUITY_STRUCTURE}` | 权益结构描述 | 正常 / ≈ 0 |
| `{BS_ROUNDING_MODE}` | 资产负债表取整 | ROUND_HALF_UP / ROUND_DOWN |
| `{IS_ROUNDING_MODE}` | 利润表取整 | ROUND_HALF_UP |
| `{CONTRACT_ASSET_CALC}` | 合同资产净额计算方式 | 组件级取整后相减 |
| `{OTHER_PAYABLES_CALC}` | 其他应付款计算方式 | 倒推 / 直接取数 |
| `{NET_PROFIT_FORMULA}` | 净利润公式 | 利润总额 − 所得税 / = 利润总额 |

## 七、参考材料

- 已验证的投资管理类项目公司 2025Q3/Q4 及 2026M05 科目余额表
- 已验证的施工总承包类总包部 2025M12 科目余额表
- 本规则基于实际快报数据反推验证
- 本文件为 Base 层，对应覆盖文件：
  - `ccfts-fr-spv-entity-type-rules` — 投资管理类（项目公司 SPV）
  - `ccfts-fr-project-unit-entity-type-rules` — 施工总承包类（总包部/项目部）

## 免责声明

本技能文件为面向 AI 代理的技术参考，不替代持证会计师的专业判断。主体分类规则基于已验证的两种企业类型，可能不覆盖所有施工企业变体（如联合体项目部、BT/BOT 项目公司等）。
