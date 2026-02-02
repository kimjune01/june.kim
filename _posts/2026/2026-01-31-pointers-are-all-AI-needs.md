---
layout: post
title: Pointers are All AI Needs
tags: coding
---

This weekend, I came to a painful realization that application building for B2B will soon evaporate. If I'm doing error debugging from just the terminal without a GUI, nontechnical Cowork users are soon to follow. Given a choice between a chat interface and a dashboard, new users would rather choose chat. It's what's familiar. No UI is best UI, and chat is as close as we can get, with exception to voice. 

B2B SaaS apps are adding chat-with-your-app features. But users often demand that their data cross app borders in agentic workflows, skipping the manual copy-paste across multiple tabs altogether. So what if instead of chatting with one app, you can chat with _all_ your apps? That's the idea behind [Rube MCP](https://rube.app/). 

![rube-plus-claude](/assets/rube-plus-claude.png)

I admitted defeat for Skillomatic, taking lessons that I can from building a unified MCP/Auth layer with skills. Rube calls them recipes. 

Combined with Claude Cowork or MCP client, it's able to ingest data from your apps, store them in sheets or any datastore of your choosing, and send emails or whatever output you desire. All on the latest SOTA model accessible. This stack can replace expensive SaaS for small businesses with more capability than ever. The only automation feature not provided is cron, which most professionals don't need anyway.

To tap into AI, all you need to do is set up a few services and point them to each other. What is there left to build? 

