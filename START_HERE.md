# CCFTS — Start Here

> 面向懂施工企业财税业务的 AI agent 使用者。用于辅助检索、推理、工作流组织和检查，不作为最终合规意见。

如果你还不清楚“AI skill 是什么、装到哪里、跟 AI workspace 有什么关系”，请先读 [docs/beginner-guide.md](docs/beginner-guide.md)。

## 这是什么

96 个中文 Markdown 技能文件，覆盖中国施工企业（铁路/公路/市政/房建/水利/港口/矿山/机电安装）的财务会计与税务全链条。AI agent 直接读取 Markdown 即可使用；另有可选的 MCP 服务器封装。

## 使用方式

**方式 A（推荐）**：直接将 `skills/` 目录中的 .md 文件作为 AI agent 的上下文加载。按场景从下方索引找到对应的技能 slug，按"推荐加载顺序"逐个加载。

**方式 B**：通过 MCP 服务器加载（需 `cd mcp && pip install -e .`）。详见 `mcp/SMOKE_TEST.md`。

## 6 个核心场景

---

### 场景 1：我要编施工企业快报

**适用**：项目财务 / 报表编制人员 / AI agent

**推荐加载顺序**：
1. `ccfts-workflow-base` — 10 步通用工作流
2. `ccfts-fr-all-flash-report-workflow` — 快报编制完整编排
3. `ccfts-fr-all-entity-type-rules` — 判定主体类型（Type A/B）
4. 对应层级的 entity-type 覆盖文件（如 `ccfts-fr-spv-entity-type-rules`）
5. `ccfts-acct-all-chart-of-accounts` + 对应层级覆盖
6. `ccfts-fr-all-rounding-rules` + 对应层级覆盖
7. `ccfts-fr-all-profit-statement` + `ccfts-fr-all-balance-sheet` + 对应层级覆盖
8. `ccfts-fr-all-quick-report-mapping` — 科目余额→快报映射总流程
9. 如非季度末：`ccfts-fr-all-period-end-adjustments` + 对应层级覆盖

**用户需要提供**：
- 科目余额表（.xls/.xlsx，标准列位格式）
- 报表期间（YYYYMM）
- 主体说明（SPV 投资管理类 or 总包部施工类？）
- 是否季度末/年末

**应输出**：
- 主体类型判定结果 + 置信度
- 科目→快报映射明细表
- 利润表 + 资产负债表（万元）
- 差异检查表（如有对照）
- 审核者摘要

**必须人工复核**：
- 主体类型是否与实际组织架构一致
- 期末调整（2211-02/6602 未结转）是否完整
- ±1 万元差异是否只是临界值噪音（非实质性差异）
- 其他应付款是否按正确方法计算（Type A 倒推 / Type B 直接取）

---

### 场景 2：判断 VAT 一般计税 / 简易计税 / 跨区域预缴

**适用**：项目财务 / 税务岗 / AI agent

**推荐加载顺序**：
1. `ccfts-intel-sta-vat-law-2026` — 增值税法 2026 法规要点
2. `ccfts-tax-all-vat-general-filing` — 一般计税 9% 月度申报
3. `ccfts-tax-all-vat-simplified-filing` — 简易计税 3% 条件与申报
4. `ccfts-tax-all-vat-cross-region-prepayment` — 跨区域 2%/3% 预缴
5. 如需子公司级申报：`ccfts-tax-subsidiary-vat-filing`

**用户需要提供**：
- 施工合同关键信息（是否甲供/清包工/EPC？合同金额？项目地址？）
- 纳税人身份（一般纳税人 / 小规模纳税人）
- 项目是否跨县/市/区

**应输出**：
- 适用计税方式判断（一般 9% / 简易 3% / 清包工 3% / 混合）
- 月度销项税额计算表
- 可抵扣进项税额归集表
- 跨区域预缴税额计算（如有）
- 申报表关键行次填列指引

**必须人工复核**：
- 甲供工程：2026.1.1 起终止简易计税，新签合同必须 9% → 合同日期是否在 2026.1.1 后？
- 清包工：分票规则从严（分包普票），分包商是否能配合？
- 跨区域预缴：项目所在地税务机关是否有特殊要求？
- EPC 项目：E/P/C 拆分开票还是一张票？混合销售风险？

---

### 场景 3：判断企业所得税预缴

**适用**：子公司/工程局级财务 / AI agent

**推荐加载顺序**：
1. `ccfts-intel-sta-cit-prepayment-rules` — CIT 预缴法规
2. `ccfts-tax-all-cit-prepayment-filing` — 季度预缴 + 年度汇算清缴
3. 如需子公司级：`ccfts-tax-subsidiary-cit-filing`
4. `ccfts-fr-all-entity-type-rules` — 确认独立法人身份

**用户需要提供**：
- 是否为独立法人（是→需预缴 / 否→不单独预缴）
- 是否有跨省施工项目（有→0.2% 预缴）
- 当期利润表（累计数）

**应输出**：
- 季度预缴税额计算（含跨省项目 0.2% 抵减）
- A105000 常见纳税调整项目清单
- 安全生产费的税会差异调增/调减
- 研发费用加计扣除提示（如适用）

