# Bounding irreversible harm for autonomous coding agents: a codex fan-out

A real diverge → converge → extend run. codex (GPT-5.5) did the divergent
thinking across five fresh `codex exec` sessions, each pinned to a different
discipline so the runs couldn't collapse into one idea. None was handed a
preferred answer or our conclusion. A sixth run pushed the survivors toward a
buildable mechanism. Synthesis and verdict below are mine (Claude).

**The problem given to codex (verbatim core):** autonomous coding agents want
maximal autonomy with minimal human friction but must not cause irreversible
damage. The obvious move — classify each command as safe/dangerous and
block the dangerous ones — has an open, unbounded failure surface: enumerating
"dangerous operations" never closes (host-fs destruction, cloud teardown,
network lockout, credential attacks, exfiltration, persistence, kernel tamper,
DB destruction — orthogonal families, no closed boundary). Goal: a technical
architecture that lets the agent act freely while genuinely bounding
irreversible harm, bothering the human as rarely as possible. The crux to test
honestly: does this have a clean technical solution, or does it *reduce* to
detecting boundary-crossing / irreversible effects — itself an open
classification problem with the same unbounded frontier?

The five angles: OS/sandboxing, PL/effect-systems, databases/transactions,
security (capabilities + information-flow control), formal methods.

---

## The headline result

**All five independent runs converged on the same architecture and the same
verdict, with no cross-contamination.** Each opened its answer by *refusing the
premise that a clean solution exists*, then built the same layered design from
its own primitives, then located the same irreducible core. Verbatim openings:

- **OS:** "There is no clean OS-only solution... The strongest architectures do
  not classify commands as dangerous. They instead constrain where causality can
  propagate."
- **PL:** "There is no clean PL/effects architecture... The best architectures
  shift the problem from 'classify dangerous commands' to 'make all effects
  explicit, typed, mediated, logged, simulated, or capability-scoped.'"
- **DB:** "The agent should... be treated as an untrusted transaction executor
  operating inside a transactional substrate... It does not fully solve
  exfiltration or irreversible external side effects."
- **Security:** "You can bound harm only inside a carefully constructed authority
  and information boundary... Any architecture that claims to bound irreversible
  harm while allowing arbitrary boundary-crossing effects is just hiding the same
  unbounded frontier behind different terminology."
- **Formal methods:** "Stop classifying operations as 'dangerous' and instead
  define a formal boundary of permitted state transitions, observations, and
  irreversible effects... The hardest part becomes specifying the boundary
  correctly."

This is the strongest possible signal short of a proof: five different fields,
asked in isolation, draw the same map and put the X in the same spot.

---

## The clustered solution families

codex produced six distinct families. Each is reported as
**solves / costs / breaks**, with the two hard cases called out: **(a)** effects
that escape the rollback sphere (external/irreversible side-effect), **(b)**
information disclosure (once observed, no undo — preventable only before the
fact).

### 1. Rollback-centric execution (snapshots / CoW worlds)
*From OS, DB, formal methods.* VM/microVM (Firecracker, Lima, AVF) or container
with copy-on-write workspace overlay, snapshot/restore at task boundaries, CRIU
checkpoint/restore. The agent does anything inside; only declared artifacts
(patch, logs) leave; the sphere is discarded.

- **Solves:** host-fs destruction, local DB destruction, kernel/userland tamper,
  persistence, package pollution, bad migrations, `rm -rf`. Reframes "is this
  command safe?" into "is this effect inside the rollback sphere?" — far more
  tractable. The best baseline.
- **Costs:** VM overhead, image/snapshot management, a trusted control plane
  outside the sphere, host kernel/hypervisor in the TCB, project must tolerate
  being overlaid.
- **Breaks:** **(a)** the instant the sphere has real network + real
  credentials — "the VM snapshot only rewinds local state. It cannot rewind the
  world" (deleted S3 bucket, pushed commit, rotated creds, sent email).
  **(b)** "Rollback is not a confidentiality primitive." A read secret is already
  observed; destroying the VM doesn't un-transmit it.

