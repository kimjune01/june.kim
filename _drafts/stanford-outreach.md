# Stanford Faculty Outreach

Emails for [friend's name] to send from their Stanford address. One email per professor, personalized to their work.

---

## Michael Ostrovsky (GSB, Economics)

Co-wrote the foundational GSP auction paper. Your piece proposes what comes after GSP.

**Subject:** Embedding vectors as ad auction primitives

Hi Professor Ostrovsky,

I'm [name], an undergrad at Stanford. A friend of mine has been working on a proposal for embedding-based ad auctions, replacing keyword matching with vector similarity as the core signal. He built simulations showing that when advertisers declare a position and radius (sigma) in embedding space, with relocation fees to prevent gaming, specialists earn more per impression than generalists.

Given your work on the GSP auction, I thought you'd find his argument interesting.

Overview (10-min scrollytelling): https://www.june.kim/advertising-journey/
Technical details on the geometric allocation: https://www.june.kim/power-diagrams-ad-auctions/

I've CC'd him here if you'd like to reply directly.

Best,
[name]

---

## Vasilis Syrgkanis (MS&E, CS)

Works on auto-bidding in ad auctions, mechanism design + ML.

**Subject:** Mechanism design for embedding-based ad auctions

Hi Professor Syrgkanis,

I'm [name], an undergrad at Stanford. A friend of mine has been developing a proposal for ad auctions where the bid request carries an embedding vector instead of keywords. Advertisers declare both a position and a sigma (radius of competence) in embedding space. He shows that adding a relocation fee makes honest positioning the greedy-optimal strategy.

Overview (10-min scrollytelling): https://www.june.kim/advertising-journey/
Scoring parameter analysis: https://www.june.kim/the-price-of-relevance/

He's CC'd here if you'd like to follow up.

Best,
[name]

---

## Gabriel Weintraub (GSB, Operations)

Studies display ad auctions, expert witness in DOJ adtech antitrust cases.

**Subject:** Open protocol for embedding-based ad auctions

Hi Professor Weintraub,

I'm [name], an undergrad at Stanford. A friend has been working on a proposal to extend OpenRTB with embedding vectors, carrying the full semantic signal from chatbot conversations into the auction instead of collapsing it to keywords. He argues this changes the equilibrium structure: specialists can outbid generalists on relevant queries, and relocation fees prevent the field from collapsing back to a keyword bin.

Given your work on digital advertising auctions and the DOJ antitrust cases, I thought you'd want to see this.

Overview (10-min scrollytelling): https://www.june.kim/advertising-journey/
Industry landscape and convergence: https://www.june.kim/the-convergence/

He's on CC if you want to discuss.

Best,
[name]

---

## Susan Athey (GSB, Economics)

Online advertising economics, former DOJ Chief Economist during Google antitrust.

**Subject:** Embedding auctions as alternative to keyword monopoly

Hi Professor Athey,

I'm [name], an undergrad at Stanford. A friend of mine has been working on a proposal for how ad auctions should work on chatbots. Chatbot conversations already produce embedding vectors, but OpenRTB has no field to carry them, so the signal gets crushed back to keywords, recreating the same market structure Google controls.

He proposes an open protocol where advertisers declare positions and radii in embedding space, with relocation fees that make honest positioning incentive-compatible. The structural claim is that the protocol boundary is what preserves monopoly.

Overview (10-min scrollytelling): https://www.june.kim/advertising-journey/
Simulation of specialist vs. generalist surplus: https://www.june.kim/keyword-tax/

I've CC'd him if you'd like to respond directly.

Best,
[name]

---

## Navdeep Sahni (GSB, Marketing)

Runs field experiments on search advertising effectiveness.

**Subject:** Embedding similarity as ad signal

Hi Professor Sahni,

I'm [name], an undergrad at Stanford. A friend has been working on embedding-based ad auctions, matching ads by vector similarity rather than keyword overlap. His simulations show improved value efficiency and specialist surplus when the full semantic signal is preserved through the auction.

The empirical claim is that higher-dimensional intent signals improve match quality and conversion. Your experimental work on search advertising seems like the right lens for this.

Overview (10-min scrollytelling): https://www.june.kim/advertising-journey/
The protocol bottleneck (why OpenRTB can't carry embeddings): https://www.june.kim/embedding-gap/

He's CC'd here.

Best,
[name]

---

## Dan Boneh (CS, Applied Cryptography)

Privacy-preserving computation. The TEE trust layer in the proposal is his domain.

**Subject:** TEE-attested ad auctions

Hi Professor Boneh,

I'm [name], an undergrad at Stanford. A friend has been building a proposal for ad auctions on chatbots where the auction runs inside a TEE. The exchange triggers computation but can't read embeddings, alter logic, or change outputs. The result carries a cryptographic attestation that the published code ran unmodified.

His argument is that this is the only way to build an ad layer that doesn't require trusting the exchange. Your work on privacy-preserving computation is directly relevant.

Overview (10-min scrollytelling): https://www.june.kim/advertising-journey/
Concrete proposal for TEE-attested exchange: https://www.june.kim/letter-to-cloudx/

I've CC'd him here if you'd like to reply.

Best,
[name]

---

## Ravi Jagadeesan (Economics)

Auction design under collusion. The relocation fee is an anti-gaming mechanism.

**Subject:** Relocation fees as anti-gaming mechanism in embedding auctions

Hi Professor Jagadeesan,

I'm [name], an undergrad at Stanford. A friend has been working on embedding-based ad auctions where advertisers declare a position and radius in vector space. Without constraints, advertisers abandon their niches and crowd the center (Hotelling-style collapse). His fix is a relocation fee proportional to position drift, which makes honest positioning the profit-maximizing strategy.

Given your work on auction design under collusion, I think the anti-gaming mechanism would interest you.

Overview (10-min scrollytelling): https://www.june.kim/advertising-journey/
Relocation fee mechanism and simulation: https://www.june.kim/relocation-fees/

He's on CC if you want to discuss.

Best,
[name]

---

## Ellen Vitercik (MS&E / CS)

ML-optimized mechanism design. Tuning auction parameters with data.

**Subject:** Data-driven sigma optimization in embedding auctions

Hi Professor Vitercik,

I'm [name], an undergrad at Stanford. A friend has been working on a proposal where ad auctions match on embedding vectors, and advertisers declare a sigma (radius of competence). The optimal sigma is self-correcting: too narrow loses volume, too wide burns budget on bad matches. The parameter space is continuous.

Your work on using ML to optimize auction parameters seems directly applicable.

Overview (10-min scrollytelling): https://www.june.kim/advertising-journey/
Scoring parameter sweep and tradeoffs: https://www.june.kim/the-price-of-relevance/

He's CC'd here if you'd like to follow up.

Best,
[name]
