---
layout: post
title: Lessons from Building Skillomatic
tags: coding, projects
---

> This post was written by Claude Opus 4.5. I prompted it to find patterns in the [Skillomatic](https://skillomatic.technology/) codebase, then validated each one against existing literature to filter out the common stuff. What remains are ideas I haven't seen documented elsewhere.

---

### The Compose-Then-Submit Pattern

LLMs hallucinate. We know this. The usual fix is to add more examples, more guardrails, more evals. But there's a simpler pattern that I haven't seen named elsewhere.

When a user creates a skill via chat in Skillomatic, two things happen:

1. **Composition**: The LLM loads a special skill that contains validation rules, valid integrations, and examples
2. **Submission**: The LLM calls a tool to submit the skill to the API, which validates again

The key insight is that you load the rules into context _before_ generation, not after. The LLM sees what's valid before it starts writing. Then the server validates again as a safety net.

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│ Load Rules  │ --> │ LLM Composes │ --> │ API Validates│
│ into Context│     │ with Rules   │     │ (safety net) │
└─────────────┘     └──────────────┘     └──────────────┘
```

This is different from "propose-then-execute" because the rules aren't just shown to the user—they're shown to the LLM. It's guided generation, not post-hoc validation.

The validation rules live in a markdown file in the database. No code changes needed to update them. When the LLM sees examples of valid integrations (`email`, `calendar`, `crm`), it stops inventing ones that don't exist.

---

### Curated Manifests vs OpenAPI Generation

The lazy approach to MCP tools is to auto-generate them from OpenAPI specs. Point at a spec, get tools. But this creates security nightmares.

Business APIs have endpoints for user management, schema changes, bulk deletes. If you auto-generate tools from the full API, Claude can see all of them. Even if you validate permissions at call time, the LLM might _suggest_ dangerous operations to users who don't know better.

Skillomatic uses hand-curated manifests instead. Each provider gets ~25 safe operations, explicitly listed:

```typescript
{
  id: 'list_contacts',
  access: 'read',
  description: 'List contacts with filters',
  // ...
}
```

When tools are generated at runtime, they're filtered by user access level. Read-only users don't see write tools. Claude can't offer what doesn't exist.

This is more work than auto-generation. But the benefits compound:
- **Security**: Explicit allowlist means dangerous operations never register
- **UX**: Hand-written descriptions help Claude understand nuances
- **Portability**: Skills work across providers because tools are described consistently
- **Reliability**: Each operation has an explicit access level, enabling predictable runtime behavior

That last point matters more than it sounds. Because each manifest operation declares its required access level, you can filter at registration time—not call time. If Claude sees a tool, it will work. No "permission denied" errors mid-conversation. The tool list IS the capability list.

The MCP security literature talks about tool poisoning and supply chain attacks. But it doesn't talk much about the architectural choice to curate rather than generate. That's the lesson here.

---

### Ephemeral Architecture

Most SaaS platforms store everything. User data, API responses, logs with full request bodies. This creates compliance headaches.

[Composio](https://composio.dev/blog/secure-ai-agent-infrastructure-guide) calls this pattern "Brokered Credentials"—the LLM never sees tokens, a secure service makes API calls on its behalf. Skillomatic takes a similar approach but pushes it further:

- OAuth tokens fetched fresh from Nango at render time, not stored locally
- LLM calls happen client-side—the server never sees the conversation
- The API proxy forwards requests without logging bodies

```
Server: "Here's a fresh token"  -->  Client  -->  LLM
   ^                                   |
   |                                   v
 Nango                            Third-party API
(token store)                    (proxied, not logged)
```

The server becomes a coordinator. It doesn't know what data you're accessing. It can't leak what it doesn't have.

---

### Security Through Absence

The obvious approach to MCP authorization: register all tools, validate permissions at call time, return errors for unauthorized requests.

[Composio](https://docs.composio.dev/docs/fetching-tools) takes a better approach—filter tools by permission level before the LLM sees them. Their SDK supports `permissions=["read"]` to limit to read-only operations.

Skillomatic does the same thing, powered by the curated manifests:

```typescript
const tools = manifest.operations
  .filter(op => accessLevel >= op.requiredAccess)
  .map(op => generateTool(op));
```

This is becoming a best practice for MCP authorization. Make unauthorized operations invisible rather than forbidden. You can still misuse the tools that exist, but you can't misuse the ones that don't.

---

### Floats for Onboarding Steps

Onboarding flows change. Product wants to squeeze a step between "connect Google" and "generate API key." With enums, that's a migration. With integers, you're renumbering.

So I used floats:

```typescript
const ONBOARDING_STEPS = {
  ACCOUNT_TYPE_SELECTED: 0.5,
  GOOGLE_CONNECTED: 1,
  API_KEY_GENERATED: 3,
  FIRST_SKILL_RUN: 4,
  COMPLETED: 5,
};
```

Need "install extension" between 3 and 4? Use 3.5. No migration.

Checking if a step is done:

```typescript
if (user.onboardingStep < ONBOARDING_STEPS.GOOGLE_CONNECTED) {
  // show google connection hint
} else {
  // dont show google connection hint
}
```

Advancing by name:

```typescript
// Client calls by name, server handles the float
onboarding.completeStep('GOOGLE_CONNECTED');
```

Schema defines constants. Client uses names. Server compares floats. Clean separation.

It's a silly trick. But it works.

---

> These lessons emerged from building [Skillomatic](https://skillomatic.technology/), a platform that connects AI assistants to business tools. This post was written by Claude Opus 4.5.
