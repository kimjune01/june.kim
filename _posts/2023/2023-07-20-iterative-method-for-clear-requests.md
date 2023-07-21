---
layout: post
title: Iterative Method for Clear Requests
tags: coding
---

When asking an engineer to incrementally improve a product, the request will certainly be ambiguous because the product increment does not yet exist. A Product Requirement Document(PRD) or a detailed ticket can be handed off to the engineer, but it leaves room for interpretation.

Where the cost of building the increment can often be 100x the cost to describe it, it's worth taking the time up front to ensure that the engineer fully understands the goal to be achieved. A great job done on the wrong thing is worse than nothing done at all. It's worth the insurance. 

### Requirements?

It's tempting to bloat the spec with increasing amounts of detail to cover your ass and to look good to management. But any work that doesn't contribute to product delivery or its environment is waste. The details will change anyway.

![cat-drawing](/assets/cat-drawing.png)

> Requirements are a communication artifact between the user's needs and the engineer's implementation. Therefore, requirement documents should only be as detailed as is needed to understand what the user needs, and why they need them.

### Trust, but verify

So, what's the best way to ensure that the technical request is received with maximal clarity? It's convention to leave the disambiguation to the receiving senior engineer, but it's irresponsible to leave them with a "Let me know if you have any questions". You may as well be playing [20 questions](https://www.youtube.com/watch?v=-DhYcvp3ZfE). 

Only the sender, not the receiver, can verify whether the received message is valid. The requester should ask the receiver to paraphrase the message in synchronous conversation. 

Here's the algorithm:

``` swift
func send(request: Request, to person: Person) {
  var summary = ""
  while (!isAccurate(summary, request)) {
    let differenceInUnderstanding = request - Request(from: summary)
    say(verbalized(differenceInUnderstanding), to: person)
    summary = askForSummary(of: request, from: person)
  }
  thank(person)
}

```

Describing a product increment with words is a lossy format; you shouldn't expect the receiver to be able to summarize their version of your request the first time. By engaging in conversation, you allow the gaps in their understanding to be filled rapidly. If this was to be communicated async, then its latency would delay the critical chain.

### Handoffs

Handoffs are inevitable because identifying & prioritizing user needs is a different skill set than technical implementation. The ideal would be to eliminate handoffs altogether, but if one is needed, let's make them as unambiguously clear as possible.


See also: [Human TCP](https://www.june.kim/human-tcp)