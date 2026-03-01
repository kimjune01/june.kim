---
layout: post
title: "Beyond Text"
tags: adtech
---

*Part of the [adtech](/adtech) series.*

---

This series assumed text. The math never did. The scoring function `log(bid) - distance² / σ²` operates on distance in a vector space — it doesn't know or care whether the vector came from a sentence, a photograph, or an audio clip.

People don't only discover products and services by typing. They search by image. They watch videos. They listen to podcasts. As new AI platforms handle these modalities, they'll face the same revenue question chatbots face now. The auction mechanism is already ready for them.

## The Visual Bottleneck

Image and video advertising today follows a familiar pattern: sophisticated understanding in, crude categories out.

**Seedtag** (Madrid, $250M+ raised) calls it "neuro-contextual" advertising. Their system analyzes page content using computer vision and NLP, producing 11,000+ contextual categories from 600+ recognized objects. They expanded to CTV with video content analysis and report 3.5x higher engagement versus non-contextual targeting. At the auction boundary, all that visual understanding gets flattened into category labels. The image was analyzed at pixel resolution. The bid clears at category resolution.

**GumGum's ContextIQ** (now Verve Group) does the same thing for video. Their computer vision system understands video content at the scene level — objects, actions, sentiment, brand safety. Then it collapses that understanding into categorical output for the programmatic auction. Scene-level in, category-level out.

**Pinterest** has native visual search. Users tap the camera icon and search by image, not text. 553 million monthly active users. The platform already matches by visual content — it knows that a photo of a campus board is about rock climbing without anyone tagging it. But ad targeting routes through interest labels. The visual understanding exists on the discovery side and vanishes on the monetization side.

**YouTube CTV** targets ads based on scene-level content analysis — what's happening visually in the video, not just metadata or title keywords. Projected CTV ad revenue: $4.47 billion in 2026. The visual analysis is production-grade. The auction still clears on categories.

The pattern is identical to the text bottleneck described in [The $200 Billion Bottleneck](/embedding-gap). Every incumbent has multimodal understanding. Every incumbent flattens it at the protocol boundary. And none of them will fix it — they built the walled gardens. The fix comes from new platforms that adopt an open protocol before building a proprietary ad system.

## Shared Space

Modern multimodal models don't just analyze images or audio separately — they place everything in a single shared vector space alongside text.

