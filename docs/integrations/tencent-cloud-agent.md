# Tencent Cloud Agent / CloudBase Integration

## Compatibility

Tencent Cloud Agent / CloudBase-style platforms are a stronger enterprise fit than consumer chat apps because they can use knowledge bases, workflows, plugins, and deployment channels.

CCFTS can be integrated in two stages:

1. Knowledge-base mode: upload Markdown skills as a domain knowledge base.
2. Tool mode: expose CCFTS as an MCP SSE or HTTP service for structured search and retrieval.

The current repository ships a local stdio MCP server under `mcp/`. For cloud platforms that require SSE/HTTP MCP, an adapter still needs to be built.

## Stage 1: Knowledge Base

Recommended first enterprise deployment:

1. Create a private knowledge base.
2. Upload:
   - `README.md`
   - `START_HERE.md`
   - `docs/beginner-guide.md`
   - selected `skills/` files
   - selected `agent-packs/` files
3. Configure the Agent role instruction:

```text
You are a China construction enterprise finance and tax assistant.
Use CCFTS only as a reference and checklist source.
Ask for missing business facts before giving a conclusion.
Always separate confirmed facts, assumptions, risk points, and manual review items.
Never present output as final compliance advice.
```

4. Add example questions for first-time users.
5. Test with anonymized validation cases before internal rollout.

## Stage 2: MCP SSE / HTTP Adapter

Build a cloud adapter only after knowledge-base mode proves useful.

Target capabilities:

- list available skills
- search skills by scenario
- read a skill by slug
- return recommended skill bundles
- return manual review checklist by task type

Possible future directory:

```text
mcp-sse/
  server.py
  deployment.md
  tests/
```

## Enterprise Controls

Before production use, define:

- data classification rules
- upload restrictions
- audit logs
- user permission scope
- professional review workflow
- retention and deletion policy
- validation cases and acceptance thresholds

## Limits

- Cloud deployment is an engineering project, not just a documentation task.
- CCFTS is still public alpha and CPA review is pending.
- A knowledge-base agent can retrieve rules, but it still needs workflow design and evaluation before enterprise use.

