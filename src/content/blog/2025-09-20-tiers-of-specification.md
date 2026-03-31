---
layout: post
title: Tiers of Specification
tags: coding
image: "/assets/spec-tiers.png"
---

> Using AI to code is like using a jackhammer to carve a Michelangelo

When given a small well-defined specification, coding agents are fantastic at generating code. But when it comes to ambiguous requests, or obscure topics, then it struggles to meet our expectations. Amazon's response to this problem is Kiro, a specifications-first approach. However, spec docs assume a divide-and-conquer approach that doesn't fit our mental model of how a feature works. 

Instead of jumping straight into the spec, I propose a gradual approach that offers an equal degree of control with much less tedium.

![spec-tiers](/assets/spec-tiers.png)

On a high level, features can be described from a user's perspective. This is like a PRD(Product Requirements Document) that serves as a goal for the details that follow. Elicitation can be used to fill in gaps for error cases or to generate alternative approaches here.

On a medium level before detailed specification, an architecture doc that describes the data flow between the parts of the system can be written. This is like a Design Doc, outlining the scope and the key components involved. New files and modules can be named here. For common implementations, I like to ask Claude to do some research to recommend the best implementation.

The actual spec can now be written. The details may be described as behaviors (BDD) or tests (TDD). These are easily generated, and be human-approved one section at a time. For a fresh feature, it really helps to specify that it's an MVP, not enterprise-grade.

Once the spec is written, it can turn into a work plan with multiple phases. Nobody likes reviewing huge PRs, so each section should serve as a source for a PR-bite-sized chunk. For example, defining types and mocked interfaces would be a nice PR. 
