---
layout: post
title: MCP in the Shell
tags: coding
image: "/assets/ghost-hands.webp"
---

![ghost-hands](/assets/ghost-hands.png)

_an allusion to Ghost in the Shell_

In a recent post, I wrote about [Protocol Architecture](/protocol-architecture) where glue code for user-facing applications is no longer necessary to write. Where a bit of latency is acceptable, each user request can be routed to a MCP client for it to use tools to fulfill the user request.

The terminal is making a comeback in 2025. Thousands of services are available as MCP servers, and to reach them, MCP clients can be used. Current implementations of MCP clients serve one user at a time, requiring each user to add the tools for themselves. Some companies tried to make an omni-server that authenticates once and routes everywhere, but that requires the end user to be aware of what MCP is, and to get a client. 

```
 # Option 2: Load server config from file (Claude Desktop format)
    config = MCPGhostConfig(
        server_config="path/to/server_config.json",  # or dict as above
        system_prompt="You are a helpful maps assistant with access to thousands of datasets.",
        provider="openai", 
        api_key="sk-...",
        user_prompt="Show me earthquake-prone buildings near Burnaby, BC, Canada."
    )
    
    result = await mcp_ghost(config)
    print(f"Tool calls made: {len(result.tool_chain)}")
```

By having an MCP client that can be invoked from Python, any layers of abstraction can be added, so that any user anywhere can interface with the tools via the web. That means the user doesn't download anything, just enter natural language and they get their request filled. Even the UI layer can be presented to the client as a tool, so that its parameters can show any template or custom UI for each request.

I'm incredibly excited to see how the MCP trend plays out, and to see applications take on a broader scope of what it means to fulfill a user request.

Link to Github repo: [mcp-ghost](https://github.com/kimjune01/mcp-ghost)

