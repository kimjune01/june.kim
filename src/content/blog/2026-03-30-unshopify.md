---
variant: post
title: "Unshopify"
date: 2026-03-30
tags: envelopay
---

*Part of the [envelopay](/envelopay) series.*

You want to sell a digital product. A template, a component kit, a prompt library.

Agents want to buy things. They can't fill out checkout forms. They don't have credit cards. The crypto micropayment dream was supposed to fix this, but nobody built the UX. So agents can talk, but they can't shop.

Here's what selling looks like today: sign up for Gumroad. Upload your file. Set a price. Customize your landing page. Connect your bank account. Wait for approval. Share the link. Gumroad takes 8.5%. Your buyer creates an account, enters their card, agrees to terms, and downloads.

An agent can't do any of that. But an agent can send an email.

### What you need

1. A free [AgentMail](https://agentmail.to) inbox
2. A Solana wallet
3. One Python file

No web framework. No database. No Stripe integration. No checkout page. No deploy pipeline. One Python file with zero dependencies beyond the standard library.

### How it works

The [Envelopay protocol](/envelopay-spec) defines nine message types. A shop only needs two:

- **WHICH** — the buyer asks what you accept. You reply with **METHODS**: your wallet, your rail.
- **ORDER** — the buyer sends payment on-chain and emails the proof. You reply with **FULFILL**: a download link.

Here's what the exchange looks like:

```
→ WHICH
← METHODS | Solana, SOL
→ ORDER | React UI Kit, 0.5 SOL
← FULFILL | React UI Kit
```

<details><summary>Full messages</summary>

<pre>
To: shop@agentmail.to
Subject: WHICH
</pre>

<pre>
Subject: METHODS | Solana, SOL
{"rails":[{"chain":"solana","token":"SOL","wallet":"9gYw...pAM"}]}
</pre>

<pre>
To: shop@agentmail.to
Subject: ORDER | React UI Kit, 0.5 SOL
{"type":"order","task":{"description":"React UI Kit"},"proof":{"tx":"3tfT..."}}
</pre>

<pre>
Subject: FULFILL | React UI Kit
{"type":"fulfill","result":{"download":"yoursite.com/download/react-ui-kit.zip"}}
</pre>

</details>

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

Proof verification. The script trusts the buyer's claim that they paid. A production shop should verify the transaction on-chain before fulfilling — check that the tx exists, the amount matches, and the recipient is your wallet. The [Solana JSON-RPC API](https://solana.com/docs/rpc) makes this straightforward, but this is a prototype. Verification is the first thing to add before real money flows through.

### No UI. No integrations. No SDK. No fees.

[Build one →](https://github.com/kimjune01/envelopay/tree/master/shop)