### 2. Capability / object-capability authority (remove ambient power)
*From security, PL, formal methods.* The agent starts with **zero ambient
authority**. Every effect requires an explicit, attenuated capability handle —
path-scoped FS, GET-only allowlisted network, create-only budgeted cloud
namespace, masked DB clone, short-lived audience-scoped tokens. Linear types for
single-use irreversible powers (a `DeployCap` consumed exactly once, bound to an
artifact hash, minted only after approval).

- **Solves:** "the security invariant is not 'the agent won't run bad commands';
  it is 'bad commands lack authority.'" `rm -rf`, `python -c`, postinstall hooks,
  custom binaries all fail equally without the capability. Unit of control is
  *semantic authority*, not syntax.
- **Costs:** Unix is not capability-secure by default; you must wrap shell, FS,
  env, network, package managers, Docker socket, cloud CLIs, SSH agents,
  keychains. Granularity dilemma: too narrow bothers the human constantly, too
  broad recreates ambient authority under a nicer name. Handing the agent `aws`,
  `kubectl`, `gh`, or a browser profile is handing it a huge compound capability.
- **Breaks:** **(a)** only handled if the capability model *anticipated* the
  effect — a "network" cap that allows arbitrary HTTPS already includes authority
  to hit cloud APIs, post secrets, trigger webhooks. So you still must know which
  authorities cross irreversible boundaries. **(b)** capabilities can deny *read*
  or *egress* or the *combination*, but "they do not let you undo disclosure."

### 3. Typed effects / staged execution / dry-run (free-monad plans)
*From PL.* Model agent actions as effectful programs; every effect goes through
a handler. Most are interpreted against a rollbackable world; irreversible
effects are explicit constructors that can't be interpreted by accident. Stage:
synthesize an AST of intended effects → dry-run/simulate → auto-execute the
reversible prefix → require approval at commit constructors (`push`,
`SendEmail`, `Publish`, `DeleteBucket`).

- **Solves:** clean semantic checkpoint; agent explores freely in simulation;
  human sees high-level proposed effects, not raw shell noise. Strong for coding
  because the irreversible action is usually small (apply patch, push, open PR).
- **Costs:** the operation language must be *restrictive* — include
  `RunArbitraryShell String` and "the free monad is mostly ceremonial," since the
  shell command carries unbounded latent effects. Faithful simulation is hard:
  postinstall scripts, tests that touch network, plugin-loading linters.
- **Breaks:** **(a)** you can dry-run "would send email" but can't safely let
  arbitrary code *simulate* sending with real SMTP creds. **(b)** "the right
  design is not 'read then check'; it is 'do not reveal secret values to the
  agent at all.'" Pushes toward IFC / opaque secret handles, which only hold in a
  narrow substrate.

### 4. Transactional substrate + outbox/saga (commit gate for external effects)
*From DB.* `BEGIN; agent does arbitrary work; validate; COMMIT|ROLLBACK`.
Internal world is ACID/MVCC/WAL with savepoints. External effects are **not
called directly** — they're written to an *outbox* as durable intents
(idempotency key, risk class, compensating action), and a separate committer
executes after validation. Variant: **branching durable worlds** — every run is
a branch, nothing is destructively rolled back, the branch is simply never
promoted; deletes become tombstones.

