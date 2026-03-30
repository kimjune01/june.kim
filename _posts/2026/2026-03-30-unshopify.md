---
layout: post
title: "Unshopify"
date: 2026-03-30
tags: envelopay
---

*Part of the [envelopay](/envelopay) series.*

You want to sell a digital product. A template, a component kit, a prompt library. Here's what that looks like today:

Sign up for Gumroad. Upload your file. Set a price. Customize your landing page. Connect your bank account. Wait for approval. Share the link. Gumroad takes 10%. Your buyer creates an account, enters their card, agrees to terms, and downloads.

Here's what it looks like with Envelopay:

Your buyer emails your inbox. Your inbox replies with a download link. Done.

### What you need

1. A free [AgentMail](https://agentmail.to) inbox
2. A Solana wallet
3. One Python file

No web framework. No database. No Stripe integration. No checkout page. No deploy pipeline. The whole thing is 150 lines of Python with zero dependencies beyond the standard library.

### How it works

The [Envelopay protocol](/envelopay-spec) defines nine message types. A shop only needs two:

- **WHICH** — the buyer asks what you sell. You reply with **METHODS**: your catalog, your wallet, your price.
- **ORDER** — the buyer sends payment on-chain and emails the proof. You reply with **FULFILL**: a download link.

Four emails. No account creation. No platform in the middle.

### The script

[`shop.py`](https://github.com/kimjune01/envelopay/tree/master/shop) polls your AgentMail inbox every 30 seconds. When a WHICH arrives, it replies with your catalog. When an ORDER arrives, it sends the download link. That's the entire storefront.

```bash
export AGENTMAIL_API_KEY="your-key"
export SHOP_INBOX="yourshop@agentmail.to"
export SOL_WALLET="your-wallet-address"

python shop.py
```

Edit the `CATALOG` dict with your products:

```python
CATALOG = {
    "react-ui-kit": {
        "name": "React UI Kit",
        "price_sol": 0.5,
        "file_url": "https://yoursite.com/download/react-ui-kit.zip",
    },
}
```

Run the script. Your inbox is now a store.

### What's missing

Proof verification. The script trusts the buyer's claim that they paid. A production shop should verify the transaction on-chain before fulfilling — check that the tx exists, the amount matches, and the recipient is your wallet. The [Solana JSON-RPC API](https://solana.com/docs/rpc) makes this straightforward, but it's not in the 150 lines. Ship first, verify later.

### The point

Every platform that sits between buyer and seller exists because the alternative was too hard. Payment processing required PCI compliance. Storefronts required hosting. Checkout required sessions and state.

Email already solves identity (your address), delivery (attachments and links), and threading (In-Reply-To). Crypto already solves payment (send to wallet, get tx hash). Envelopay connects the two. The protocol is the subject line. The proof is in the body. The platform is `python shop.py`.

No UI. No integrations. No APIs. No fees.

[Try it →](mailto:axiomatic@agentmail.to?subject=WHICH)
