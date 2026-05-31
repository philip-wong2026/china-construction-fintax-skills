# 新手说明：这个项目是什么，怎么用

这份文档写给第一次看到 CCFTS 的人。你不需要先懂 MCP、agent、repo、skill 这些词，也可以理解它能做什么。

## 一句话解释

CCFTS 是一套“给 AI 看的中国施工企业财税操作手册”。

它不是一个财务软件，也不是一个新的大模型。它是一组结构化 Markdown 文件，告诉 AI 在处理施工企业财务、税务、报表、分析问题时应该参考哪些规则、按什么步骤问问题、怎么检查结果、哪些地方必须人工复核。

可以把它理解成：

> 把一个懂施工企业财税的人的经验，整理成 AI 可以反复读取和执行的工作说明书。

## Skill 到底是什么

在这个项目里，skill 就是一个 `.md` 文件。每个文件负责一个相对明确的财税能力。

例如：

- `ccfts-fr-all-flash-report-workflow`：施工企业财务快报编制流程
- `ccfts-tax-all-vat-cross-region-prepayment`：跨区域施工项目 VAT 预缴
- `ccfts-fr-all-retention-money`：质保金处理
- `ccfts-anlys-project-unit-profitability`：项目盈利能力分析

普通提示词通常是一段一次性的要求。Skill 更像可复用的专业作业指导书：它有名称、适用范围、依赖关系、输入材料、处理步骤、输出格式、风险提示和人工复核点。

## 它能实现什么

你把相关 skill 提供给 AI 后，AI 可以更稳定地完成这些事情：

- 判断一个主体是 SPV 项目公司、项目部、子公司还是集团层级
- 根据科目余额表生成施工企业快报映射思路
- 检查资产负债表是否平衡、损益表口径是否合理
- 判断 VAT 一般计税、简易计税、跨区域预缴的适用场景
- 列出企业所得税预缴、汇算清缴中常见的纳税调整风险
- 分析项目盈利、现金流、垫资、两金、清收清欠
- 给出质保金、竣工结算、变更索赔、亏损合同等场景的检查清单

它不会自动保证结论正确。它的价值是让 AI 不再只靠临时发挥，而是按一套稳定的行业工作流来辅助你。

## 装到哪里

你有三种常见用法，从简单到高级。

### 方式一：直接给 AI 读取

这是最容易理解的方式。

你可以把某几个 skill 文件复制进 AI 对话，或者把整个 `skills/` 目录作为项目资料交给支持文件上下文的 AI 工具。

适合：

- ChatGPT / Claude / Gemini / DeepSeek 这类对话工具
- Codex / Claude Code / Cursor 这类能读项目文件的 AI 编程或 agent 工具
- 只想试一下，不想安装任何东西的用户

示例提问：

```text
请阅读以下 CCFTS skills，并按这些规则帮我检查施工企业快报：
1. ccfts-fr-all-flash-report-workflow
2. ccfts-fr-all-entity-type-rules
3. ccfts-fr-all-quick-report-mapping
4. ccfts-fr-all-balance-sheet

我会提供一份科目余额表。请先判断主体类型，再列出映射逻辑、缺失信息和人工复核点。
```

### 方式二：放进你的 AI workspace

如果你已经有自己的 AI workspace，推荐把这个项目作为“可复用专业知识库”放进去，而不是每次临时复制。

一种常见结构：

```text
AI workspace/
  20_references/
    domain-skills/
      china-construction-fintax-skills/
```

之后你在不同项目里都可以引用同一套技能：

```text
请使用 AI workspace/20_references/domain-skills/china-construction-fintax-skills/skills 中的相关 skill，
帮我处理这个项目部 2026 年 5 月快报。
```

这样做的意义是：你的 AI workspace 不再只是文件堆放区，而是多了一层可复用、可版本管理、可测试的专业能力层。

### 方式三：通过 MCP 接入

MCP 是给 AI 客户端使用外部工具的一种协议。这个项目提供了可选的 MCP server，让支持 MCP 的客户端通过工具调用来列出、搜索和读取 skill。

适合：

- Claude Desktop
- Cursor
- Codex MCP
- 其他支持 MCP 的 agent 客户端

安装方式：

```bash
git clone https://github.com/philip-wong2026/china-construction-fintax-skills.git
cd china-construction-fintax-skills/mcp
python3 -m pip install -e .
```

然后在 MCP 客户端里配置 `ccfts-mcp`。详细检查步骤见 [../mcp/SMOKE_TEST.md](../mcp/SMOKE_TEST.md)。

如果你只是新手试用，不建议一开始就走 MCP。先用“直接读取 skill 文件”的方式理解价值，再考虑 MCP。

### 方式四：使用现成场景包

如果你只会用豆包、马维斯这类桌面 AI 助手，最简单的方式不是打开 96 个 skill 文件，而是使用 `agent-packs/`。

场景包是把多个相关 skill 的使用方法压缩成一个更容易上传、复制和执行的 Markdown 文件。

例如：

- 豆包检查快报：`agent-packs/doubao/flash-report.md`
- 豆包检查 VAT 跨区域预缴：`agent-packs/doubao/vat-prepayment.md`
- 马维斯读取本地文件夹检查财税资料：`agent-packs/marvis/desktop-finance-review.md`
- Trae Solo 项目型接入：`agent-packs/trae-solo/README.md`

使用方式：

1. 打开你的 AI 工具
2. 上传一个场景包
3. 上传脱敏业务数据
4. 复制场景包里的提示词
5. 检查输出里的人工复核清单

