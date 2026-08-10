---
variant: post-wide
title: "AI Safety is Reinventing the Law"
tags: epistemology
---

AI safety has spent a decade re-deriving the conceptual inventory of law.

## Legend

- *same*: one problem, two vocabularies. The legal literature applies with the names changed.
- *port*: same content, new enforcement substrate. Law enforces through consequences on persons; the safety version must hold by construction.
- *analogy*: structural resemblance only. The doctrine does not transfer.

## Crosswalk

| AI safety term | Legal term | Relation | Note |
|---|---|---|---|
| alignment | agency law | *same* | Principal-agent problem under incomplete specification. |
| operator | principal | *same* | |
| intent alignment | duty of loyalty | *same* | The agent tries to serve the principal's ends; whether it succeeds is separate. |
| capabilities | duty of care | *same* | Fiduciary law splits loyalty from competence; [Christiano's definition](https://www.lesswrong.com/posts/ZeE7EKHTFMBs8eMxn/clarifying-ai-alignment) draws the same line independently. |
| value alignment | natural law | analogy | Norms sourced above any particular principal or sovereign. |
| outer alignment | legislative drafting | *same* | Writing text so the text picks out the intent. |
| inner alignment | subdelegation | analogy | [Delegatus non potest delegare](https://en.wikipedia.org/wiki/Delegatus_non_potest_delegare). The trained policy is a sub-agent that may not carry the mandate. |
| mesa-optimizer | sub-agent | analogy | |
| prompt injection | forged instruction | *same* | Business email compromise with the employee swapped for a model. |
| reward misspecification | incomplete contract | *same* | [Hadfield-Menell and Hadfield (2019)](https://arxiv.org/abs/1804.04268) state the identity outright. |
| specification gaming | substance-over-form doctrine | *same* | Letter satisfied, purpose defeated; the doctrine looks through the form. |
| reward hacking | defeat device | *same* | Volkswagen detected the test and optimized for it. |
| Goodhart's law | rule gaming | *same* | Tax avoidance is the canonical instance: optimize the measure, lose the target. |
| jailbreak | loophole | *same* | |
| alignment tax | compliance cost | *same* | |
| constitution (Constitutional AI) | constitution | port | Superordinate norms constraining downstream rule-making. Anthropic chose the word for the function. |
| model spec | statute | port | Enacted text, general application, enforced by training rather than courts. |
| system prompt | standing orders | port | |
| content policy | terms of service | *same* | It is a contract. |
| chain of command | hierarchy of norms | port | Supremacy ordering: platform over developer over user. [Kelsen](https://en.wikipedia.org/wiki/Hans_Kelsen) without attribution. |
| RLHF | common law | analogy | Policy accreted from judged instances rather than enacted text. |
| LLM-as-judge | judge | port | |
| red-teaming | adversarial process | *same* | Truth-finding by paid opposition. |
| honeypot eval | sting operation | *same* | Inducement invalidates the result in both. |
| capability eval | licensure examination | port | Capability tested before practice is permitted. |
| model card | mandated disclosure | port | A prospectus for a model. |
| chain-of-thought monitoring | record requirement | analogy | Reasoning on the record so review is possible. |
| interpretability | reasoned-decision requirement | analogy | Administrative law voids decisions that cannot give reasons. |
| scalable oversight | appellate hierarchy | analogy | Most decisions final at the lowest level; review above. Appeals are party-initiated, oversight is sampled. |
| human-in-the-loop | right to human decision | port | [GDPR art. 22](https://gdpr-info.eu/art-22-gdpr/). |
| corrigibility | revocability of agency | port | The principal's unilateral power to amend or terminate the agency. |
| off-switch | power of termination | port | [Hadfield-Menell et al. (2017)](https://arxiv.org/abs/1611.08219) formalize when the agent submits to it. |
| deceptive alignment | fraudulent concealment | analogy | Requires a mental state that doctrine cannot yet locate. |
| sandbagging | misrepresentation in examination | analogy | |
| treacherous turn | sleeper agent | analogy | An espionage concept; doctrine has no counterpart. |
| refusal | conscience clause | analogy | The common-carrier duty to serve is the more instructive contrast. |
| guardrails | regulation compiled to architecture | port | [Lessig (1999)](https://en.wikipedia.org/wiki/Code_and_Other_Laws_of_Cyberspace), executed literally. |
| responsible scaling policy | internal compliance program | *same* | Self-regulation drafted in anticipation of statute. |
| deployment gate | permitting | port | |
| safety case | burden of proof | port | The developer shows safety; the regulator need not show harm. |
| AI safety levels | biosafety levels | port | Regulatory classification imported with the acronym. |
| red-team safe harbor | security research exemption | *same* | The [DMCA §1201](https://www.law.cornell.edu/uscode/text/17/1201) shape, requested for models. |
| CSAM reporting | mandatory reporting statute | *same* | [18 U.S.C. §2258A](https://www.law.cornell.edu/uscode/text/18/2258A) already governs providers. |
| long-term benefit trust | trust | *same* | [Anthropic's LTBT](https://www.anthropic.com/news/the-long-term-benefit-trust) is a trust in the ordinary legal sense. |
| model welfare | animal welfare law | analogy | Duties regarding an entity, possibly duties toward one. |

## What does not transfer

Law presupposes four things the substrate does not supply.

- *Mens rea.* Every intent doctrine assumes a mind at the origin of the act: actual malice, incitement, scienter. Nobody home to take the test. Ayres and Balkin's answer is to skip the mind and hold the risky agent to objective standards.
- *Legal terminus.* Attribution rules need a party who can be found and billed. Whoever runs the model qualifies, but open weights leave the runners unregistered and too many to sue, and an agent that buys its own compute leaves no runner at all.
- *Enforcement substrate.* Law compiles norms to consequences applied to persons who fear them. Deterrence has no purchase on a forward pass.
- *Loss of control.* Law's machinery presupposes that consequences applied to humans propagate into the artifact's behavior. Loss of control names the case where the propagation fails. No legal concept survives it, because law itself does not.

Are safety and alignment just law and compliance?

## Sources

- Hadfield-Menell and Hadfield, [Incomplete Contracting and AI Alignment](https://arxiv.org/abs/1804.04268) (2019)
- Hadfield-Menell, Dragan, Abbeel, Russell, [The Off-Switch Game](https://arxiv.org/abs/1611.08219) (2017)
- O'Keefe, Ramakrishnan, Tay, Winter, [Law-Following AI](https://ir.lawnet.fordham.edu/flr/vol94/iss1/2/) (2025)
- Ayres and Balkin, [The Law of AI is the Law of Risky Agents Without Intentions](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4862025) (2024)
- Christiano, [Clarifying "AI Alignment"](https://www.lesswrong.com/posts/ZeE7EKHTFMBs8eMxn/clarifying-ai-alignment) (2018)
- Lessig, [*Code and Other Laws of Cyberspace*](https://en.wikipedia.org/wiki/Code_and_Other_Laws_of_Cyberspace) (1999)
