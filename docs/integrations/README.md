# Agent Integrations

CCFTS is designed as a cross-agent finance and tax skill library. Different AI products have different levels of integration:

| Platform | Recommended mode | Fit | Notes |
|---|---|---:|---|
| Trae Solo | Open repo + optional MCP | High | Best for developer/project users |
| Doubao Desktop/Web | Upload scenario pack + prompt | Medium | Best for non-technical business users |
| Tencent Marvis | Local folder/scenario pack | Medium | Depends on current local-file capability |
| Tencent Cloud Agent / CloudBase | Knowledge base or MCP SSE | High | Requires engineering deployment |

Use this directory to choose the right integration path:

- [Trae Solo](trae-solo.md)
- [Doubao](doubao.md)
- [Tencent Marvis](marvis.md)
- [Tencent Cloud Agent / CloudBase](tencent-cloud-agent.md)

## Which One Should I Use

If the user understands repositories, folders, and local agent tools, start with Trae Solo.

If the user only knows how to use a chat app such as Doubao, start with `agent-packs/doubao/`.

If the user wants an enterprise application for many users, start with Tencent Cloud Agent / CloudBase and treat CCFTS as a knowledge base first.

