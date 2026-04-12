# Draft reply to "Semantic Memory in Soar" thread

To: John, Calvin, Yongjia, Steven

---

Hi all,

After the April 9 meeting I went back and re-read D&L 2013 cold, re-did my intake, and corrected the diagnosis. The short version: I was wrong about the smem/epmem eviction motivation, and I've retired PRs #578-580. The longer version is at june.kim/soap-notes-soar-revised.

John, you asked in your first email how we might evaluate and compare alternative implementations. I took that seriously and built something.

**soar-eval** is a harness that wraps Soar's existing test agents, captures per-test quantitative stats (decision cycles, production firings, WM peak, chunks learned), and diffs two builds. It's a Python script that calls the Soar CLI — no changes to the kernel required.

Two design choices that might be useful for the group:

1. **Visibility and decision are separate.** The harness reports raw deltas — what changed, by how much. A separate, configurable policy file (that the maintainer controls) decides what counts as a regression or improvement. Contributors see the numbers. The maintainer sets the criteria.

2. **It runs on existing agents.** I tested upstream vs my PR #577 across 19 chunking demo agents. One agent (BW-Hierarchical-Look-Ahead) showed 30% fewer decisions and 48% fewer production firings. Zero regressions on any other agent.

For Thursday's meeting, I'd like to demo the harness and discuss how it could help us compare our three approaches to semantic learning. If each of us writes a test agent that exercises our proposed mechanism, the harness can measure all of them on the same terms.

Yongjia, to your evaluation question — I think starting standalone and then measuring within Soar via the harness is the right two-step approach.

Looking forward to Thursday.

June
