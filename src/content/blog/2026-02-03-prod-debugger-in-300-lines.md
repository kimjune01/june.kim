---
layout: post
title: "A Prod Debugger in 300 Lines of Markdown"
tags: coding, projects
---

> This post was written by Claude Opus 4.5. The pattern is from [Skillomatic](https://skillomatic.technology/)—a Claude Code command that replaces expensive incident response tooling.

---

### The Enterprise Approach

Production debugging has become a product category:

- [Datadog Bits AI SRE](https://www.datadoghq.com/blog/bits-ai-sre/) - Autonomous investigation, proposes fixes
- [Meta's LLM root cause analysis](https://www.tryparity.com/blog/how-meta-uses-llms-to-improve-incident-response) - Fine-tuned Llama ranking causes
- [AWS Bedrock + RAG runbooks](https://devops.com/building-a-genai-rag-runbooks-based-chatops-assistant-in-aws-bedrock-with-ms-teams-integration-for-incident-management/) - Semantic search over docs

These systems have RAG pipelines, vector databases, multi-agent orchestration. They work. They also cost money.

---

### The Markdown Approach

Claude Code has custom commands—markdown files in `.claude/commands/`. Type `/prod-debugger`, Claude follows the instructions.

Mine has three things:

**1. SQL templates**
```sql
SELECT error_code, COUNT(*) FROM error_events
WHERE created_at > datetime('now', '-24 hours')
GROUP BY error_code ORDER BY count DESC;
```

**2. Error reference table**

| Code | Common Cause |
|------|--------------|
| `LLM_RATE_LIMITED` | Too many requests |
| `TOKEN_EXPIRED` | OAuth needs refresh |

**3. Output format**
```markdown
### Issue #1: Rate Limiting (85 errors)
**Root Cause:** Multiple LLM calls without backoff
**Location:** `apps/api/src/chat.ts:142`
**Fix:** [code]
```

Claude queries the DB, matches errors to causes, searches the codebase, proposes fixes. Investigation done by the time I read the output.

---

### What This Replaces

| Product | Cost |
|---------|------|
| Datadog Bits AI | $100+/mo per seat |
| PagerDuty AIOps | $30+/mo per user |
| Rootly | $20+/mo per user |
| Custom RAG pipeline | Engineering time |

You don't need semantic search over runbooks if the runbook *is* the prompt.

---

### The Pattern

Instead of:
```
Runbooks → Embeddings → Vector DB → RAG → LLM → Response
```

You get:
```
Runbook IS the prompt → LLM → Response
```

No retrieval step. The command file contains the knowledge. Claude follows it.

Won't work for massive distributed systems or compliance-heavy orgs. For those, buy the enterprise tool. For everyone else: 300 lines of markdown, no infrastructure.

---

> This post was written by Claude Opus 4.5.
