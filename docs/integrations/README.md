# 不同 AI 工具怎么用 CCFTS

这页写给不懂技术的人。

CCFTS 不是一个 App，也不是一个网页系统。它是一套“给 AI 看的施工企业财税说明书”。不同 AI 工具的用法不一样。

## 先看你会用哪种工具

| 你会用的工具 | 怎么用最合适 | 难度 |
|---|---|---|
| 豆包桌面端 / 网页端 | 上传一个场景包，再上传脱敏表格 | 最简单 |
| 腾讯马维斯 | 让它读取本地文件夹或上传场景包 | 简单 |
| Trae Solo | 打开整个项目目录，让它读取 skills | 中等 |
| Codex / Claude Code / Cursor | 打开项目目录，或配置 MCP | 中等 |
| 腾讯云 Agent / CloudBase | 做成企业知识库或内部智能体 | 较复杂 |

## 如果你只会用豆包

不要管 `skills/`、`MCP`、`GitHub clone` 这些词。

你只需要用这里的文件：

- [豆包：施工企业快报检查](../../agent-packs/doubao/flash-report.md)
- [豆包：VAT 跨区域预缴检查](../../agent-packs/doubao/vat-prepayment.md)

用法就是：

1. 打开豆包。
2. 上传上面的一个场景包。
3. 上传脱敏后的 Excel、CSV、Word 或截图。
4. 复制场景包里的提示词。
5. 看豆包输出的结果和“人工复核清单”。

## 如果你会用马维斯

看这一页：

- [马维斯使用说明](marvis.md)

简单说，就是把这个项目当成本地资料夹，让马维斯读取一个场景包，再处理你的脱敏文件。

## 如果你会用 Trae Solo

看这一页：

- [Trae Solo 使用说明](trae-solo.md)

Trae Solo 更适合懂项目目录、会让 AI 读取文件的人。它可以直接打开整个 CCFTS 项目。

## 如果你是企业信息化或数字化部门

看这一页：

- [腾讯云 Agent / CloudBase 使用说明](tencent-cloud-agent.md)

这条路不是给普通财务人员自己折腾的。它适合企业把 CCFTS 做成内部知识库或内部财税助手。

## 一句话建议

普通用户先用 `agent-packs/`。
开发者再看 `skills/` 和 `mcp/`。
企业部署再考虑腾讯云 Agent 或 MCP 服务化。

