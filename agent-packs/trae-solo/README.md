# Trae Solo Agent Pack

Trae Solo can use CCFTS as a project repository and optionally through MCP.

## Quick Start

Open this repository in Trae Solo and send:

```text
Use this repository as the CCFTS skill library.
Read README.md, START_HERE.md, docs/beginner-guide.md, and docs/integrations/trae-solo.md.
For my task, identify the smallest set of relevant skill files under skills/.
Before producing a finance or tax answer, ask for missing inputs and include a manual review checklist.
```

## MCP Setup

```bash
cd mcp
python3 -m pip install -e .
```

Configure `ccfts-mcp` in Trae Solo's MCP settings if available in your installed version.

## Best Tasks

- building more validation cases
- improving skills
- searching skill dependencies
- generating demo output
- maintaining repository quality

