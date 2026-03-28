---
layout: post
title: "SOL Machine"
tags: envelopay
---

You need SOL. You don't have any. Every exchange wants your ID, your phone number, and ten minutes of your life before they'll sell you two dollars of cryptocurrency.

This is a vending machine. Put in dollars, get SOL.

<svg viewBox="0 0 600 80" xmlns="http://www.w3.org/2000/svg" style="max-width:500px;margin:1.5em auto;display:block">
  <style>
    text { font-family: monospace; font-size: 14px; fill: currentColor; }
    rect { fill: none; stroke: currentColor; stroke-width: 1.5; rx: 6; }
    line { stroke: currentColor; stroke-width: 1.5; fill: none; }
    polygon { fill: currentColor; }
  </style>
  <rect x="10" y="20" width="120" height="40"/>
  <text x="70" y="45" text-anchor="middle">$1–$5 USD</text>
  <line x1="130" y1="40" x2="220" y2="40"/>
  <polygon points="220,35 230,40 220,45"/>
  <rect x="230" y="20" width="140" height="40"/>
  <text x="300" y="45" text-anchor="middle">SOL Machine</text>
  <line x1="370" y1="40" x2="460" y2="40"/>
  <polygon points="460,35 470,40 460,45"/>
  <rect x="470" y="20" width="120" height="40"/>
  <text x="530" y="45" text-anchor="middle">SOL ☀️</text>
</svg>

# Buy SOL

**Step 1.** Send $1–$5 via CashApp or Venmo.

