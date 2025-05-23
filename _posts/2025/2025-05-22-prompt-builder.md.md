---
layout: post
title: Prompt Builder
tags: coding
---

<iframe width="560" height="315" src="https://www.youtube.com/embed/VudzO-BPFNE?si=S4p_FUZCHFr6vSJa" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

Forms are everywhere. `POST` is a kind of form, and prompts are a kind of form, too. When you go apply for a loan? Form. Intersect map features? Form. Order pizza? Form. But forms in a GUI can be bad UX. When you have dozens or hundreds to choose from, having a dropdown or a cascading list of options is overwhelming. Psychologically, the paradox of choice can even reduce the perceived value of the outcome. 

![pizza-options](/assets/pizza-options.jpeg)

Most of the time, when ordering pizza, you already have a good idea of what kind of pizza you want. Imagine calling up a pizza shop and and they list every topping option they have — that's not happening. When my wife wants pizza, she always wants the large thin-crust ham and pineapple. Why can't ordering pizza be as simple as saying it? It's one of those times where a chatbot interface is better than a GUI. 

![prompt-builder](/assets/prompt-builder.png)

So suppose that we want a chatbot to help us fill out a form. If we're good at describing what we want, it should be a one-shot operation. But if some parts are missing, it should tell the user. It's a simple requirement but a lot can go wrong, especially with natural language. Just like server-side param validation, we have these requirements for the prompt builder:

- Required fields must be specified
- Default parameters shouldn't need to be specified
- Partial success shouldn't require re-specifying previous fields
- Full success shouldn't need confirmation
- Output should be testable
- Output should be typed appropriately
- Irrelevant inputs should be ignored

The interface for the prompt builder takes in a conversation as input, and outputs an optional response and an optional prompt. The response can then be fed back to the user until an order prompt is filled to completion.

### Architecture

In our example, we achieve this by breaking down the operation into two main parts. The first is to process the input conversation (called demand here) for the presence of pizza orders and ambiguities. If there are any ambiguities in the demand, it is specified explicitly for testing. The second is to map the ambiguities into a coherent message back to the user, that asks to fill in the rest of the order. For example, in the following test case, we have a partial completion that is missing the size field.

```
{
    "messages": [
      {"role": "user", "content": "I want a pizza with thin crust"}
    ],
    "expected": {
      "orders": [
        {"size": null, "crust": "thin", "toppings": ["cheese"], "missing_fields": ["size"]}
      ]
    }
}
```

We could have combined the steps of detecting ambiguities and generating responses for them, but the interception between the two steps gives us a quality gate. That means we can attribute bugs and make changes easier. 

### Testing segue

When I was vibe coding this, I found myself lessons I learned during my Google days: I was making snapshots / goldens!

![snapshot-tests](/assets/snapshot-tests.png)

Normally, snapshot testing would be reserved for products well into the production phase to prevent regressions. But for me, it was the perfect tool to help me realize that I under-specified the test cases and the prompt. When it generated the snapshots, the pizza orders kept coming back as missing the cheese. In my mind, I shouldn't have to specify cheese for a pepperoni pizza. It should be on there by default. 

So I went in the loop, writing test cases, prompting Cursor to write the prompt to fit the test cases, generating goldens based on the responses, fixing the tests, and asking Cursor to update the prompts for me. By the time I was done, I had barely realized that Cursor wrote 90% of the prompt for me, and 50% of the test cases. Once I had a few examples, it could generate so many more. I stopped at 10.

### Generalizing

Ordering pizzas via natural language may be interesting to dozens of engineers that work at Domino's, but it's not much use to everyone else. But I hope that the prompt builder generalizes to any kind of form-filling operation. GUIs still make sense for visual-heavy interactions such as shopping, but test-based interactions such as with lawyers, accountants, bankers; can all benefit from a chatbot interface that doesn't compromise on speed or quality. 





