# Trae Solo 使用入口

Trae Solo 适合会打开项目目录的人。

## 最简单用法

用 Trae Solo 打开这个项目，然后复制：

```text
请把当前项目当成 CCFTS 中国施工企业财税技能库。

请先读取 README.md、START_HERE.md、docs/beginner-guide.md。
然后根据我的任务，帮我选择最少数量的相关 skill 文件。

回答前先问我要缺失资料。
输出必须包含：
1. 已确认事实
2. 推断结论
3. 缺失信息
4. 风险点
5. 人工复核清单

不要把结果作为最终合规意见。
```

## 如果你懂 MCP

可以安装：

```bash
cd mcp
python3 -m pip install -e .
```

然后在 Trae Solo 的 MCP 设置里配置 `ccfts-mcp`。

如果你不懂 MCP，就不要管这一段。