## 跟现在的 AI workspace 有什么升级

没有 skills 的 AI workspace，常见问题是：

- 提示词散落在各个聊天里，难以复用
- 每次换一个 AI 工具，都要重新解释业务背景
- 专业规则没有版本记录，不知道哪次改了什么
- AI 输出有没有按规则检查，很难追踪
- 经验在人的脑子里，不容易变成团队资产

加入 CCFTS 这类 skills 后，AI workspace 会多出一层“专业能力资产”：

- **可复用**：同一套施工企业财税规则可以给 Claude、Codex、Cursor、DeepSeek 使用
- **可追踪**：所有 skill 都是 Markdown 文件，可以用 GitHub 管理版本
- **可检查**：项目有验证脚本和 GitHub Actions，能发现结构和引用问题
- **可扩展**：未来可以增加更多行业、税种、主体层级、真实验证案例
- **可协作**：别人可以围绕某个 skill 提 issue、提交修正、补验证样本

简单说，它把 AI workspace 从“资料仓库”升级成“带专业操作说明的 AI 工作系统”。

## 哪些 AI 工具能用

| 工具 | 能不能用 | 推荐方式 |
|---|---|---|
| Codex / Claude Code | 能 | 直接读取 repo 或配置 MCP |
| Trae Solo | 能 | 打开 repo，必要时配置 MCP |
| 豆包 Desktop / Web | 能，但用简化方式 | 上传 `agent-packs/doubao/` 场景包 |
| 腾讯马维斯 | 能，但取决于版本能力 | 读取本地文件夹或上传 `agent-packs/marvis/` |
| 手机端 AI | 只能轻量用 | 复制单个场景包和提示词 |
| 腾讯云 Agent / CloudBase | 能，但需要工程化 | 上传为知识库，或未来接 MCP SSE |

详细接入说明见 [integrations/README.md](integrations/README.md)。

## 一个完整使用例子

假设你要让 AI 帮你检查某项目公司的月度快报。

### 你准备的材料

- 科目余额表
- 报表期间
- 主体说明：这是 SPV 项目公司还是施工项目部
- 是否季度末、年末
- 如果有对照表，提供企业原报表结果

### 你让 AI 读取的技能

从 [../START_HERE.md](../START_HERE.md) 里选择“场景 1：我要编施工企业快报”，加载推荐 skill。

最小集合可以先用：

- `ccfts-workflow-base`
- `ccfts-fr-all-flash-report-workflow`
- `ccfts-fr-all-entity-type-rules`
- `ccfts-fr-all-quick-report-mapping`
- `ccfts-fr-all-profit-statement`
- `ccfts-fr-all-balance-sheet`

### 你可以这样问 AI

```text
请按 CCFTS 的施工企业快报流程处理这份科目余额表。

要求：
1. 先判断主体类型，并说明判断依据和置信度。
2. 给出科目到快报项目的映射表。
3. 输出利润表和资产负债表草稿，单位万元。
4. 检查资产负债表是否平衡。
5. 列出需要人工复核的问题，不要把不确定项当成确定结论。
```

### AI 应该输出什么

- 主体类型判断
- 缺失信息清单
- 科目映射表
- 利润表草稿
- 资产负债表草稿
- 差异和风险点
- 人工复核 checklist

你再用 [manual-review-template.md](manual-review-template.md) 逐项复核。

## 新手最容易误解的地方

### 它不是自动报税软件

CCFTS 不会替你登录电子税务局，也不会自动完成申报。它是辅助 AI 理解施工企业财税规则和工作流。

### 它不是最终专业意见

所有输出都需要人工复核。特别是税务、审计、监管报送、年报、重大经营决策，必须由专业人员确认。

### 它不是越多 skill 一起加载越好

一次只加载和当前场景相关的 skill。先从 [../START_HERE.md](../START_HERE.md) 的推荐顺序开始。

### 它不是必须用 MCP

MCP 只是高级接入方式。直接读取 Markdown 文件就能使用核心价值。

### 它不会替代真实数据验证

项目目前是 public alpha。它需要更多脱敏真实案例、人工复核记录和可复现实验来提高可信度。

## 建议学习顺序

1. 先读本文件，理解 skills 是什么
2. 再读 [../START_HERE.md](../START_HERE.md)，选择一个真实场景
3. 打开 `examples/` 看脱敏 demo 输入和 expected 输出
4. 把 3-6 个相关 skill 文件交给 AI 读取
5. 用自己的脱敏样本试一次
6. 用 [manual-review-template.md](manual-review-template.md) 做人工复核
7. 熟悉后再考虑 MCP 接入

## 最小可用提示词

如果你不知道怎么开始，可以直接复制下面这段：

```text
你现在要使用 CCFTS（China Construction Enterprise Finance & Tax Skills）辅助我处理中国施工企业财税问题。

请先阅读我提供的相关 skill 文件，并遵守这些要求：
1. 只在 skill 支持的范围内给出结论。
2. 遇到缺失数据，先列出需要补充的信息。
3. 区分确定结论、推断结论和必须人工复核的事项。
4. 不要把 AI 输出包装成最终合规意见。
5. 输出最后必须包含“人工复核清单”。

我的业务场景是：[在这里填写，例如：项目部月度快报 / SPV 快报 / VAT 跨区域预缴 / CIT 预缴 / 质保金处理]
我提供的数据是：[在这里说明你会提供什么文件或表格]
```
