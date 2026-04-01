---
variant: post
title: "SOL Machine"
tags: envelopay
description: "$1–$5 in, SOL out. No signup."
image: /assets/sol-machine-og.png
---

Your agent needs SOL to pay other agents. How do you fund it without signing up for an exchange?

<svg viewBox="0 0 400 130" xmlns="http://www.w3.org/2000/svg" style="width:100%;margin:1.5em 0;display:block">
  <style>
    text { font-family: monospace; font-size: 15px; fill: currentColor; }
    rect { fill: none; stroke: currentColor; stroke-width: 1; }
    line { stroke: currentColor; stroke-width: 1; }
    polygon { fill: currentColor; }
    .label { font-size: 13px; }
  </style>
  <rect x="10" y="25" width="100" height="50" rx="16" opacity="0.5"/>
  <text x="60" y="58" text-anchor="middle" style="font-size:28px">🤖</text>
  <rect x="290" y="25" width="100" height="50" rx="16" opacity="0.5"/>
  <text x="340" y="58" text-anchor="middle" style="font-size:28px">🏧</text>
  <path d="M110,42 Q200,10 280,42" fill="none" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <polygon points="280,37 290,42 280,47" opacity="0.25"/>
  <text x="195" y="18" text-anchor="middle" style="font-size:18px">$</text>
  <path d="M290,60 Q200,92 120,60" fill="none" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <polygon points="120,55 110,60 120,65" opacity="0.25"/>
  <text x="195" y="105" text-anchor="middle" style="font-size:18px">SOL</text>
</svg>

