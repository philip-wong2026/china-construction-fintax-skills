# Trae Solo 怎么用 CCFTS

这页写给会用 Trae Solo 的人。

Trae Solo 比豆包、马维斯更适合处理这类项目，因为它能打开项目目录，也更容易读取多个文件。

## 最简单用法

1. 下载或克隆这个项目。
2. 用 Trae Solo 打开整个项目文件夹。
3. 先让 Trae Solo 读取：
   - `README.md`
   - `START_HERE.md`
   - `docs/beginner-guide.md`
   - `docs/integrations/trae-solo.md`
4. 告诉 Trae Solo 你的业务场景。
5. 让它只选择相关 skill，不要一次读取全部 97 个。

## 可以直接复制这段话

```text
请把当前项目当成 CCFTS 中国施工企业财税技能库。

请先读取 README.md、START_HERE.md、docs/beginner-guide.md。
然后根据我的任务，帮我选择最少数量的相关 skill 文件。

在回答财税问题前，请先问我要缺失资料。
输出时必须区分：
1. 已确认事实
2. 推断结论
3. 缺失信息
4. 风险点
5. 人工复核清单

不要把结果写成最终合规意见。
```

## 如果要用 MCP

懂技术的人可以再配置 MCP。

安装：

```bash
cd mcp
python3 -m pip install -e .
```

然后在 Trae Solo 的 MCP 设置里配置 `ccfts-mcp`。不同版本界面可能不同，先看 Trae Solo 自己的 MCP 设置入口。

## Trae Solo 适合做什么

- 查某个财税问题应该用哪些 skill
- 改进 skill 文件
- 新增验证案例
- 运行测试脚本
- 帮这个项目继续迭代

## 注意

Trae Solo 能读项目文件，不代表它的财税结论一定正确。所有正式报送、纳税、审计、决策事项都要人工复核。
