When you build an API, your customer needs to integrate it, so you write an SDK. It just wraps an API with a cache layer and some retry logic. Your customers use four different languages, so all four SDKs need maintenance. You deal with:

- Client-server version mismatches
- Migration guides on every API change
- Transitive dependencies nobody reads
- Support tickets from deprecated endpoints
- Compatibility matrices across runtimes

Your customer already knows what's coming when you say "SDK." And you're not their only vendor. How many customers did you lose before they even tried your product?

![A briefcase opened flat, revealing a team of small robots in foam cutouts alongside manuals and data cores, deployment ready](/assets/agents.jpg)

## Send a Text File

A skill is a set of human-readable instructions that runs on the recipient's LLM. Every engineering team already relies on Claude Code or Codex, and they can trust what they can read.

I'm building an ad exchange. The publisher integration is four skills:

- **evaluate.md** — a Forward Deployed (FD) Revenue Agent that assesses whether ads make sense for the publisher's chatbot
- **install.md** — an FD Engineer that writes the integration directly into the publisher's codebase, checkpoint by checkpoint
- **verify.md** — an FD Auditor that audits the integration for HIPAA, FTC, and state privacy compliance
- **uninstall.md** — an FD Engineer that cleanly removes the integration and all its artifacts

No code, all text. The publisher's coding assistant reads the skill, asks clarifying questions, and generates the code needed. An SDK can't [elicit](/elicitation) requirements from your customer, but a skill can.

A skill also welds modules into your customer's codebase, using their HTTP client, their error handling, their logging, and their UI components. After the PR merges, there's no seam. It's their code now.

It ships with everything it needs: API schemas, system prompts, config defaults, and compliance checklists. The parts that need to be exact (endpoint URLs, payload shapes, embedding model names) are code examples that state-of-the-art models copy verbatim. Determinism where it matters, flexibility everywhere else.

## Readable by Default

When an SDK fails, you get a stack trace with a support email.

When a skill runs, the agent's reasoning is logged in natural language. The audit trail is a consequence of the medium.

Every team that uses Claude Code already has a CLAUDE.md, a file that tells the agent how this codebase works, what conventions to follow, what to avoid. The agent is already aligned to the team's standards, and a skill inherits that alignment for free.

The PR is still the customer's accountability. The skill proposes changes; a human reviews and merges. The same code review process the team already trusts. Don't YOLO vendor skills. Use protection.

Healthcare, finance, and legal adopt new software slowly because compliance review of opaque vendor code takes months. Skills skip the entire queue. The compliance officer reads a few sentences of English and approves it the same afternoon. The bottleneck was never the technology. It was the lack of transparency.

## When SDKs Still Win

When you need high-throughput, deterministic execution, skills fall apart. Stripe's SDK handles cryptographic signatures, retries with exponential backoff, and webhook verification at thousands of requests per second. You don't want an LLM doing that. Anything that requires exact numerical computation, sub-millisecond latency, or binary protocols still belongs in compiled code.

> Mechanical, performance-critical: ship an SDK.
>
> Interpretive, trust-critical: ship skills.

## No Version Matrix

Even where SDKs win on execution, they create coordination problems. A server SDK and a client SDK have to ship together. Version mismatches between them cause silent failures. Deprecated API calls linger for months because upgrading one side means upgrading both. Skills sidestep all of this. The skill says what to do in plain language, and the LLM figures out the current way to do it.

When a skill does need to change, the vendor ships an **update.md**: a second prompt that migrates the first. The recipient's agent reads both, applies the diff, done. The recipient can test it before running it: spin up a subagent, feed it sample inputs, verify the outputs match expectations. Testing is delegated to the same coding agent.

## The New Executable

Software shipped as binaries you couldn't read. Open source made the code readable, but the build artifacts stayed opaque. With skills, what you read assembles into code that runs.

Skills are the new unit of software distribution for anything that touches an LLM. This is the layer of abstraction above code that everyone's been speculating about. It's just instructions.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose.*
