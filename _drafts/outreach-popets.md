# Outreach: PoPETS 2026, Making Sense of Private Advertising

## Mayank Varia (BU), Gabriel Kaptchuk (UMD), Kyle Hogan (MIT)

You proved leakage is inherent in any useful ad system. I think the proof assumes the exchange sees the query. What if it doesn't?

I designed an ad protocol for AI conversations where privacy is architectural, not policy. Four constraints:

1. **The chatbot can't see ads.** Separate TEE enclaves, one-directional data flow. The model generating the answer doesn't know advertising exists. https://june.kim/model-blindness

2. **The exchange can't see user data.** It receives an embedding inside a sealed enclave, runs the auction, returns a result. The conversation never leaves the publisher. https://june.kim/monetizing-the-untouchable

3. **The advertiser can't link impressions to outcomes.** Attribution uses blind signatures. The exchange sees envelope counts, never coupon values or customer identities. https://june.kim/croupier

4. **The user initiates.** No ad fires until the user opts in. https://june.kim/ask-first

The first market is health chatbots. HIPAA-governed conversations that publishers can't monetize under current adtech.

Everything is copyleft (AGPL): 50+ posts, open-source code, a formal auction proof in Lean 4. Anyone can run an exchange; any proprietary derivative must open its source. Full series: https://june.kim/vector-space

Does TEE isolation + blind signatures change your leakage bounds? I think it does. The exchange never sees the query, and the advertiser can't reconstruct it from outcomes. But I can't prove that in your framework. That's the collaboration.

June Kim
https://june.kim

Contact:
- Mayank Varia: varia@bu.edu
- Gabriel Kaptchuk: kaptchuk@umd.edu
- Kyle Hogan: klhogan@csail.mit.edu
