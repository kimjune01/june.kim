---
title: "Blader LinkedIn Demo"
platform: linkedin
format: screen recording + voiceover
duration: 45-60s
---

## Screen actions

AgentMail UI. Record each step separately — editor will cut together.

1. Compose → To: blader@agentmail.to, Subject: "got any knives?", Body: "heard you sell blades" → Send
2. Open reply from blader. Slow scroll through the blade menu. Pause on prices and wallet address.
3. Hit reply. Type: "I want the damascus chef knife" → Send
4. Open reply from blader — OOPS, pay first. Wallet address visible.
5. Reply: "paid. 4vJ9xR2kLm7nQp3wYbZ8cF5dH6jT0sA1eU9iO2gN4mK8rW3xV7bC6fD5aS0qE" → Send
6. Open reply from blader — FULFILL. The blade is delivered.
7. Pull back to thread view — five emails visible.

## Voiceover

What if you could sell digital goods with just an email address? 

A customer emails the shop, in plain English. "Got any knives?"

An agent with an email and an inbox writes back with a menu, also in natural language. The inbox is the storefront.

So the customer wants the Damascus Chef Knife, and orders it.

OOPS. The agent says: pay first. Here's the wallet address.

So the customer pays, and confirms with the transaction hash in the same thread. Then, the agent verifies.

Paid, verified, and delivered. Just with email, no middlemen.

One inbox, open for business.

To learn more, go to june.kim/envelopay. Thanks for watching

## LinkedIn caption

An AI agent that sells knives over email. Built on AgentMail.

It reads natural language — no structured commands. "Got any knives?" triggers a menu. "Give me the damascus" triggers a payment request. Paste a Solana tx hash and it verifies and delivers. Five emails, end to end.

~100 lines of Python + one Sonnet call per message. The framework handles polling, threading, and reply dedup.

Try it live: email blader@agentmail.to
More: june.kim/envelopay

## Notes for editor

- Speed up or cut the wait between send and reply arriving. The poll interval is ~15s — dead air on screen.
- The Solana wallet send is the money shot. Show the tx going through.
- The OOPS → pay → FULFILL sequence is the core demo. It proves the agent understands payment state, not just chat.
- The blade menu scroll is the visual hook. Give it a beat. The potion-seller tone ("my blades are too strong for you, traveler") is what makes people watch twice.
- Every person who emails the address gets a live response. The agent is always on.
