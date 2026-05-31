# CCFTS 可信度分级说明

## 5 个等级

| 等级 | 名称 | 含义 | 当前覆盖 |
|------|------|------|---------|
| **L1** | `source-cited` | 基于法规/准则/监管文件整理，含明确文件引用 | 所有 96 个文件均满足（每个文件都有 `sources` 或 `references`） |
| **L2** | `practice-derived` | 基于施工企业实务经验归纳，需结合企业自身制度复核 | 操作类技能（利润表/B.S./取整/快报映射等），已验证匹配率 99.2% |
| **L3** | `demo-verified` | 已通过 `examples/` 中的脱敏 demo 验证流程正确性 | 3 个 demo 目录已建立，但 demo 数据尚未填充，**暂未达到此等级** |
| **L4** | `accountant-reviewed` | 已由持证 CPA / 税务师 / 企业资深财务审核并署名 | **0 / 96 文件**（全部为 `verified_by: pending`） |
| **L5** | `production-proven` | 已在真实业务流程中持续使用并验证 | **0 / 96 文件**（项目尚未在生产环境中部署使用） |

## 当前默认状态

- **所有 96 个文件**：`quality_tier: research-verified`，`verified_by: pending`
- 这意味着：所有文件已达到 **L1（source-cited）**，部分操作类技能达到 **L2（practice-derived）**
- **不等于**：已获 CPA 审核（L4）或已在生产环境验证（L5）
- 从 L1/L2 到 L4/L5 的差距是"可信工具"和"可信知识库"的核心差距

## 各等级需要的证据

### L1 → L2
- 每个操作技能需标注"基于哪个企业的哪些期间的数据验证"
- 当前已有：某项目公司 Q3/Q4 2025 + 2026M05 验证数据（99.2% 匹配率）

### L2 → L3
- `examples/` 中每个 demo 的 `input/` 需填充脱敏真实数据
- `expected/` 需填入经过人工核验的正确输出
- 运行 demo → `output/` 与 `expected/` 对比，偏差分析

### L3 → L4
- 持证 CPA / 税务师逐文件审核
- 在 frontmatter 中签署：`verified_by: <姓名> <执业编号>`
- `quality_tier` 从 `research-verified` 改为 `accountant-verified`

### L4 → L5
- 在生产环境中实际使用 ≥ 3 个月
- 关键业务指标（如快报编制时间/错误率/VAT 申报准确率）有量化改善
- 用户反馈系统建立并持续跟踪

## 阅读建议

- 使用 L1-L2 的技能时：**必须人工复核**（见 `docs/manual-review-template.md`）
- 涉及法定申报/审计/融资时：仅能作为参考，不替代专业判断
- 如果某个技能的核心规则与你的企业实务不一致：以企业实务和当地税务机关口径为准

## 免责声明

本可信度分级是 CCFTS 项目的自我评估，不作为外部审计或监管合规的证明。
