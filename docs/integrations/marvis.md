# Tencent Marvis Integration

## Compatibility

Tencent Marvis is positioned as an operating-system-level assistant that can understand files and help users operate their computer. CCFTS can be used with Marvis as a local document skill pack if Marvis can read the relevant folder or uploaded Markdown files.

At the current public-alpha stage, do not assume Marvis can directly run the local `ccfts-mcp` stdio server unless its product documentation or client UI explicitly supports that integration.

## Recommended Setup

1. Keep this repository in a local folder.
2. Ask Marvis to read:
   - `docs/beginner-guide.md`
   - `START_HERE.md`
   - one task-specific file under `agent-packs/marvis/`
3. Provide anonymized Excel, Word, PDF, screenshot, or CSV inputs.
4. Ask Marvis to output both:
   - business result draft
   - manual review checklist

Example prompt:

```text
请读取这个文件夹里的 CCFTS 马维斯场景包，并按其中规则帮我检查这份脱敏科目余额表。
请先说明你读取了哪些规则，再输出映射思路、异常点和人工复核清单。
不要把结果作为最终合规意见。
```

## Good Use Cases

- Local file-based review
- Desktop document summarization
- Screenshot-based checklist generation
- Simple finance/tax risk triage

## Limits

- Product capability may vary by Marvis version and platform.
- If Marvis cannot reliably read a whole folder, upload or paste the specific scenario pack instead.
- Use anonymized data unless the enterprise has approved the tool and data path.

