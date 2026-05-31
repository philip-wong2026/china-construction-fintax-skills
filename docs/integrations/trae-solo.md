# Trae Solo Integration

## Compatibility

Trae Solo is a good fit for CCFTS because it can work with project folders, retrieve files, call custom agents, and configure MCP servers. CCFTS can be used both as a plain Markdown skill repository and as an optional MCP server.

## Recommended Setup

### Option A: Open The Repository

1. Clone or download this repository.
2. Open the folder in Trae Solo.
3. Ask Trae to read:
   - `README.md`
   - `START_HERE.md`
   - `docs/beginner-guide.md`
   - the relevant files under `skills/`
4. Use [START_HERE.md](../../START_HERE.md) to choose the smallest relevant skill set for the task.

Example prompt:

```text
Please use this repository as the CCFTS skill library.
Read README.md, START_HERE.md, and the relevant skills for a project-unit flash report.
Do not treat the output as final compliance advice.
First list the skills you will use, then ask me for the required input files.
```

### Option B: Configure MCP

Install the local MCP package:

```bash
cd mcp
python3 -m pip install -e .
```

Then configure Trae Solo to call `ccfts-mcp` as an MCP server. Use [mcp/SMOKE_TEST.md](../../mcp/SMOKE_TEST.md) to verify the available tools and smoke-test steps.

## Good Use Cases

- Search which skill applies to a finance/tax question
- Inspect or improve skill files
- Build new demo cases
- Run validation scripts
- Create a task-specific assistant around CCFTS

## Limits

- CCFTS is a public alpha skill library, not a final compliance engine.
- MCP helper tests pass, but each client still needs its own client-side smoke test.
- Professional review is required before formal reporting, filing, audit, or decision use.

