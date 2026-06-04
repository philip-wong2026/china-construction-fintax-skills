# CCFTS 测试

## 测试范围

| 测试文件 | 覆盖内容 | 依赖 |
|---------|---------|------|
| `test_skill_integrity.py` | Frontmatter 完整性、filename==name、交叉引用、质量字段 | 无外部依赖 |
| `test_mcp_loading.py` | MCP parser 对关键 slug 的解析正确性 | 无外部依赖（直接解析 markdown） |
| `test_demo_contracts.py` | Demo 目录结构、样例文件存在性、基础 expected 表内等式 | 无外部依赖 |

## 运行方式

```bash
cd /path/to/china-construction-fintax-skills
python3 tests/test_skill_integrity.py
python3 tests/test_mcp_loading.py
python3 tests/test_demo_contracts.py
```

## 当前局限

- **无完整内容级自动化测试**：不逐条验证技能正文中的会计/税务规则是否正确
- **Demo 仍是脱敏教学样例**：examples/ 中已有 input/expected，但尚未形成从 input 自动生成 output 并逐项比对的端到端回归
- **MCP 客户端集成测试缺失**：本地 helper/parser 可测，完整 MCP server 仍需在 Claude Desktop / Cursor / Codex 等客户端逐工具调用
- **测试覆盖的技能数量**：`test_mcp_loading.py` 仅抽样覆盖 5 个关键 slug，非全部 97 个

## 未来扩展方向

- 基于脱敏科目余额表 + 快报模板的端到端回归测试
- 金税四期三方比对模拟
- 业务规则断言（如"Type A 的其他应付款必为倒推"）
