# CCFTS — China Construction Enterprise Finance & Tax Skills

[![Skills](https://img.shields.io/badge/skills-96-blue)](https://github.com/philip-wong2026/china-construction-fintax-skills)
[![Validation](https://github.com/philip-wong2026/china-construction-fintax-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/philip-wong2026/china-construction-fintax-skills/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-AGPL--3.0-orange)](LICENSE)
[![Status](https://img.shields.io/badge/status-Public%20Alpha-lightgrey)](https://github.com/philip-wong2026/china-construction-fintax-skills)

## 中国施工企业财税技能包

为 AI 代理（Claude、Codex、DeepSeek 及任何支持 MCP 的客户端）提供结构化的中国施工企业财务会计与税务知识。从科目余额表到财务快报，从增值税简易计税到完工百分比法——把中国施工企业财税专家的经验变成可复用的 AI 技能文件。

**当前阶段**：**Public Alpha** — 96 个技能文件，6 个职能领域全覆盖。面向懂施工企业财税业务的 AI agent 使用者，用于辅助检索、推理、工作流组织和检查，不作为最终合规意见。全部 `research-verified`（待 CPA 审核）。

第一次接触 AI skills？先看 [新手说明：这个项目是什么，怎么用](docs/beginner-guide.md)。

已经知道自己要处理哪个财税场景？看 [START_HERE.md](START_HERE.md)，里面按 6 个真实财税场景列出了推荐加载顺序、输入材料、输出结果和人工复核点。

## 适用边界

**适合：**

- 施工企业财务、税务、报表、经营分析人员用 AI agent 做资料检索、规则检查和工作流组织
- 构建中文财税垂直 AI agent、MCP 工具或 domain skills 的开发者
- 学习中国施工企业财税场景下的技能文件组织方式和验证方法

**不适合：**

- 直接替代 CPA、税务师、律师或企业正式内控制度
- 未经人工复核就用于正式纳税申报、审计签字、监管报送或重大经营决策
- 作为通用中国会计准则知识库使用；本项目当前聚焦施工企业场景

## 设计理念

- **Markdown 优先**：技能文件即纯 .md，无需任何工具即可被 AI 代理直接读取
- **平台无关**：同一套技能文件，Claude 用、Codex 用、未来的 DeepSeek Agent 也用
- **深度优先**：从一个垂直领域（中国施工企业）做深做实，再逐步扩展
- **Base + SLOT 架构**：`_base/` 文件定义通用工作流和占位符，层级覆盖文件填充具体参数
- **MCP 可选**：MCP 服务器是便捷封装层，技能文件本身可直接使用
- **OpenAccountants 兼容**：采用相同的 frontmatter schema 和质量等级标准
- **开源免费**：AGPL-3.0，永远免费开放

## 项目结构

```
china-construction-fintax-skills/
├── skills/                          # 技能文件（核心内容，96 个 .md）
│   ├── foundation/                  # 跨领域工作流基础（2 文件）
│   ├── financial-reporting/         # 财务报表域（29 文件，fr）
│   ├── accounting/                  # 会计核算域（14 文件，acct）
│   ├── tax/                         # 税务申报域（12 文件，tax）
│   ├── analysis/                    # 经济活动分析域（6 文件，anlys）
│   ├── management/                  # 管理办法域（10 文件，mgmt）
│   ├── intelligence/                # 法规知识库（16 文件，intel）
│   ├── china-construction/          # 旧文件（7 个，保持向后兼容）
│   └── _template-skill.md          # 技能模板
├── mcp/                             # MCP Server v0.3（可选便捷封装）
├── scripts/                         # 验证工具（validate-skills.py v0.3）
├── docs/                            # 新手说明、人工复核、可信度分级等文档
├── examples/                        # 脱敏示例数据和期望输出
├── tests/                           # 结构、MCP 解析、demo 契约测试
├── LICENSE                          # AGPL-3.0
└── README.md                        # 本文件
```

## 快速开始

### 5 分钟试用

```bash
git clone https://github.com/philip-wong2026/china-construction-fintax-skills.git
cd china-construction-fintax-skills
python3 scripts/validate-skills.py
python3 tests/test_demo_contracts.py
```

然后打开 [START_HERE.md](START_HERE.md)，按你的场景选择对应技能 slug。

如果你还不清楚“skills 装到哪里、跟普通提示词有什么区别、跟 AI workspace 有什么关系”，先读 [docs/beginner-guide.md](docs/beginner-guide.md)。

### 方式一：直接引用（任何 AI 工具）

将 `skills/` 目录加入你的 AI 项目上下文。所有技能文件均为纯 Markdown，AI 代理可直接读取。

### 方式二：MCP Server（Claude Desktop / Cursor / Codex MCP）

```bash
cd china-construction-fintax-skills/mcp
python3 -m pip install -e .
```

在 `claude_desktop_config.json` 中添加：

```json
{
  "mcpServers": {
    "ccfts": { "command": "ccfts-mcp" }
  }
}
```

如果 `ccfts-mcp` 不在 shell 的 `PATH` 中，请使用 `python3 -m pip show -f ccfts-mcp` 找到脚本安装位置，并在 MCP 客户端配置中填写完整路径。

## 验证状态

- **结构验证**：`python3 scripts/validate-skills.py` → 96 files, 0 issues
- **CI 验证**：GitHub Actions 每次 push/PR 运行结构、完整性、MCP loading 和 demo 契约测试
- **MCP 解析**：多行 YAML list、跨引用、slug 别名均通过 helper 测试；完整客户端联调见 `mcp/SMOKE_TEST.md`
- **示例数据**：`examples/` 提供脱敏教学样例和 expected 输出，用于演示流程，不代表真实企业报表
- **历史数据验证**：部分操作技能基于施工企业 Q3/Q4 2025 及 2026M05 实际财务数据验证，快报匹配率 99.2%
- **脱敏**：0 个真实企业/项目/地名残留

## 已知限制

- MCP 服务器需用户自行安装；本地 helper/parser 已验证，MCP 客户端联调需按 `mcp/SMOKE_TEST.md` 执行
- 全部 96 个文件尚未经持证 CPA 审核（`verified_by: pending`）
- `tests/` 目前以结构、解析和 demo 契约测试为主，尚未覆盖完整会计/税务规则自动验算

## 质量等级

| 等级 | 含义 | 当前状态 |
|------|------|---------|
| `research-verified` | 基于权威来源起草，待持证会计师审核签字 | **所有 96 个文件** |
| `accountant-verified` | 已由持证注册会计师审核并署名 | 暂无（待未来 CPA 审核） |

## 覆盖范围

| 维度 | 覆盖 |
|------|------|
| 监管机构 | SASAC / MOF / STA / MOHURD |
| 职能领域 | 财务报表 / 会计核算 / 税务申报 / 经济活动分析 / 管理办法 / 法规知识库 |
| 组织层级 | 央企集团 / 独立法人子公司 / 分公司 / 项目部 / 项目公司SPV / 小企业 / 境外 |
| 工程行业 | 铁路 / 公路 / 市政(含城轨) / 房建 / 水利水电 / 港口航道 / 矿山 / 机电安装 |
| 企业规模 | 大型央企 / 中型 / 小型 / 个体户 |
| 税种 | VAT一般 / VAT简易 / 跨区域预缴 / CIT / 印花税 |
| 特殊场景 | 质保金 / 竣工结算 / EPC / 专项债 / PPP / 政府补贴 / 代局指 / 清收清欠 / 亏损合同 / 变更索赔 |

## 贡献

欢迎提交 PR。技能文件的修改需附带验证数据。

提交前建议运行：

```bash
python3 scripts/validate-skills.py
python3 tests/test_skill_integrity.py
python3 tests/test_mcp_loading.py
python3 tests/test_demo_contracts.py
```

## 免责声明

本项目不构成法律、税务、审计、会计或投资建议。AI 输出必须由具备相应专业能力的人员结合最新法规、地方口径和企业制度复核后使用。详见 [DISCLAIMER.md](DISCLAIMER.md)。

## 作者

Philip Wong — 基于在中国施工企业财务快报自动化的实战经验构建。

本技能库基于公开法规、准则和中国施工行业公开资料整理，不代表任何特定企业的内部制度或数据。

## 许可证

AGPL-3.0 — 详见 [LICENSE](LICENSE)