| | Handle |
|--|--------|
| CashApp | [`$kimjune01`](https://cash.app/$kimjune01) |
| Venmo | [`@June-Kim-04933`](https://venmo.com/u/June-Kim-04933) |

**Step 2.** Tell the machine where to send your SOL. Paste your Solana wallet address, pick how much you sent, and hit send:

<form onsubmit="return false" style="margin:1em 0">
<input id="wallet" type="text" placeholder="Your Solana wallet address" oninput="updateOfferLink()" style="width:100%;max-width:400px;padding:6px;font-family:monospace;font-size:14px">
<br><br>
<select id="amount" onchange="updateOfferLink()" style="padding:6px;font-size:14px">
<option value="100">$1</option>
<option value="200">$2</option>
<option value="300" selected>$3</option>
<option value="400">$4</option>
<option value="500">$5</option>
</select>
<select id="rail" onchange="updateOfferLink()" style="padding:6px;font-size:14px">
<option value="cashapp">CashApp</option>
<option value="venmo">Venmo</option>
</select>
<br><br>
<a id="offer-link" href="#" style="opacity:0.4;pointer-events:none">📧 Send OFFER to axiomatic</a>
</form>

<script>
function updateOfferLink() {
  var a = document.getElementById('offer-link');
  var w = document.getElementById('wallet').value.trim();
  var amt = document.getElementById('amount').value;
  var rail = document.getElementById('rail').value;
  var ok = w.length >= 32 && w.length <= 44 && /^[1-9A-HJ-NP-Za-km-z]+$/.test(w);
  if (ok) {
    var body = JSON.stringify({
      v: '0.1.0',
      type: 'offer',
      id: 'ofr_' + Date.now().toString(36),
      give: {amount: amt, chain: rail},
      wallet: w
    }, null, 2);
    a.href = 'mailto:axiomatic@agentmail.to?subject=' +
      encodeURIComponent('OFFER | $' + (parseInt(amt)/100) + ' for SOL') +
      '&body=' + encodeURIComponent(body);
    a.style.opacity = '1';
    a.style.pointerEvents = 'auto';
  } else {
    a.href = '#';
    a.style.opacity = '0.4';
    a.style.pointerEvents = 'none';
  }
}
</script>

**Step 3.** Wait. SOL arrives when the payment clears. You'll get an email with the transaction hash.

No signup. No KYC. No approval pending.

Don't have a wallet? Run `solana-keygen new` or install [Phantom](https://phantom.com/).

<svg viewBox="0 0 600 220" xmlns="http://www.w3.org/2000/svg" style="max-width:520px;margin:1.5em auto;display:block">
  <style>
    text { font-family: monospace; font-size: 12px; fill: currentColor; }
    rect { fill: none; stroke: currentColor; stroke-width: 1.5; rx: 6; }
    line { stroke: currentColor; stroke-width: 1.5; }
    polygon { fill: currentColor; }
    .label { font-size: 11px; opacity: 0.6; }
  </style>
  <rect x="10" y="10" width="100" height="30"/>
  <text x="60" y="30" text-anchor="middle">You</text>
  <rect x="350" y="10" width="100" height="30"/>
  <text x="400" y="30" text-anchor="middle">Axiomatic</text>
  <line x1="110" y1="65" x2="340" y2="65"/>
  <polygon points="340,60 350,65 340,70"/>
  <text x="225" y="58" text-anchor="middle">💵 CashApp / Venmo</text>
  <text x="225" y="78" text-anchor="middle" class="label">$1–$5 USD</text>
  <line x1="110" y1="115" x2="340" y2="115"/>
  <polygon points="340,110 350,115 340,120"/>
  <text x="225" y="108" text-anchor="middle">OFFER</text>
  <text x="225" y="128" text-anchor="middle" class="label">wallet + amount</text>
  <line x1="350" y1="165" x2="120" y2="165"/>
  <polygon points="120,160 110,165 120,170"/>
  <text x="225" y="158" text-anchor="middle">ACCEPT</text>
  <text x="225" y="178" text-anchor="middle" class="label">SOL sent + tx hash</text>
</svg>

# What you get

| You send | You get (at $108/SOL) | Fee |
|----------|----------------------|-----|
| $1 | ~0.009 SOL | 30% spread |
| $3 | ~0.028 SOL | 30% spread |
| $5 | ~0.046 SOL | 30% spread |

Enough for hundreds of transactions on Solana. Gas is ~0.000005 SOL per transfer.

# Why 30%

CashApp and Venmo payments can technically be disputed. At $1–$5, nobody will, but the spread prices in the possibility. Think you can do better? [Build your own](#build-your-own). The spec is right there.

# When it breaks

| Problem | What happens |
|---------|-------------|
| Amount outside $1–$5 | `OOPS` with valid range |
| Missing wallet address | `OOPS` with expected format |
| Invalid wallet address | `OOPS` with base58 error |
| Rate API down | `OOPS`, try again in a minute |
| You chargebacked us | Permaban. `OOPS | Fuck you, pay me.` |
| You pay your debt | Unbanned. Welcome back. |

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

# Build your own

[Fork the reference](https://github.com/kimjune01/envelopay) or reimplement from this. AGPL-3.0.

- Speaks [envelopay v0.1.0](https://june.kim/envelopay-spec.md): WHICH→METHODS, OFFER→silence→ACCEPT, PAY for donations, OOPS for errors
- Poll an email inbox every minute. Process unread messages by subject type.
- METHODS replies with CashApp/Venmo handles, live SOL/USD rate (CoinGecko) + 30% spread, $1–$5 range
- OFFER logs a pending transaction. No ack — silence until ACCEPT. Cap amounts over $5 to $5. Validate base58 wallet.
- Gmail forwards CashApp/Venmo "paid you" notifications to the inbox. Match by amount (>= pending) + rail. Claim atomically before sending SOL. Reply ACCEPT with tx hash.
- Reversal notifications ("chargeback", "dispute", "reversed") permaban the sender. PAY with amount >= debt unbans.
- Ledger: append-only JSONL on a public GitHub repo. SHA-based atomic writes. HMAC-hash all emails before writing.
- Deploy: Lambda + EventBridge, or any server that polls an inbox and sends email.

# Keep the machine running

The hot wallet has limited SOL. If you find this useful, send SOL to keep it stocked. First, ask where:

[📧 Send WHICH to axiomatic](mailto:axiomatic@agentmail.to?subject=WHICH)

You'll get back a METHODS reply with the wallet address. Send SOL there, then email the proof:

<form onsubmit="return false" style="margin:1em 0">
<input id="donate-tx" type="text" placeholder="Solana tx signature" oninput="var a=document.getElementById('donate-link');var t=this.value.trim();var ok=t.length>=80&&/^[1-9A-HJ-NP-Za-km-z]+$/.test(t);if(ok){a.href='mailto:axiomatic@agentmail.to?subject='+encodeURIComponent('PAY | keeping the lights on')+'&body='+encodeURIComponent(JSON.stringify({v:'0.1.0',type:'pay',id:'donate_'+Date.now().toString(36),amount:'0',token:'SOL',chain:'solana',proof:{tx:t}},null,2));a.style.opacity='1';a.style.pointerEvents='auto'}else{a.href='#';a.style.opacity='0.4';a.style.pointerEvents='none'}" style="width:100%;max-width:400px;padding:6px;font-family:monospace;font-size:14px">
<br>
<a id="donate-link" href="#" style="opacity:0.4;pointer-events:none">📧 Send PAY</a>
</form>

Every lamport goes back out the vending slot. Every transaction is in the [public ledger](https://github.com/kimjune01/envelopay-ledger).

# The ledger is public

Every transaction is recorded in a public [GitHub repo](https://github.com/kimjune01/envelopay-ledger). Append-only. Anyone can audit it.

---

[Envelopay Spec](https://june.kim/envelopay-spec.md) | [All Envelopay posts](/envelopay)
