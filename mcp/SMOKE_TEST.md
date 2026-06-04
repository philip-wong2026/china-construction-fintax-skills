# CCFTS MCP Server — Smoke Test Guide

## 安装

```bash
cd china-construction-fintax-skills/mcp
python3 -m pip install -e .
```

**前置依赖**：`mcp>=1.0.0`（通过 pip 自动安装）

## 启动

```bash
ccfts-mcp
```

MCP server 通过 stdio 与客户端（Claude Desktop / Cursor / Codex）通信，不暴露 HTTP 端口。

如果 `ccfts-mcp` 不在 `PATH` 中：

```bash
python3 -m pip show -f ccfts-mcp
```

查找输出中的脚本路径（例如 Python 安装目录下的 `bin/ccfts-mcp`），并在 MCP 客户端中使用完整路径。

## 需验证的工具

### 1. `list_skills`

**验证内容**：
- 返回所有 97 个技能的基本信息（slug/description/jurisdiction/category/entity_levels）
- 可按 `jurisdiction` 过滤（CN / GLOBAL）
- 可按 `category` 过滤（financial-reporting / accounting / tax 等）
- 返回字段必须包含 `entity_levels`（非废弃的 `entity_types`）

**预期**：`list_skills(category="intelligence")` 返回 16 条结果。

### 2. `list_intelligence`

**验证内容**：
- 返回所有 intelligence 类技能
- 可按 `authority` 过滤（SASAC / MOF / STA / MOHURD）

**预期**：`list_intelligence(authority="SASAC")` 返回 4 条结果。

### 3. `get_skill`

**验证内容**：
- 按 slug 返回完整 Markdown 内容
- 附加 provenance footer（jurisdiction / quality / version）
- 旧 slug 通过别名映射到新 slug

**测试 slug**：
- 新 slug：`ccfts-fr-all-rounding-rules`
- 旧 slug（别名）：`ccfts-rounding-rules` → 应映射到 `ccfts-fr-all-rounding-rules`

### 4. `resolve_references`

**验证内容**：
- 解析指定 slug 的依赖链
- 返回 `depends_on` + `references` 列表
- 返回 `total_files_to_load`
- 旧 slug 自动映射

**测试 slug**：`ccfts-fr-all-profit-statement`

### 5. `search_skills`

**验证内容**：
- 按关键词在全文中搜索
- 返回匹配的 slug + 上下文片段

**测试查询**："营业收现率"

### 6. `start`

**验证内容**：
- 按自然语言意图推荐技能加载列表
- 返回 `intent`（匹配的意图类型）和 `recommended_skills`

**测试意图**："我要编制月度财务快报"

## 当前安装状态

本地已验证：
- `mcp` Python package 可安装（测试环境版本：1.27.2）
- `ccfts-mcp` editable package 可安装（测试环境版本：0.3.0）
- `ccfts_mcp.server` 可导入，helper/parser 层可解析关键 slug

尚需在目标 MCP 客户端中逐项确认以下工具调用。不要仅凭 Python 导入成功就宣称客户端 smoke test 完整通过。

## 轻量自测（无需安装 mcp）

在项目根目录运行：

```bash
# 测试 parser 层（无需 MCP runtime）
python3 tests/test_mcp_loading.py

# 测试全部技能完整性
python3 tests/test_skill_integrity.py
python3 scripts/validate-skills.py
```

**当前自测结果**：
- `test_mcp_loading.py`：5/5 slugs passed
- `test_skill_integrity.py`：97 files, 0 errors
- `validate-skills.py`：97 files, 0 issues

## 已知限制

- 完整 MCP smoke test 需要安装 `mcp>=1.0.0` 并在 MCP 客户端（如 Claude Desktop / Cursor / Codex）中逐工具调用
- `slugs_aliases` 映射仅覆盖 7 个旧 slug → 新 slug 的场景
- MCP server 未做并发/超载测试
- `search_skills` 的全文搜索在大规模技能库下未做性能测试
