# Curated index vs forum (working title)

Sequel to [New Reading](/new-reading) and [Vibelogging](/vibelogging). Scaffold, not prose. Spine + receipts + open questions.

## Thesis

Forums hold content hostage. A curated, owned, copyleft index is the better model, because every layer of the barrier that once justified centralization has a free replacement, and the only remaining cost (curation) is the one that should be scarce.

Lived contradiction to open on: this argument was first posted to LessWrong. A forum. Use the irony, don't hide it.

## Spine

1. **Forums hold content hostage.** A forum stores your writing as a feed, not a corpus. Optimized for recency and engagement, not retrieval. Answers buried in comment threads, scrolled away, unqueryable as a whole. You wrote a module; the forum files it as a chapter in an infinite book nobody reopens. The platform owns the access pattern.

2. **"But they have an API." For now.** The API is a lease, not ownership. Recent history is revocation:
   - Reddit 2023: free API for years, then overnight pricing that killed Apollo + third-party clients; same year a ~$60M/yr Google data deal (train Gemini). Your comments sold, your access metered. https://www.reuters.com/technology/reddit-ai-content-licensing-deal-with-google-sources-say-2024-02-22/
   - Twitter/X: free tier gutted 2023, ~$42k/month for meaningful volume.
   - Stack Overflow: OpenAI licensing deal, then suspended users who tried to delete their own answers in protest. https://www.404media.co/stack-overflow-bans-users-en-masse-for-rebelling-against-openai-partnership/
   - Note who they sell to: AI labs. The exact "new readers" from New Reading. The platform monetizes the queryability you wanted and rents you back a slice.

3. **The open web already had the right model.** Decentralized nodes joined by links (Berners-Lee topology). It lost on *discovery* (didn't scale without a central index), so it recentralized into platforms that owned distribution + network effects.

4. **The discovery moat is gone, on every axis.**
   - *Algorithm:* PageRank is public (Page & Brin 1998). Stanford patent US6285999B1, exclusive to Google, **expired 2019**. No legal or conceptual wall. https://patents.google.com/patent/US6285999B1/en
   - *The crawl* (the real moat): Common Crawl gives it away. Petabytes, free.
   - *The software:* forkable + copyleft. OpenSearch forked Elasticsearch (Apache 2.0) within months of Elastic's 2021 license grab; Elastic reopened in 2024. https://www.elastic.co/blog/elasticsearch-is-open-source-again . Also Lucene/Solr, Tantivy, SearXNG; pgvector/Qdrant/Chroma/FAISS for retrieval. An embeddings index over your own corpus is a weekend.
   - *The need for global scale at all:* gone. Agents index on demand over the corpora you point them at. You don't query "the web," you query your trusted nodes.

5. **Agents are the new ranker; curation is the new link.** Whose index you point your agent at is the new vote. PageRank with a web of trust instead of a global crawl. The forum was a workaround for a discovery problem that no longer exists.

6. **Copyleft content makes the index legal and portable.** Infra forkable = you can build the index. Copyleft content = the index is allowed to serve it across many frontends at once. Share-alike: attribution travels with every copy, derivatives can't relicense closed. Content becomes portable AND tamper-evident. Inverse of the forum (immobile content, revocable attribution).

7. **POSSE.** Index is home and canonical; forum post is a pointer/billboard back to it. Keep the distribution, demote the platform from home to billboard.

## Honest caveats (keep the claim falsifiable)

- **"No barrier" overshoots if the target is "rebuild Google."** The algorithm was never the moat; scale was. The honest claim: you no longer *need* global scale, because the agent indexes on demand over a bounded curated set. That's what changed.
- **Curation is the remaining cost, and that's the point.** Dev cost → 0. Deciding what's in the index and whose nodes to trust is human labor. Fine: curation is the scarce thing New Reading already crowns (the key ring). Cost migrated to judgment, where it belongs.
- **BY vs SA is a real fork.** CC-BY = no misrepresentation of authorship. CC-BY-SA adds no-enclosure but taxes interop (incompatible with some licenses). Maximal portability sometimes argues BY or CC0. Name which you optimize for.
- **License governs copying, not interpretation.** Copyleft stops name-stripping and paywalling; it can't stop an agent summarizing you badly. Misattribution it fixes, misreading it doesn't. Defense against misreading = the provenance pointer (New Reading: agent holds the proof, you hold the pointer; copyleft keeps the pointer resolving to you).

## Possible openers
- The "for now" pull-the-floor-out move (mirror the New Reading lead question).
- "I posted this to a forum."
