---
variant: post-wide
title: "Timekeeping Parameter"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [Temporal Compression](/temporal-compression) and [Consolidation Codec](/consolidation-codec).*

Any system that keeps time under bounded memory converges on the same structure: store complete states occasionally, differences the rest of the time. The ratio is the keyframe rate — the survival parameter of temporal compression.

### Why it converges

Three constraints force the structure:

1. **The buffer is finite.** You can't store every moment at full resolution.
2. **The sequence has temporal dependencies.** Later states depend on earlier ones.
3. **Accumulated error grows with chain length.** Each delta drifts from the original. Over enough steps, the reconstruction becomes unusable.

Given these constraints, any system that doesn't periodically store a complete state drifts past recovery. The checkpoint is a necessity, not an optimization. The only free parameter is how often.

### The evidence

The same five-part architecture appears independently across eleven domains. Technical systems (top rows) are precise; institutional and cultural systems (lower rows) less exact but structurally recognizable.

| Domain | Checkpoint (I-frame) | Delta (P-frame) | Cycle (GOP) | Break (chain fragility) | Reset |
|---|---|---|---|---|---|
| **Video codecs** | Intra-coded frame | Predicted frame | GOP | Reference loss | Keyframe insertion |
| **git** | Base object / packfile snapshot | Delta object | Repack cycle | Corrupted object | Re-clone / fsck |
| **Databases** | WAL checkpoint | Write-ahead log entry | Checkpoint interval | Log corruption | Recovery from checkpoint |
| **ML training** | Model checkpoint | Gradient update | Checkpoint interval | NaN / divergence | Rollback to checkpoint |
| **Accounting** | Balance sheet | Journal entry | Month-end close | Audit discrepancy | Reconciliation |
| **Oral poetry** | Formulaic epithet | Improvised variation | Performance segment | Audience lost | Re-invoke formula |
| **Common law** | Landmark case | Subsequent opinion | Era of precedent | Overturned ruling | New landmark |
| **Religion** | Founding myth | Cultural practice | Liturgical cycle | Schism | Reformation / revival |
| **Nation-state** | Founding document | Legislation / amendment | Political generation | Constitutional crisis | New constitution |
| **Scientific paradigm** | [Paradigm](https://en.wikipedia.org/wiki/The_Structure_of_Scientific_Revolutions) (Kuhn) | Normal science | Research program | Anomaly accumulation | Revolution |
| **Software architecture** | Clean-sheet design | Feature additions | Major version | Technical debt collapse | Rewrite |

Eleven domains. Same architecture. The top five are precise: git's packfile delta compression is I-frame/P-frame encoding on a DAG, and database WAL checkpointing is GOP structure. The lower six are structural analogies, less exact but recognizable.

### What kills systems

Systems that get the keyframe rate wrong fail in predictable ways.

**Too few keyframes (drift → death):**

| System | What happened | Chain length | Source |
|---|---|---|---|
| **Boeing 737** | 57 years of inherited fuselage design, never a clean-sheet redesign. Engines mounted forward to fit, MCAS to mask pitch-up tendency. 346 dead. | 57 years, 4 generations | [Seattle Times](https://www.seattletimes.com/seattle-news/times-watchdog/the-inside-story-of-mcas-how-boeings-737-max-system-gained-power-and-lost-safeguards/) |
| **Kodak** | Invented digital camera in 1975, refused to reset founding assumption (photography = film). Bankruptcy 2012. | 37 years | [MIT Sloan](https://sloanreview.mit.edu/article/the-real-lessons-from-kodaks-decline/) |
| **Qing Dynasty** | 268 years without structural reform. Three failed partial resets (Self-Strengthening, Hundred Days, New Policies), each too late. Fell 1912. | 268 years | [Britannica](https://www.britannica.com/place/Qing-dynasty) |
| **Zoroastrianism** | State religion of Persia → 200,000 worldwide. Orthodox refusal to accept converts. No mechanism to replenish. | ~1,400 years | [Pluralism Project](https://pluralism.org/news/zoroastrianism-dying-out-modern-times) |
| **Ariane 5 Flight 501** | Reused Ariane 4 inertial reference software without re-verifying against new flight profile. Integer overflow 37 seconds after launch. $370M lost. | 1 transplant | [MIT report](http://sunnyday.mit.edu/nasa-class/Ariane5-report.html) |
| **South Korea (TFR)** | Post-war I-frame: industrialize or die. Never decompressed after crisis ended. Reproduction was never in the checkpoint. TFR 0.75, population projected to halve by 2100. | 70 years | [Statistics Korea](https://kostat.go.kr) |

**Too many keyframes (overhead → death):**

| System | What happened | Reset frequency | Source |
|---|---|---|---|
| **France 1791–1870** | 14 constitutions in 80 years. No regime lasted long enough to build legitimacy. | ~1 every 6 years | [Wikipedia](https://en.wikipedia.org/wiki/List_of_constitutions_of_France) |
| **Mao's Continuous Revolution** | Permanent ideological reset destroyed institutions faster than they could function. 500K–2M dead. | Continuous | [Stanford SPICE](https://spice.fsi.stanford.edu/docs/introduction_to_the_cultural_revolution) |
| **Khmer Rouge Year Zero** | Total reset: all culture, institutions, professions destroyed and rebuilt from scratch. 2M dead out of 7M. | Single total | [Wikipedia](https://en.wikipedia.org/wiki/Year_Zero_(political_notion)) |
| **Italy (postwar)** | 68 governments in 76 years. No policy trajectory can accumulate momentum. | ~1 every 13 months | [Euronews](https://www.euronews.com/my-europe/2022/10/21/italy-is-set-for-its-68th-government-in-76-years-why-such-a-high-turnover) |
| **Digg v4** | 100% rewrite discarded all accumulated community features. Lost 30% of audience in one month. Couldn't roll back. | Single total | [SearchEngineLand](https://searchengineland.com/digg-v4-how-to-successfully-kill-a-community-50450) |

**Got it right (calibrated keyframe rate → survival):**

| System | Keyframe rate | Duration | Why it works | Source |
|---|---|---|---|---|
| **Catholic ecumenical councils** | ~1 per 90 years (21 in 1,900 years) | 1,700 years | Slow enough for continuity, frequent enough to prevent fatal drift. Trent answered the Reformation. Vatican II answered modernity. | [Catholic Answers](https://www.catholic.com/magazine/print-edition/the-21-ecumenical-councils) |
| **British constitution** | Incremental partial keyframes (Magna Carta, Reform Acts, Parliament Acts) | 800 years | No total reset, ever. Gradual expansion within stable institutional frame. | [PolSci Institute](https://polsci.institute/comparative-politics/gradual-evolution-of-british-constitution/) |
| **Vedic oral transmission** | Continuous (11 redundant recitation modes) | 3,000+ years | Redundant encoding as continuous error correction. Group verification — any mistake triggers restart. | [IJFMR](https://www.ijfmr.com/papers/2025/6/59645.pdf) |
| **Aboriginal songlines** | Landscape-anchored (physical terrain as external keyframe) | 7,000+ years | External reference frame immune to cognitive drift. Multi-modal encoding (song, dance, painting). | [Scientific American](https://www.scientificamerican.com/article/ancient-indigenous-songlines-match-long-sunken-landscape-off-australia1/) |
| **US Supreme Court** | ~1 reversal per year (141 in 170 years) | 170 years | Stare decisis as default, with rare landmark reversals for constitutional drift. | [Constitution Center](https://constitutioncenter.org/blog/a-short-list-of-overturned-supreme-court-landmark-decisions) |
| **Swiss Confederation** | Distributed (26 cantons reset independently) | 734 years | Federalism distributes keyframes across scales. Cantons can reset without destabilizing the whole. | [Liberty International](https://liberty-intl.org/2000/03/12/the-swiss-cantonal-system-a-model-democracy/) |
| **The Mishnah** | Emergency keyframe (~200 CE) | Chain saved | Oral Torah deliberately kept unwritten. Temple destruction threatened the chain. Emergency checkpoint to persistent storage. | [Chabad](https://www.chabad.org/library/article_cdo/aid/6173507/jewish/Why-Was-the-Talmud-Written.htm) |

### What the tables show

**1. Too few keyframes kills slowly.** Boeing drifted for 57 years. The Qing for 268. Korea is drifting now. Accumulated error becomes structural, and the system can no longer distinguish what it is from what it was supposed to be. By the time someone calls for a reset, the cost of a keyframe exceeds what the system can bear.

**2. Too many keyframes kills fast.** France cycled through 14 constitutions in 80 years. Mao's Continuous Revolution destroyed institutions faster than they could function. The Khmer Rouge destroyed the substrate itself. Each reset discards accumulated P-frames that took years to build. Reset too often and nothing accumulates.

**3. The survivors calibrate.** The Catholic Church resets once per century. The British constitution patches continuously without ever fully resetting. The Vedas use redundant encoding as continuous error correction. Aboriginal songlines anchor to physical terrain that doesn't drift. None found the rate by theory. All found it by selection: the ones that got it wrong aren't here to compare.

### Trauma compresses the keyframe

South Korea's population crisis is a keyframe written under duress, never decompressed after the pressure lifted.

The pre-war I-frame was Confucian: family continuity, ancestor worship, filial piety. Reproduction was in the checkpoint. The Korean War destroyed everything. [Park Chung-hee](https://en.wikipedia.org/wiki/Park_Chung_Hee) wrote a new I-frame from rubble: industrialize or die. Intentionally monodimensional — a traumatized society rebuilding from nothing can't afford a complex checkpoint. A simple I-frame compresses well, transmits easily, aligns the population toward a single objective.

It worked. One generation: agrarian poverty to OECD.

Then the crisis ended and the I-frame didn't update. Family formation, communal obligation, generational continuity were never re-encoded into the new reference. They existed only as P-frame inheritance, increasingly distant from the active checkpoint. When accumulated economic and social pressure compressed the P-frames, reproduction was the first thing dropped. It was never in the I-frame. It was never protected from drift.

### The downstream consequences

The standard explanations are downstream. Housing is expensive because the society optimized for one dimension and never re-encoded livability. Work culture is brutal because the I-frame says sacrifice, and every institutional delta since 1960 has been faithful to that reference. Education is a pressure cooker because the checkpoint rewards competition, not formation. These are consequences. The root cause is what the I-frame encodes and what it doesn't.

"Economics" fails because Israel has [higher cost of living](https://www.numbeo.com/cost-of-living/compare_countries_result.jsp?country1=Israel&country2=South+Korea) and a [TFR of ~2.9](https://data.worldbank.org/indicator/SP.DYN.TFRT.IN?locations=IL). "Culture" fails because it doesn't specify which parameter. The keyframe framing does: Israel's I-frame encodes reproduction ("[be fruitful and multiply](https://en.wikipedia.org/wiki/Be_fruitful_and_multiply)" is in the Torah, which is the I-frame). Korea's doesn't. What's in the checkpoint is protected from drift. What isn't gets compressed away.

The generalization: *the severity of the trauma that forces a new I-frame determines its dimensionality.* The more severe, the simpler. Simple I-frames are adaptive in crisis. In peace, they become the chain that can't encode what matters.

### The parameter

The keyframe rate is not a design choice. It emerges from three quantities:

- **Buffer size** — how much state the system can hold
- **Error accumulation rate** — how fast deltas drift from the reference
- **Checkpoint cost** — how expensive a complete state is to store

Every system in the tables discovered this tradeoff independently. Codecs formalized it as [rate-distortion optimization](https://en.wikipedia.org/wiki/Rate%E2%80%93distortion_theory). Legal systems as [stare decisis](https://www.law.cornell.edu/wex/stare_decisis) with rare reversals. Religions as liturgical cycles with occasional councils. The formalism differs. The parameter is the same.

The systems that persist found, by trial or by selection, a keyframe rate matched to their constraints. The systems that died didn't. This is more than metaphor. It is the consequence of keeping time with a finite buffer.

### How to prove this wrong

Score founding documents for dimensionality. Constitutional preambles, national curricula, liturgical texts, corporate mission statements — count how many distinct social functions each one encodes. Reproduction, education, defense, commerce, leisure, spiritual practice, environmental stewardship. Each is either in the checkpoint or it isn't.

Then measure which outcomes survived a century of drift and which didn't.

The prediction: outcomes encoded in the founding document persist under pressure. Outcomes absent collapse first when the system is stressed. If Korea's founding documents encode development but not family formation, and Israel's encode both, and the TFR tracks that difference after controlling for GDP, housing cost, and female labor participation — the parameter is real.

If it doesn't track — if I-frame content has no predictive power over which outcomes survive drift — the framework is wrong. Not "needs refinement." Wrong. Run the test.

---

*Written via the [double loop](/double-loop). For the technical crosswalk: [Temporal Compression](/temporal-compression). For the formal reading section: [june.kim/reading/temporal-compression](https://june.kim/reading/temporal-compression/).*
