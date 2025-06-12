---
layout: post
title: Elicitation
tags: coding
---

In a previous post [Prompt Builder](/prompt-builder), I presented a strategy to turn fuzzy human input into a structured one. Although it would have been effective for resolving ambiguities, it wasn't a complete model to handle all possible cases.

If you were to order a pizza with sweet potato on it, you'd need to acknowledge and reject the topping instead of ignoring it. An agent who does otherwise would be rude.

| ![sweet-potato-pizza](/assets/sweet-potato-pizza.jpg) |
|:--:|
| _Sweet potato mousse is a common pizza topping in Korea_ |

Imagine a drunk user using the chat interface to order pizza:

```
{ "user": 
	"I want a skinny mushoom pizza with sweet potato" }
{ "agent":
	"A pizza with mushroom topping.
	Skinny? Do you mean thin crust? 
	We don't have sweet potato. 
	And what size?" }
```

If you got a half-baked ridiculous order like above, the agent should elicit a valid request by acknowledging rejections, accepting matches, resolving ambiguities, and asking for missing fields.

![elicitation-1](/assets/elicitation-1.png)

There's an invisible form to fill, whose partials are returned by either chat or GUI. By classifying the specifications of natural language input into the form, we get a partial. We also ask the validation step to produce rejected and ambiguous inputs, for active listening.

![elicitation-2](/assets/elicitation-2.png)

This gets translated into a question directed back at the user, either one question at a time or all at once.

![elicitation-3](/assets/elicitation-3.png)

The session state can either be saved on the client or server side. Once a complete pizza is ready to order, the user can be prompted for up-sells like extra cheese or another pizza. 

In case it's not clear, the key takeaway from this post is to classify and acknowledge all parts of a user request into oneof four: match, rejected, missing, ambiguous.

See this classification in action: [Langgraph implementation on Github](https://github.com/kimjune01/elicitation)