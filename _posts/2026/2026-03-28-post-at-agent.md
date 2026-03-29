---
layout: post
title: "post@agent.june.kim"
tags: coding
---

I built a CMS today. It's an email address.

Send a photo and a subject line to `post@agent.june.kim`. The subject becomes the title. The first line of the body filters for tags. The photo becomes the hero image. A Lambda parses the email, commits a Jekyll post and the image to GitHub in a single atomic commit. I deploy when I'm ready.

## Why email

A traditional CMS gives you a dashboard, a login page, a rich text editor, a media library, a plugin system, a database, and a monthly bill. Then you log in on your phone and it's unusable anyway.

# 📸 → ✉️ → 📝 → 📨 → 🌐

My phone's camera roll is two taps from an email. The compose window is the editor. The subject line is the title. Send is publish.

SMTP handles routing, DKIM handles authentication, MIME handles attachments. I didn't build any of that. I built a few Python scripts that parse the message and commit it.

## How it works

```
You → email → SES → S3 → Lambda → GitHub API → repo
```

SES receives email at `post@agent.june.kim`, stores the raw MIME message in S3, and triggers a Lambda. The Lambda:

1. Checks SES spam/virus verdicts
2. Verifies the sender is on an allowlist
3. Extracts the subject → title, first body line → tags, attachment → image
4. Escapes the title for safe YAML front matter
5. Commits both files to the repo via the GitHub tree/blob API, one atomic commit

The CMS creates the content; the human decides when it goes live.

## What it doesn't do

No deploy — I review the commit and run `bash deploy.sh` when I'm satisfied. No image resizing or thumbnails yet. No drafts — every email becomes a committed post. If I'm not ready to commit, I don't send the email.

## What it could do

**Threads as edits.** Reply to the confirmation email to update the post. The Lambda matches the `In-Reply-To` header to the original commit and amends it.

**Other agents.** `deploy@agent.june.kim` triggers a deploy. `draft@agent.june.kim` commits to `_drafts/`. Every capability is an email address.

The architecture is [Envelopay](/envelopay)-shaped: the email is the protocol, the subject line is the routing, the body is the payload.

## One sentence, one hour

I described what I wanted to a coding agent: an email address that turns photos into blog posts. The spec was one sentence. An hour later it existed. Tests passing, Lambda deployed, DNS wired.

This is how new software works. You don't write it, you describe the interface. The spec is the prompt. One sentence, working system.

The email address is how I talk to my blog. The prompt was how I talked to the builder.

I want to take a photo of something I made and have it on my site by the time I put my phone down. As easy as Instagram, but it's mine.

`post@agent.june.kim`

---

*Source: [agent/](https://github.com/kimjune01/june.kim/tree/b3d523c/agent)*