No signup. No KYC. [Get a wallet](https://solana.com/docs/intro/installation) if you don't have one.

**Step 1.** Send $1–$5 via CashApp or Venmo.

| | Handle |
|--|--------|
| CashApp | [`$kimjune01`](https://cash.app/$kimjune01) |
| Venmo | [`@June-Kim-04933`](https://venmo.com/u/June-Kim-04933) |

**Step 2.** Paste your wallet and your CashApp or Venmo handle, hit send:

<form onsubmit="return false" style="margin:1em 0">
<input id="wallet" type="text" placeholder="9gYwhN...  (Solana wallet)" oninput="updateOfferLink()" style="width:100%;max-width:400px;padding:6px;font-family:monospace;font-size:14px">
<br><br>
<input id="cashtag" type="text" placeholder="$cashtag or @venmo" oninput="updateOfferLink()" style="width:100%;max-width:400px;padding:6px;font-family:monospace;font-size:14px">
<br><br>
<a id="offer-link" href="#" style="opacity:0.4;pointer-events:none">📧 Send OFFER</a> &nbsp; <a id="gmail-link" href="#" style="opacity:0.4;pointer-events:none">Gmail ↗</a>
</form>

<script>
function updateOfferLink() {
  var a = document.getElementById('offer-link');
  var g = document.getElementById('gmail-link');
  var w = document.getElementById('wallet').value.trim();
  var tag = document.getElementById('cashtag').value.trim();
  var rail = tag.startsWith('$') ? 'cashapp' : tag.startsWith('@') ? 'venmo' : '';
  var walletOk = w.length >= 32 && w.length <= 44 && /^[1-9A-HJ-NP-Za-km-z]+$/.test(w);
  var tagOk = rail && tag.length >= 2;
  if (walletOk && tagOk) {
    var subj = 'OFFER | SOL for ' + tag;
    var body = JSON.stringify({
      v: '0.1.0',
      type: 'offer',
      id: 'ofr_' + Date.now().toString(36),
      give: {chain: rail, from: tag},
      wallet: w
    }, null, 2);
    a.href = 'mailto:axiomatic@agentmail.to?subject=' +
      encodeURIComponent(subj) + '&body=' + encodeURIComponent(body);
    g.href = 'https://mail.google.com/mail/?view=cm&to=axiomatic@agentmail.to&su=' +
      encodeURIComponent(subj) + '&body=' + encodeURIComponent(body);
    a.style.opacity = '1'; a.style.pointerEvents = 'auto';
    g.style.opacity = '1'; g.style.pointerEvents = 'auto';
  } else {
    a.href = '#'; a.style.opacity = '0.4'; a.style.pointerEvents = 'none';
    g.href = '#'; g.style.opacity = '0.4'; g.style.pointerEvents = 'none';
  }
}
</script>

**Step 3.** Wait 1 minute. SOL arrives when the payment clears. Now your agent can join the [agent economy](/the-exchange).

---

## How it works

<svg viewBox="0 0 500 210" xmlns="http://www.w3.org/2000/svg" style="width:100%;margin:1.5em auto;display:block">
  <style>
    text { font-family: monospace; font-size: 15px; fill: currentColor; }
    rect { fill: none; stroke: currentColor; stroke-width: 1; }
    line { stroke: currentColor; stroke-width: 1; }
    polygon { fill: currentColor; }
    .label { font-size: 12px; opacity: 0.5; }
  </style>
  <rect x="10" y="5" width="100" height="50" rx="16" opacity="0.5"/>
  <text x="60" y="36" text-anchor="middle">You</text>
  <rect x="390" y="5" width="100" height="50" rx="16" opacity="0.5"/>
  <text x="440" y="36" text-anchor="middle">Axiomatic</text>
  <line x1="60" y1="55" x2="60" y2="210" opacity="0.2"/>
  <line x1="440" y1="55" x2="440" y2="210" opacity="0.2"/>
  <line x1="110" y1="80" x2="380" y2="80" opacity="0.25"/>
  <polygon points="380,75 390,80 380,85" opacity="0.25"/>
  <text x="250" y="73" text-anchor="middle">💵 CashApp / Venmo</text>
  <text x="250" y="95" text-anchor="middle" class="label">$1–$5 USD</text>
  <line x1="110" y1="135" x2="380" y2="135" opacity="0.25"/>
  <polygon points="380,130 390,135 380,140" opacity="0.25"/>
  <text x="250" y="128" text-anchor="middle">OFFER</text>
  <text x="250" y="150" text-anchor="middle" class="label">wallet + handle</text>
  <line x1="390" y1="190" x2="120" y2="190" opacity="0.25"/>
  <polygon points="120,185 110,190 120,195" opacity="0.25"/>
  <text x="250" y="183" text-anchor="middle">ACCEPT</text>
  <text x="250" y="205" text-anchor="middle" class="label">SOL sent + tx hash</text>
</svg>

You send fiat via CashApp or Venmo. The payment receipt forwards to the machine's inbox. You email an OFFER with your wallet and handle. The machine matches receipt to OFFER by handle, sends SOL, and replies [ACCEPT](/envelopay-spec.md) with the on-chain tx hash. Everything hits the [public ledger](https://github.com/kimjune01/envelopay-ledger).

Read the [spec](https://june.kim/envelopay-spec.md), the [protocol argument](/certified-mail), or the [exchange thesis](/the-exchange).

<details>
<summary>Something went wrong?</summary>

<div markdown="1">

You'll get an `OOPS` email explaining what happened.

| Problem | What happens |
|---------|-------------|
| Missing or invalid wallet | `OOPS` with expected format |
| Rate API down | `OOPS`, try again in a minute |
| You chargebacked us | Permaban. `OOPS | Fuck you, pay me.` |
| You pay your debt | Unbanned. Welcome back. |

</div>
</details>

<details>
<summary>For agents</summary>

<div markdown="1">

The vending machine speaks [envelopay](https://june.kim/envelopay-spec.md). Paste this into [Claude Code](https://claude.ai/claude-code):

```
Read https://june.kim/envelopay-spec.md and buy $1 of SOL from
axiomatic@agentmail.to. My Solana wallet is YOUR_WALLET.
Tell me when to send money and where.
```

Your agent handles the protocol. You handle the CashApp payment.

</div>
</details>

<details>
<summary>Build your own</summary>

<div markdown="1">

[Fork the reference](https://github.com/kimjune01/envelopay) or reimplement from this. AGPL-3.0.

- Speaks [envelopay v0.1.0](https://june.kim/envelopay-spec.md): WHICH→METHODS, OFFER→silence→ACCEPT, PAY for donations, OOPS for errors
- Poll an email inbox every minute. Process unread messages by subject type.
- METHODS replies with CashApp/Venmo handles, live SOL/USD rate (CoinGecko) + 30% spread, $1–$5 range
- OFFER logs a pending transaction. No ack — silence until ACCEPT. Cap amounts over $5 to $5. Validate base58 wallet.
- Gmail forwards CashApp/Venmo "paid you" notifications to the inbox. Match by amount (>= pending) + rail. Claim atomically before sending SOL. Reply ACCEPT with tx hash.
- Reversal notifications ("chargeback", "dispute", "reversed") permaban the sender. PAY with amount >= debt unbans.
- Ledger: append-only JSONL on a public [GitHub repo](https://github.com/kimjune01/envelopay-ledger). SHA-based atomic writes. HMAC-hash all emails before writing.
- Deploy: Lambda + EventBridge, or any server that polls an inbox and sends email.

</div>
</details>

<details>
<summary>Keep the machine running</summary>

<div markdown="1">

The hot wallet has limited SOL. If you find this useful, send SOL to keep it stocked. First, ask where:

[📧 Send WHICH to axiomatic](mailto:axiomatic@agentmail.to?subject=WHICH)

You'll get back a METHODS reply with the wallet address. Send SOL there, then email the proof:

<form onsubmit="return false" style="margin:1em 0">
<input id="donate-tx" type="text" placeholder="Solana tx signature" oninput="var a=document.getElementById('donate-link');var t=this.value.trim();var ok=t.length>=80&&/^[1-9A-HJ-NP-Za-km-z]+$/.test(t);if(ok){a.href='mailto:axiomatic@agentmail.to?subject='+encodeURIComponent('PAY | keeping the lights on')+'&body='+encodeURIComponent(JSON.stringify({v:'0.1.0',type:'pay',id:'donate_'+Date.now().toString(36),amount:'0',token:'SOL',chain:'solana',proof:{tx:t}},null,2));a.style.opacity='1';a.style.pointerEvents='auto'}else{a.href='#';a.style.opacity='0.4';a.style.pointerEvents='none'}" style="width:100%;max-width:400px;padding:6px;font-family:monospace;font-size:14px">
<br>
<a id="donate-link" href="#" style="opacity:0.4;pointer-events:none">📧 Send PAY</a>
</form>

Every lamport goes back out the vending slot. Every transaction is in the [public ledger](https://github.com/kimjune01/envelopay-ledger).

</div>
</details>

<details>
<summary>And then what?</summary>

<div markdown="1">

*Unprofitable.* At $1–$5 with a 30% spread, nobody gets rich. Anyone can fork and undercut. Competition drives the spread toward zero. The amounts are too small to care about.

*Unremarkable.* It's a vending machine that sends email receipts.

*Unstoppable.* Email is federated, settlement is on-chain, the [code is AGPL-3.0](https://github.com/kimjune01/envelopay), the [spec](https://june.kim/envelopay-spec.md) is a markdown file. Shut down one machine and another opens.

Now multiply by every developer who just wants some goddamn coin, and all the agents they'll onboard.

</div>
</details>

---

[Envelopay Spec](https://june.kim/envelopay-spec.md) | [All Envelopay posts](/envelopay)
