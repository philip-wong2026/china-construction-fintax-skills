# CCFTS 项目进展笔记 — 2026-05-31（Internal Preview / Alpha）

## 当前状态

**Phase 0（架构）+ Phase 1（法规层）+ Phase 2（扩展）+ Phase 2.5（补缺）+ Phase 2.6（清理收尾）+ Phase 2.7（可信度基础设施）= 全部完成。**

**内部预览版（Internal Preview / Alpha）**：96 个技能文件，6 个职能领域全覆盖，0 个验证问题。面向懂施工企业财税业务的 AI agent 使用者，用于辅助检索、推理、工作流组织和检查，不作为最终合规意见。

## 最终文件清单

### Phase 0 — 架构搭建
- [x] 目录结构：6职能领域 × 8组织层级
- [x] `skills/README.md` — 导航地图
- [x] `skills/_template-skill.md` — SLOT就绪的技能模板
- [x] `scripts/validate-skills.py` v0.3 — filename==name + domain/level/slug/references 全面校验
- [x] `mcp/ccfts_mcp/server.py` v0.3 — MCP 前端解析器与验证器逻辑一致
- [x] MCP `pyproject.toml`

### Phase 1 — 法规层

| 监管机构 | 文件 | 内容 |
|---------|------|------|
| SASAC(4) | flash-report-deadlines, annual-settlement, one-profit-five-rates, state-capital-budget | 快报时间表、决算、一利五率、国有资本经营预算 |
| MOF(6) | cas14-revenue, cas33-consolidation, small-enterprise-standards, epc-accounting, special-bond-project, government-subsidies | CAS 14收入、CAS 33合并、小企业准则、EPC、专项债、政府补贴 |
| STA(4) | vat-law-2026, golden-tax-phase4, e-invoice-mandate, cit-prepayment-rules | 增值税法、金税四期、全电发票、CIT预缴 |
| MOHURD(2) | qualification-system, safety-fund-rates | 资质体系、安全生产费 |

### Phase 1 MVP 遗留
- [x] foundation/ccfts-workflow-base.md（已升级至 v0.2）
- [x] china-construction/ ×7（保持向后兼容，MCP 别名映射）

### Phase 2 — Base+SLOT 迁移

| Base 文件 | SPV 覆盖 | 项目部覆盖 |
|----------|----------|-----------|
| ccfts-fr-all-rounding-rules | ccfts-fr-spv-rounding-rules | ccfts-fr-project-unit-rounding-rules |
| ccfts-fr-all-entity-type-rules | ccfts-fr-spv-entity-type-rules | ccfts-fr-project-unit-entity-type-rules |
| ccfts-fr-all-profit-statement | ccfts-fr-spv-profit-statement | ccfts-fr-project-unit-profit-statement |
| ccfts-fr-all-balance-sheet | ccfts-fr-spv-balance-sheet | ccfts-fr-project-unit-balance-sheet |
| ccfts-fr-all-quick-report-mapping | ccfts-fr-spv-quick-report-mapping | ccfts-fr-project-unit-quick-report-mapping |
| ccfts-fr-all-period-end-adjustments | ccfts-fr-spv-period-end-adjustments | ccfts-fr-project-unit-period-end-adjustments |
| ccfts-acct-all-chart-of-accounts | ccfts-acct-spv-chart-of-accounts | ccfts-acct-project-unit-chart-of-accounts |

### Phase 2.5 — 场景空白 + 新域

| 领域 | 文件数 | 内容 |
|------|--------|------|
| 场景空白 | 8 | 质保金、竣工结算、EPC/专项债/PPP(4)、政府补贴(2) |
| 税务域(tax) | 6 | VAT一般/简易/跨区域预缴、CIT预缴、印花税、全电发票 |
| 会计核算(acct) | 7 | 合同成本Base、预计总成本、安全生产费分录、关联交易、变更索赔、保险理赔、质保金分录 |
| 管理办法(mgmt) | 7 | 内控、代局指、资金池、国家审计、成本控制、分包管理、清收清欠 |
| 规模变体 | 5 | 中型报表、小规模VAT、小型微利CIT、小企内控、个体施工队 |
| 境外(intl) | 3 | 外币折算、内外账差异、境外预提税 |
| 分析域(anlys) | 6 | 一利五率分析、预算偏差、集团KPI看板、两金分析、项目盈利、项目现金流 |

### Phase 2.6 — 清理（2026-05-31）

- [x] 3 个文件名与 frontmatter name 不一致 → 已统一
- [x] 验证器升级至 v0.3（新增 filename==name 校验）
- [x] MCP 解析器升级至 v0.3（多行 YAML list、全字段解析）
- [x] MCP `list_skills` 返回 `entity_levels`（替代废弃的 `entity_types`）
- [x] MCP `list_intelligence(authority=...)` 过滤正常
- [x] MCP `resolve_references` 正确返回 depends_on + references
- [x] 文档状态更新（README.md、skills/README.md、project-status.md）

## 验证结果
```
96 files, 0 issues
所有交叉引用有效
所有 filename stem == frontmatter name
MCP parser self-test: 5/5 slugs passed
0 个真实企业/项目/地名残留
```

## 最终项目全景

```
6 职能领域 × 8 组织层级 = 96 文件

intelligence/          16 法规
financial-reporting/   29 操作
accounting/            14 操作
tax/                   12 操作
analysis/               6 操作
management/            10 操作
foundation/             2 文件 (workflow-base v0.2 + skill-index)
旧文件                   7 (向后兼容)
```

## 质量状态

- 所有 96 个文件均为 `quality_tier: research-verified`
- 所有 96 个文件均为 `verified_by: pending`（尚未 CPA 审核）
- 脱敏：0 违规

## 关键设计决策（新会话需要知道）

1. **职能领域主维度，组织层级子维度**
2. **Base + SLOT 模式** — `_base/` 定义通用工作流+SLOT占位符，层级覆盖文件填充
3. **命名规范** — `ccfts-{domain}-{level}-{topic}.md`，filename stem == frontmatter name
4. **脱敏原则** — 所有文件不出现真实企业/项目/地名
5. **向后兼容** — 旧 slug 通过 MCP SLUG_ALIASES 映射到新 slug
6. **MCP 可选** — Markdown 文件本身可直接使用，MCP 是便捷封装层
7. **验证优先** — 任何修改后运行 `python3 scripts/validate-skills.py`

## 暂未处理

- CPA 审核（外部依赖）
- `tests/` 目录已有 3 个测试脚本（integrity/mcp-loading/demo-contracts）
- `skills/china-construction/` 旧文件可择机清理（当前保持不动）
- 分析域外的 soe-group/subsidiary/branch 层级 B.S./P&L/取整覆盖可复用已有覆盖推断