[CLIP](https://arxiv.org/abs/2103.00020) (OpenAI, 2021) was the breakthrough. Trained on 400 million image-text pairs, it embeds images and text into the same 512-dimensional space. The text "rock climbing finger pulley injury" and a photograph of a swollen A2 pulley land near each other — measurable cosine similarity, not metaphor. This isn't theoretical: on the Flickr30K benchmark, OpenCLIP ViT-G/14 achieves 94.9% Recall@5 for text-to-image retrieval — given a text description, the correct image is in the top 5 results 95% of the time. CLIP is open-weight and reproduced under Apache 2.0 via [OpenCLIP](https://github.com/mlfoundations/open_clip). Anyone can run the model and verify the embedding independently.

[SigLIP 2](https://arxiv.org/abs/2502.14786) (Google, 2025) pushes further: 85.3% Recall@1 on COCO text-to-image — the correct image is the *top* result 85% of the time. It handles images, video, and text with multilingual support. [ImageBind](https://github.com/facebookresearch/ImageBind) (Meta, 2023) extends to six modalities in a single space — images, text, audio, depth, thermal, IMU. All open-weight.

The one most relevant to this series: [Nomic Embed Vision v1.5](https://huggingface.co/nomic-ai/nomic-embed-vision-v1.5). Open-weight, Apache 2.0. Its image embeddings are aligned with Nomic Embed Text — the same model family the series already uses for text embeddings. A text description of a service and a photograph of the problem it solves share a coordinate system.

## Same Auction, New Inputs

The scoring function doesn't change:

```
score(x) = log(bid) - distance² / σ²
```

An advertiser defines their position with a text description — same UX as the text-only case. "Licensed physical therapist specializing in rock climbing finger pulley injuries" embeds to a point in the shared space. When inventory arrives, the auction scores each advertiser by proximity to that embedding. The [power diagram](/power-diagrams-ad-auctions) tiles the space identically regardless of what produced the input vector. One calibration detail: raw cosine similarity between matched text-image pairs typically falls in the 0.20–0.35 range, lower than text-text similarity. The σ parameter would need to be tuned for cross-modal distances — wider than the text-only case — but the scoring function itself is unchanged.

A person pins a photo of a campus board. CLIP embeds the image. The climbing PT's text-defined position is close. The suggestion surfaces. No tags needed. The image content *is* the query.

A YouTube video shows someone struggling with marathon form. SigLIP 2 embeds the frame. A running coach's embedding is nearby. Matched by visual content, not video title keywords.

A podcast discusses freelance tax strategy. ImageBind embeds the audio. The freelance financial planner's position matches. Contextual targeting by what's being *said*, not show-level genre tags.

## The Trust Chain Holds

The [trust chain](/the-last-ad-layer) has three links. Each holds for multimodal inputs.

**Link 1: Verifiable embeddings.** Every model listed above is open-weight. Anyone can embed the same image and verify the vector — same property as text embeddings in the rest of the series.

**Link 2: Verifiable auction.** The TEE enclave receives an embedding vector and runs the scoring function. It doesn't care what produced the vector. The attestation proves the same code ran regardless of input modality. The [sealed auction](/perplexity-was-right-to-kill-ads) works identically. And for public content — images, videos, podcast episodes — anyone can re-embed the input after the fact to verify, which is harder with ephemeral chatbot queries.

**Link 3: Presentation.** The third link adapts. Visual context gets visual suggestions — a relevant service card alongside a pinned image. Audio context gets audio-appropriate presentation — a brief mention between podcast segments. The first two links guarantee honest matching; the third determines whether the user experiences it as help.

## The Glue Is Trivial

The models exist. The auction exists. The missing piece is a thin translation layer: accept multimodal content, run it through an open-weight model, hand the vector to the auction. That's a wrapper around an inference call.

[OpenCLIP](https://github.com/mlfoundations/open_clip) (13K+ stars, Apache 2.0) already provides production-grade CLIP inference with dozens of pretrained checkpoints. [clip-retrieval](https://github.com/rom1504/clip-retrieval) builds an end-to-end indexing and query pipeline on top of it. [Nomic Embed Vision](https://huggingface.co/nomic-ai/nomic-embed-vision-v1.5) slots directly into an ecosystem that already uses Nomic for text. None of these are ad-specific. The auction handles allocation. The model just produces the vector.

One constraint: the model must be open-weight *with a commercial license* or the exchange can't legally run it. OpenCLIP and Nomic Vision are Apache 2.0. ImageBind is CC-BY-NC — fine for research, unusable for production ad infrastructure. The model registry should enforce this: open-weight and commercially licensed, or it doesn't enter the auction.

## Inventory Without a Marketplace

Some of the richest intent signals have no ad system to receive them.

A phone camera pointed at a climbing gym wall. AR glasses scanning a kitchen mid-renovation. An AI image search for "rash that won't go away." A spatial computing app where someone walks through a furniture showroom. These platforms produce multimodal context dense with intent — but there's no marketplace for it. No keywords to bid on. No category taxonomy. No ad exchange has a slot for "what the camera is looking at."

This is the frontier case for embedding-space auctions. The content is visual or spatial. The advertiser's position is defined in text. The shared embedding space connects them without anyone building a bespoke ad product first. The protocol can be there before the marketplace — the same way HTTP was there before anyone built an e-commerce site on top of it.

An advertiser defines their position once: "Licensed physical therapist specializing in rock climbing finger pulley injuries." That position already works cross-modally. When a new platform comes online — AR, spatial, visual search — the advertiser's existing bid reaches it. Cross-modal reach is a free side effect of how the models work.

The protocol extension is one field: `embedding_model` specifies a multimodal model instead of a text-only model. Everything else — the bid, the sigma, the scoring function — stays identical.

---

*Part of the [adtech](/adtech) series. Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude researched prior art, drafted prose, and called out its own overclaims.*