**必须人工复核**：
- 安全生产费：本年计提未使用部分是否已纳税调增？
- 资产减值准备是否已纳税调增？
- 跨省项目 0.2% 预缴是否足额？
- 小型微利企业 5% 优惠是否可享受（资产总额 ≤ 5000 万是主要门槛）？

---

### 场景 4：做项目盈利 / 现金流分析

**适用**：项目部 / 工程公司经营分析人员 / AI agent

**推荐加载顺序**：
1. `ccfts-anlys-project-unit-profitability` — 项目盈利能力分析
2. `ccfts-anlys-project-unit-cashflow` — 项目现金流分析
3. `ccfts-anlys-all-budget-variance` — 预算偏差分析方法
4. `ccfts-mgmt-project-unit-cost-control` — 责任成本控制
5. `ccfts-acct-all-contract-cost` — 合同履约成本归集
6. `ccfts-acct-enterprise-contract-cost` — 预计总成本/亏损合同

**用户需要提供**：
- 项目责任成本预算
- 实际成本数据（人工/材料/机械/分包/间接费）
- 累计收款/付款记录
- 累计确认收入数据

**应输出**：
- 毛利率趋势分析（月度追踪）
- 各成本项偏差分析（量差 + 价差）
- 红黄绿灯预警
- 项目营业收现率
- 垫资比例
- 亏损项目清单 + 预计损失评估

**必须人工复核**：
- 成本偏差的根因是量差还是价差？（不同对策）
- 垫资比例是否在安全范围内（< 20%）？
- "已完工未结算"挂账周期是否过长？
- 是否有未计提的亏损合同预计负债？

---

### 场景 5：处理质保金 / 竣工结算

**适用**：项目部 / 工程公司商务+财务 / AI agent

**推荐加载顺序**：
1. `ccfts-fr-all-retention-money` — 质保金完整流程（确认→持有→到期→回收）
2. `ccfts-acct-enterprise-quality-guarantee` — 质保金分录实操
3. `ccfts-fr-all-final-account-settlement` — 竣工结算五阶段流程
4. `ccfts-mgmt-project-unit-collection-clear-arrears` — 清收清欠（如需催收）

**用户需要提供**：
- 施工合同质保金条款（比例、缺陷责任期）
- 竣工结算书（送审金额）
- 审计报告（审定金额、审减明细）
- 应收账款台账（如需催收）

**应输出**：
- 质保金四阶段确认分录
- 审减争议处理建议（接受/协商/争议）
- 收入调整分录（审定金额 vs 累计确认收入）
- 合同资产→应收账款转换时点
- 逾期质保金催收策略

**必须人工复核**：
- 质保金扣留比例是否 ≤ 3%？
- 争议项可收回性评估是否合理？有无需单项计提减值的？
- VAT：审减后是否及时开具红字发票？
- 竣工结算拖延的原因和对策是否明确？

---

### 场景 6：做合并报表或集团层面分析

**适用**：集团财务 / 上市公司合并岗 / AI agent

**推荐加载顺序**：
1. `ccfts-fr-all-consolidation-workflow` — 合并报表编制工作流
2. `ccfts-fr-all-consolidation-report` — 合并抵销分录 + PPP 合并处理
3. `ccfts-intel-mof-cas33-consolidation` — CAS 33 法规要点
4. `ccfts-anlys-soe-group-kpi-dashboard` — 集团经营看板
5. `ccfts-anlys-soe-group-two-funds-analysis` — "两金"分析
6. `ccfts-mgmt-soe-group-cash-pooling` — 资金池
7. `ccfts-mgmt-soe-group-budget-approval` — 全面预算（如需）

**用户需要提供**：
- 母公司 + 各子公司单户 TB
- 合并范围清单（含持股比例、控制判断依据）
- 内部往来/内部交易明细
- PPP 项目公司清单

**应输出**：
- 合并范围判断（控制三要素逐项评估）
- 合并工作底稿（汇总+抵销借/贷=合并数）
- 5 步标准抵销分录（权益/内部往来/内部交易/现金流/债券）
- PPP 项目公司合并 vs 不合并的影响对比
- 合并层面"两金"和资产负债率

**必须人工复核**：
- 合并范围变更是否有正当商业理由（不是规避考核）？
- 内部往来是否全额抵销（3001 在合并层面 = 0）？
- PPP 项目公司是否按国资委要求原则性合并？
- 少数股东权益/损益计算是否正确？
- 合并层面"一利五率"是否已重算？

---

## 人工复核总则

以上所有场景的 AI 输出均需人工复核后方可用于正式报送或决策。详见：
- `docs/manual-review-template.md` — 结构化复核清单
- `docs/evidence-levels.md` — 可信度分级说明

## 快速索引

全部技能的场景路由详见：`skills/foundation/ccfts-all-skill-index.md`

## 免责声明

本工具输出仅用于辅助分析，不替代持证 CPA / 税务师 / 企业内部审批流程。所有决策责任由使用者承担。
