# Grants for the VCG paper

Funding candidates for "The Power Diagram Auction: A Formally Verified VCG Mechanism for LLM Advertising" (Lean 4, zero sorry, artifact DOI 10.5281/zenodo.21214697). Researched 2026-07-14.

Nobody funds adtech per se. The fundable framing is formally verified economic mechanisms: extending Lean formalization beyond pure math into mechanism design, with a shipped artifact as the receipt.

## Actionable now

### 1. AI for Math Fund (Renaissance Philanthropy / XTX Markets)

The closest match. Seed grants up to $100K, reviewed on a rolling basis, for early-stage research, proof-assistant tooling, and formalization work. Open to individuals worldwide. Open-access requirement already satisfied (Zenodo artifact, arXiv preprint).

- Apply: https://www.renaissancephilanthropy.org/ai-for-math-fund
- Contact to confirm no-institution eligibility: aiformath@renphil.org
- Annual Fund ($100K to $1M, 12 to 24 months) closed March 30, 2026; recurs. Get on the list for the next cycle.
- Pitch angle: Lean formalization of mechanism design as a new domain for the formalization ecosystem. Precedent exists (Vickrey/auction theory formalizations in Isabelle AFP) but nothing at this scope in Lean 4.

### 2. Emergent Ventures (Mercatus / Tyler Cowen)

Built for individuals without institutional backing. Fast, lightweight application; grants from hundreds to tens of thousands of dollars. Cowen is an economist, so the mechanism-design content lands directly.

- Apply: https://mercatus.tfaforms.net/5099527
- Pitch angle: proved a live ad-auction scoring rule is VCG, machine-checked, and building the company that runs it. The venture angle is a feature here, not a liability.

## Possible with reframing

### 3. Ethereum Foundation academic grants

2026 call lists both Economics & Game Theory (mechanism design named) and Formal Verification as tracks. Would need reframing toward on-chain auctions or MEV rather than ad auctions.

- https://esp.ethereum.foundation/applicants

## Watch list (closed or wrong shape)

- **ARIA Safeguarded AI** (UK, £59M, davidad). Machine-checked proofs at exactly this methodological intersection, but the current call closed July 1, 2026 and awards are consortium-scale (£500K to £5M). Watch for future calls: https://aria.org.uk/opportunity-spaces/mathematics-for-safe-ai/safeguarded-ai/funding
- **Survival and Flourishing Fund**. 2026 round closed July 8; funds organizations, not individuals.
- **NSF and similar**. Needs an institutional home.

## Next actions

- [ ] Email aiformath@renphil.org to confirm independent-researcher eligibility, then submit a seed application
- [ ] Submit the Emergent Ventures application (short form, no deadline)

## Travel funding for workshop talks

The immediate need is airfare, accommodation, registration, local transport, and possibly visa costs to present the work. This is usually funded through conference-specific travel support or an invited-speaker budget, not a conventional research grant.

### Best route: acceptance, organizer support, then gap funding

1. Submit the paper or talk to a relevant workshop.
2. State during submission that travel support is required for in-person presentation.
3. After acceptance or an invitation, ask the organizers about airfare, accommodation, registration waivers, and speaker honoraria.
4. Use a small public grant or sponsorship request to cover any shortfall.

Suggested organizer email:

> Thank you—I would be glad to present. I am an independent researcher and do not have institutional travel funding. Does the workshop have support for invited or contributed speakers, including airfare, accommodation, registration waivers, or an honorarium? Even partial support would make attendance possible. I can provide a budget and book economy travel promptly.

### Manifund

The most directly usable independent-researcher option. Anyone can create a public-benefit proposal, and the platform has hosted a close precedent: an independent formal-mathematics researcher requesting travel funding to present an accepted paper at an ICML workshop.

- Open call: https://manifund.org/about/open-call
- Possible title: **Presenting Formally Verified Mechanism Design at Research Workshops**
- Possible request: **US$4,000–$8,000** for two or three events, with an itemized economy budget
- Strongest timing: after obtaining at least one acceptance or invitation

Suggested pitch:

> I produced a zero-`sorry` Lean 4 verification of a geometric VCG advertising mechanism. Funding will allow me, as an unaffiliated independent researcher, to present the result to formal-methods and economics-and-computation communities, obtain specialist criticism, and build collaborations around verified market infrastructure. The paper, proof artifact, and resulting workshop materials are openly available.

### Conference travel awards

These are worth checking event by event but often restrict eligibility to students, early-career institutional researchers, or researchers from low- and middle-income countries.

- ACM EC 2026 offered roughly **US$500–$1,000**, but its 2026 deadline has passed and non-student eligibility was principally for researchers from LMICs: https://ec26.sigecom.org/participation/travel-and-childcare-grant/
- The Artificial Intelligence Journal funding program is not a fit: it explicitly does not support individual travel requests. It may support an organization running a workshop: https://aij.ijcai.org/funding-opportunities-for-promoting-ai-research/

### Target venues

- ACM Economics and Computation (EC)
- WINE
- AAMAS
- IJCAI/AAAI workshops on mechanism design or AI economics
- ITP, CPP, FSCD, CAV, and FM
- Lean Together and formalized-mathematics meetings
- AI-for-mathematics workshops at ICML or NeurIPS

### Travel next actions

- [ ] Make a list of target workshops, countries, dates, submission deadlines, and expected budgets
- [ ] Submit talks and disclose the need for travel support
- [ ] Ask organizers for speaker support immediately after acceptance
- [ ] Create a Manifund proposal once an acceptance or invitation provides evidence of demand