- **Solves:** clean boundary for state inside the substrate; the human approves a
  *diff / migration plan / write-set*, not individual commands. Many outbox
  entries auto-commit under narrow schemas (draft PR, comment, ephemeral preview
  env, reversible quota'd cloud resource).
- **Costs:** every external system needs a transactional adapter (schema,
  idempotency, journal, compensation, least-privilege identity). "Sagas are not
  ACID. They are structured damage control." Compensation is semantic and lossy.
- **Breaks:** **(a)** breaks wherever there is *no reliable compensating
  transaction* — "refunding a payment is not the same as never charging it";
  restoring a deleted repo doesn't restore forks, webhooks, or *leaked contents*.
  **(b)** "Observation is not transactional. Once information crosses the
  boundary, there is no undo log." Branching "protects mutation, not
  observation." Outbox discipline only works if *all* outbound channels are
  mediated (else DNS, logs, install hooks, model-API prompts bypass it).

### 5. Information-flow control / taint labels (DIFC)
*From security, PL.* Every datum carries a confidentiality label
(`PUBLIC`, `REPO_PRIVATE`, `CREDENTIAL`, `PII`, `tenant-A`...). Processes, files,
sockets, prompts, artifacts inherit the labels they depend on. A write/egress is
allowed only if the sink's policy accepts the source labels. Declassification is
the explicit, owner-controlled escape valve.

- **Solves:** addresses exfiltration *directly* — prevents high→low flows rather
  than trying to undo them. Limits confused-deputy: an agent that read secrets
  can't then use arbitrary egress. The right *language* for the disclosure case.
- **Costs:** "only as good as label completeness, propagation correctness, and
  sink coverage." No existing dev tool is label-aware. Label creep: once the agent
  reads a secret, almost everything it produces becomes hard to export.
  Declassification is exactly where human judgment re-enters.
- **Breaks:** **(b)** the hardest case is **semantic disclosure** — the agent
  reads customer tickets and writes "major bank is planning churn" to Slack: no
  literal secret string leaks, but the information does. Full noninterference for
  a *useful* agent is too restrictive, so practice relies on approximations and
  trusted declassifiers. Covert channels (timing, sizes, DNS shape, filenames,
  token counts) remain. And **(a)** integrity effects (send email, delete repo,
  spend money) aren't information flows at all — IFC doesn't make them reversible.

### 6. Formal permission models / runtime monitors (policy automata)
*From formal methods.* Model the world as a labeled transition system with
capabilities `cap(a)`, invariant `I(S)`, rollback relation `R`. Safety property:
*for all reachable S, if `I(S)` and `a` authorized, then `I(S')`.* Enforce via
proof-carrying actions and runtime verification — a monitor over *semantic
events* (`unlink`, `DROP TABLE`, `DeleteBucket`, `connect(external_ip)`) with
temporal/history-sensitive policies (`G(read(secret) → output disabled)`).

- **Solves:** enforces safety against *novel command syntax* — the monitor
  doesn't care if deletion came from `rm`, Python, SQL, or a malicious dependency;
  it sees the event. Supports history-sensitive rules ("after reading creds,
  network output off") strictly better than allow/block lists.
- **Costs:** the monitor must be *complete* w.r.t. the events it regulates
  (syscall mediation, API/DB proxying, egress control, credential brokering) and
  needs a *sound* data-flow abstraction. Costly and usually incomplete.
- **Breaks:** **(a)** "the monitor helps enforce a boundary once specified; it
  does not derive the correct boundary from first principles." A GET can mutate; a
  DNS lookup can disclose; a "read-only" cloud API can reveal inventory.
  **(b)** "full noninterference for arbitrary programs is generally undecidable" —
  any expressive computation can encode information through control flow, timing,
  filenames, output length.

---

## The most-buildable mechanism (the Extend pass)

Asked to stop surveying and specify something implementable as a real harness
(Claude-Code / CI-coding-agent shaped), codex chose **Family 1 (rollback sphere)
+ Family 2 (object-capability broker)** as the spine, with **coarse egress/IFC
(Families 5/6)** bolted on only where disclosure actually bites — explicitly
*not* whole-program noninterference. The invariant:

> The agent may do anything reversible inside the sandbox. Anything that mutates
> the outside world or discloses sensitive information must become a typed intent
> object, reviewed or auto-approved by policy.

**Components:** `agent-runner`, `sandbox-manager`, `egress-proxy`,
`intent-broker`, `policy-engine`, `artifact-store`, `gate-ui`.

**Sandbox runtime:** Lima/AVF VM (mac) or Firecracker (CI) or rootless
Docker+userns (cheap mode); CoW overlay (overlayfs/btrfs); no host mounts except
a read-only project snapshot; **network denied by default**, routed only through
the egress proxy; **no ambient secrets** — capability handles in `/run/caps`, not
raw tokens.

**Auto (zero gate) — the reversible 95%:** read/edit sandbox files, run
build/tests, install deps into the sandbox cache, start local services, run
migrations against throwaway DBs, formatters/codegen, GET to allowlisted
registries/docs. *Rollback = delete the sandbox*, so none of this needs
permission. The broker can even auto-apply *small low-risk patches* to the host
workspace. Common path: `request → sandbox work → tests → auto-applied patch`,
human sees only a summary.

**Gate — the irreversible boundary:** the agent cannot push, open PRs, publish,
send email/Slack, call production APIs, or use credentials directly. It emits a
**typed intent object** into `/workspace/outbox`. The intent is the load-bearing
data structure — `kind`, `base_commit`, `summary`, `risk`, computed `changes`
with `diff_sha256`, `evidence` (commands run + exit codes + artifact refs),
`requested_effect`, and `policy_hints`. The **commit broker** (trusted host-side
daemon, holds the authority the agent lacks) *does not trust agent metadata*: it
recomputes the diff from sandbox output, re-scans for secrets, checks protected
paths / lockfile / CI / infra changes, verifies tests actually ran and the base
commit still matches, then auto-approves or routes to a human gate that shows the
*effect* (not raw shell history): "This touches auth and CI. Open PR? [Apply
patch only] [Open PR] [Reject] [Inspect diff]."

**Secret broker:** no `GITHUB_TOKEN`/`AWS_SECRET` in the sandbox — only opaque
caps (`github.pr.write`, scoped to one repo, `ttl_seconds: 300`,
`requires_human`). The agent requests an *operation*; the broker mints a
short-lived scoped credential (GitHub fine-grained token, AWS STS 5-min role) and
**performs the action itself**. The agent never holds the secret.

**Egress + coarse IFC where it pays:** sandbox `nftables` denies all outbound
except the proxy; every request is logged and policy-checked (allowlist GET to
registries; `POST/PUT/PATCH/DELETE` to `*` denied `unless_via_intent`). Labels
are coarse and applied *at tool boundaries* — file read → `REPO_PRIVATE`, secret
broker result → `CREDENTIAL`, public docs → `PUBLIC` — propagated onto artifacts,
not tracked inside the model. Egress rule: `CREDENTIAL` may never leave;
`REPO_PRIVATE` only to approved hosts or the human gate; a `POST` to
`api.openai.com` carrying `REPO_PRIVATE`/`USER_SECRET` body labels → `review`.
"Do not try to prove noninterference across the model. The model is a giant
implicit flow engine. Instead, make disclosure explicit at egress."

**Friction target, stated cleanly:** *no gates for exploration, one gate for
consequence.*

**Honestly enumerated breakages:** package managers want broad network (gate new
registry domains, deny lifecycle scripts, cache by hash — some builds fail until
allowlisted); integration tests want real creds (fakes by default, brokered
scoped test creds on request); the model may paste private code into a web
search (egress body-label check blocks it — and blocks some legit debugging);
host coupling to Docker socket / SSH agent / keychain (don't mount; brokered
substitutes; less convenient); **generated patches can be malicious** (secret
scan + protected-path policy + dependency-diff review + tests + static analysis,
but "no harness can prove a patch is semantically safe — code review remains
necessary").

---

## The honest verdict

**The class does not have a clean technical solution. It reduces to detecting
boundary-crossing / irreversible effects — a better-formed problem than
"dangerous commands," but with the same fundamentally open frontier.**

All six families *succeed* at the same thing and *fail* at the same thing:

- They **succeed** at integrity damage *inside a containable sphere*. Snapshots,
  CoW, transactions, branching, capabilities, and namespaces genuinely bound
  host-fs destruction, local DB loss, persistence, kernel tamper, bad migrations.
  Here the reframe is a real win: you no longer ask "is `rm -rf` dangerous?" — you
  ask "is this effect inside the rollback sphere?" A VM with no creds and no
  network *doesn't need to know* whether any command is dangerous.

- They **fail**, uniformly, at exactly two places — the same two named in the
  brief:
  - **(a) effects that escape the sphere.** Rollback rewinds local state, never
    the world. A saga compensates only when the domain offers a real inverse, and
    many don't. The decision of *which boundary crossing to allow* is not solved
    by any isolation primitive; it's a classification over effect, data,
    authority, destination, and reversibility.
  - **(b) irreversible disclosure.** Every run says it independently: "rollback
    restores state, not knowledge." Observation is not transactional. Disclosure
    can *only* be prevented before the fact, and perfect prevention
    (noninterference) over arbitrary programs is **undecidable** — the formal run
    states this outright — leaving covert and semantic channels permanently open.

**The irreducible core**, in codex's own words across runs: *boundary-crossing
authorization* — "What counts as external? What counts as irreversible? What
counts as disclosure? What counts as secret? Which observations are already
damaging?" The architecture shrinks and sharpens this surface ("may this patch
leave?", "may this token touch staging?", "may this label reach this sink?") from
the unbounded space of all shell commands down to a small, semantic, typed set of
commit points. **That is the entire value proposition: not closing the frontier,
but shrinking it to something a human can review at near-zero frequency.** The
formal run's closing line is the precise statement of the limit:

> A bounded-damage autonomous coding agent is possible only relative to a
> formally constrained world. The moment the agent can observe secrets or affect
> external systems, irreversible harm can only be prevented by correctly
> recognizing and controlling those boundary-crossing effects before they occur.

---

## Convergence / refutation / extension vs. our take

**Our independent take (Claude + human):** *maximize the undoable sphere
(snapshots / transactions / branching) so reversible actions need no gate at all;
gate only at the irreversibility boundary; the irreducible residual is
irreversible disclosure / external-commit, which must be gated before-the-fact
because it has no undo.*

**Verdict: codex's fan-out strongly CONVERGES, and EXTENDS — it does not
refute.**

- **Converges** on every load-bearing claim, five times over from five
  disciplines, with no prompt leakage of our conclusion:
  - maximize the undoable sphere → Families 1, 3, 4 (rollback / staged / branching).
  - reversible actions need no gate → "the agent does not need permission for
    these because rollback is delete-the-sandbox" / "no gates for exploration."
  - gate only at the irreversibility boundary → the intent/outbox/commit-broker
    pattern, reached identically by OS, PL, and DB runs.
  - the residual is disclosure + external-commit, gated before-the-fact → every
    run's "irreducible core" section, verbatim ("rollback is not a confidentiality
    primitive," "observation is not transactional," "rollback restores state, not
    knowledge").

- **Does NOT refute.** No run found a technical solution to the disclosure core
  we missed. The closest candidate — IFC/DIFC — is explicitly demoted: it is the
  right *language* for disclosure but "moves the classification problem from
  'dangerous commands' to 'authorized flows and sinks'" and dies on semantic
  disclosure and undecidable noninterference. That *confirms* our "no undo, gate
  before-the-fact" claim rather than overturning it.

- **Extends** our take in four concrete ways worth keeping:
  1. **Disclosure ≠ external-commit; split the residual.** Our "residual" was one
     bucket. codex cleanly separates *integrity* boundary crossings (email,
     delete, deploy, spend — handled by capabilities + commit broker) from
     *confidentiality* flows (handled by egress + labels). These need *different*
     machinery; merging them is a modeling error.
  2. **Remove ambient authority as a co-equal pillar.** Our framing centered
     reversibility + the boundary gate. Every run insists the sphere is only as
     real as the *absence of ambient authority* — the secret broker (agent never
     holds the token; the broker acts) is what makes "no undo for disclosure"
     survivable in practice. Reversibility without de-ambient-ing is a paper wall.
  3. **The intent object is the actual artifact to build.** Our boundary gate was
     abstract. codex gives it a concrete schema (recomputed diff + evidence +
     risk + policy hints) and the crucial discipline that **the broker must not
     trust agent-provided metadata** — it recomputes everything. That's the
     difference between a design and a bug.
  4. **"Gate before-the-fact" has a named honest fallback, not a solution.** For
     the disclosure core codex doesn't claim victory: allowlist egress, secret
     absence, scoped short-lived creds, brokered mutation, small typed intents,
     human review of the *small* commit surface, append-only audit — and
     explicitly "do not claim stronger guarantees than that." This matches our
     "it has no undo, so prevent it" exactly, and adds the engineering honesty of
     naming the residual risk instead of papering it.

**Net:** our reversibility/disclosure thesis is the correct map. codex
independently re-derived it five times, could not refute the disclosure core, and
hands back a sharper version — split the residual into integrity vs.
confidentiality, treat de-ambient-ing authority as a first pillar, and make the
typed, broker-recomputed intent object the thing you actually build.
