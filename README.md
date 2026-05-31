# CCFTS — China Construction Enterprise Finance & Tax Skills

[![Skills](https://img.shields.io/badge/skills-96-blue)](https://github.com/philip-wong2026/china-construction-fintax-skills)
[![Validation](https://img.shields.io/badge/validation-100%25-brightgreen)](https://github.com/philip-wong2026/china-construction-fintax-skills)
[![License](https://img.shields.io/badge/license-AGPL--3.0-orange)](LICENSE)
[![Status](https://img.shields.io/badge/status-Internal%20Preview%20%2F%20Alpha-lightgrey)](https://github.com/philip-wong2026/china-construction-fintax-skills)

## 中国施工企业财税技能包

为 AI 代理（Claude、Codex、DeepSeek 及任何支持 MCP 的客户端）提供结构化的中国施工企业财务会计与税务知识。从科目余额表到财务快报，从增值税简易计税到完工百分比法——把中国施工企业财税专家的经验变成可复用的 AI 技能文件。

**当前阶段**：**Internal Preview / Alpha** — 96 个技能文件，6 个职能领域全覆盖。面向懂施工企业财税业务的 AI agent 使用者，用于辅助检索、推理、工作流组织和检查，不作为最终合规意见。全部 `research-verified`（待 CPA 审核）。

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
├── notes/                           # 项目笔记和交接文档
├── backups/                         # 备份
├── LICENSE                          # AGPL-3.0
└── README.md                        # 本文件
```

## 快速开始

### 方式一：直接引用（任何 AI 工具）

将 `skills/` 目录加入你的 AI 项目上下文。所有技能文件均为纯 Markdown，AI 代理可直接读取。

### 方式二：MCP Server（Claude Desktop / Cursor / Codex MCP）

```bash
cd china-construction-fintax-skills/mcp
pip install .
```

在 `claude_desktop_config.json` 中添加：

```json
{
  "mcpServers": {
    "ccfts": { "command": "ccfts-mcp" }
  }
}
```

## 验证状态

- **结构验证**：`python3 scripts/validate-skills.py` → 96 files, 0 issues
- **MCP 解析**：多行 YAML list、跨引用、slug 别名均通过测试
- **数据验证**：操作技能基于施工企业 Q3/Q4 2025 及 2026M05 实际财务数据验证，快报匹配率 99.2%
- **脱敏**：0 个真实企业/项目/地名残留

## 已知限制

- MCP 服务器需用户自行 `pip install .`，当前开发环境未预装 `mcp` 包
- 全部 96 个文件尚未经持证 CPA 审核（`verified_by: pending`）
- `tests/` 目录暂无内容级自动化测试

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

## 作者

Philip Wong — 基于在中国施工企业财务快报自动化的实战经验构建。

本技能库基于公开法规、准则和中国施工行业公开资料整理，不代表任何特定企业的内部制度或数据。

## 许可证

AGPL-3.0 — 详见 [LICENSE](LICENSE)
