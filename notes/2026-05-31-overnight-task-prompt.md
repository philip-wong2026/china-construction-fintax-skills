# 今晚执行任务提示词

> 复制以下全部内容，粘贴给新会话的 AI。

---

先读项目进展笔记：`/Volumes/T7 Shield/AI workspace/10_projects/active/china-construction-fintax-skills/notes/2026-05-31-project-status.md`

然后读技能导航：`/Volumes/T7 Shield/AI workspace/10_projects/active/china-construction-fintax-skills/skills/README.md`

项目权限已在 `.claude/settings.json` 全面放开，不会弹窗。

---

## 今晚任务：Phase 2 Base+SLOT 拆分（4 个旧技能 → 12 个新文件）

将 `skills/china-construction/` 下 4 个旧操作技能拆分为 Base + 层级覆盖文件。

### 任务 1：实体类型规则拆分

1. 读旧文件 `skills/china-construction/ccfts-entity-type-rules.md`
2. 识别 Type A（SPV/投资管理类）vs Type B（项目部/总包部）的差异点 → 这些差异点就是 SLOT
3. 创建 Base 文件 `skills/financial-reporting/_base/ccfts-fr-all-entity-type-rules.md`
   - `is_base: true`
   - 列出所有 SLOT
   - 正文用 `{SLOT_NAME}` 占位
4. 创建 SPV 覆盖 `skills/financial-reporting/spv/ccfts-fr-spv-entity-type-rules.md`
   - `fills_slots_for: ccfts-fr-all-entity-type-rules`
5. 创建 project-unit 覆盖 `skills/financial-reporting/project-unit/ccfts-fr-project-unit-entity-type-rules.md`
   - `fills_slots_for: ccfts-fr-all-entity-type-rules`

### 任务 2：利润表拆分

同上流程。旧文件 `skills/china-construction/ccfts-profit-statement.md`。
Base: `skills/financial-reporting/_base/ccfts-fr-all-profit-statement.md`
SPV: `skills/financial-reporting/spv/ccfts-fr-spv-profit-statement.md`
Project-unit: `skills/financial-reporting/project-unit/ccfts-fr-project-unit-profit-statement.md`

### 任务 3：资产负债表拆分

旧文件 `skills/china-construction/ccfts-balance-sheet.md`。
Base: `skills/financial-reporting/_base/ccfts-fr-all-balance-sheet.md`
SPV: `skills/financial-reporting/spv/ccfts-fr-spv-balance-sheet.md`
Project-unit: `skills/financial-reporting/project-unit/ccfts-fr-project-unit-balance-sheet.md`

### 任务 4：科目表拆分

旧文件 `skills/china-construction/ccfts-chart-of-accounts.md`。
注意：科目表属于 accounting 域（`domains: [acct]`），放 `skills/accounting/` 目录。
Base: `skills/accounting/_base/ccfts-acct-all-chart-of-accounts.md`
SPV: `skills/accounting/spv/ccfts-acct-spv-chart-of-accounts.md`
Project-unit: `skills/accounting/project-unit/ccfts-acct-project-unit-chart-of-accounts.md`

---

## 参考范例（已完成）

- `skills/financial-reporting/_base/ccfts-fr-all-rounding-rules.md` — Base 文件范例（10 个 SLOT）
- `skills/financial-reporting/spv/ccfts-fr-spv-rounding-rules.md` — SPV 覆盖范例
- `skills/financial-reporting/project-unit/ccfts-fr-project-unit-rounding-rules.md` — project-unit 覆盖范例

---

## 两种主体类型速查

| 特征 | Type A（SPV/投资管理类） | Type B（项目部/施工总承包类） |
|------|--------------------------|------------------------------|
| 收入科目 | 6051 其他业务收入 | 6001 主营业务收入 |
| 成本科目 | 6402 其他业务成本 | 6401 主营业务成本 |
| 合同结算(5801) | 无 | 有 |
| 合同履约成本(5601) | 无 | 有 |
| 应付账款(2202) | 无 | 有 |
| 内部往来(3001) | 无 | 有 |
| 权益结构 | 正常 | ≈ 0 |
| B/S 取整 | ROUND_HALF_UP | ROUND_DOWN |
| P&L 取整 | ROUND_HALF_UP | ROUND_HALF_UP |
| 其他应付款 | 倒推 | 直接取 2241-01 + 3001 |
| 净利润 | = 利润总额 - 所得税 | = 利润总额 |

## 命名规范

`ccfts-{domain}-{level}-{topic}.md`

domain: fr(报表) / acct(会计) / tax(税务) / anlys(分析) / mgmt(管理) / intel(法规)
level: soe-group / subsidiary / branch / project-unit / spv / all(跨层级)

## 每完成一个任务后

1. 更新 `skills/README.md` 快速查找表
2. 更新 `mcp/ccfts_mcp/server.py` 的 SLUG_ALIASES（旧 slug → 新 slug）
3. 更新 `mcp/ccfts_mcp/server.py` 的 INTENT_CATALOGUE
4. 更新 `notes/2026-05-31-project-status.md` 进度
5. 运行 `python3 scripts/validate-skills.py`（在项目根目录执行）
   - 预期：N files, 0 issues
   - 如果报错，修复后重跑直到通过

## 铁律

- **脱敏**：技能文件里绝对不能出现真实企业/项目/地名。用"某项目公司""某总包部""某集团"
- **不破坏旧文件**：旧文件（`china-construction/`）保持不动，新建文件在 `financial-reporting/` 和 `accounting/` 下
- **通过验证再下一个**：每个拆分跑通 `validate-skills.py` 才能进行下一个
