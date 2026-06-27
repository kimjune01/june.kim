# Junebot demo — prior art search brief

I want to add a feature to my personal Astro site (june.kim — a blog + reading site + small web apps, hosted on S3/CloudFront).

## The idea

A subtle action button next to my logo on the homepage that says "Talk to Junebot." Clicking it opens a conversational guide — a chatbot persona ("Junebot") that acts as a **tutorial / wayfinder** for the site. Its job is to help a visitor navigate each post/page: explain what's on the site, recommend where to start, walk through how to read a given post, answer "where do I find X."

It is a **legibility** aid: my site has a lot of dense epistemics/methodology posts and several apps, and a first-time visitor doesn't know the lay of the land. Junebot is the friendly orientation layer.

## What I want from you

A SMALL prior art search. Not exhaustive. I want to know:

1. **Existing patterns** for "talk to a guide bot that helps you navigate this specific website/blog." Personal-site copilots, doc-site assistants (e.g. the kind embedded in docs), "ask this site" widgets. Name concrete examples where you can.
2. **Common implementation approaches** for a static-site (Astro/S3/CloudFront, no server by default) chatbot: client-side LLM call patterns, RAG over the site's own content, prebuilt scripted/tutorial flows vs. live LLM, serverless function options.
3. **Design conventions** — where these buttons live, how they're labeled, how the tutorial/wayfinding framing differs from generic support chat.
4. **Pitfalls / what tends to feel gimmicky** vs. what actually helps orientation.

Keep it tight. Bullet points, concrete names over abstractions. Flag anything that's a strong fit for a single-author personal site (low traffic, no backend, content is markdown I control).
