# Doubao Integration

## Compatibility

Doubao users usually need a simpler path than GitHub, MCP, or local agent configuration. The practical CCFTS mode for Doubao is:

> Upload or paste a small scenario pack, then upload anonymized business data, then ask Doubao to follow the CCFTS checklist.

Use `agent-packs/doubao/` instead of asking non-technical users to browse all 96 skill files.

## Recommended Setup

1. Open Doubao Desktop or Web.
2. Start a new chat.
3. Upload one scenario pack from `agent-packs/doubao/`.
4. Upload anonymized source data, such as a trial balance or project information table.
5. Paste the prompt included in the scenario pack.
6. Review the output using [docs/manual-review-template.md](../manual-review-template.md).

## Good Use Cases

- Quick finance/tax checklist generation
- Reading a trial balance or project information table
- Drafting flash-report mapping logic
- VAT prepayment checks
- Leadership summary drafting

## Not Recommended

- Uploading real sensitive enterprise data to a personal account
- Loading all 96 skills at once
- Treating Doubao output as final tax, audit, or reporting advice
- Production workflows without enterprise data approval

## Data Safety Rule

For state-owned enterprise or central enterprise users, do not upload original sensitive data unless your organization explicitly allows it.

Before uploading, anonymize:

- enterprise names
- project names
- tax IDs
- contract numbers
- bank accounts
- personal information
- exact commercially sensitive amounts, if needed

When possible, use scaled or sample data.

