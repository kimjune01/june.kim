---
layout: post
title: Write logs to file
tags: coding
---

> `> It still doesn't work. Error: ...`

Are you still copy-pasting error messages back to your coding agent? Does Claude Code go in loops, so you check [Anthropic Status](https://status.anthropic.com/) to check if Claude has been lobotomized? I've been there. 

I talked about [closing the loop](/close-the-loop) before, but tests aren't always feasible. For example, checking if a modal shows and closes would take setup and takedown in a simulated environment. And as soon as the simulation requires system permissions or hardware APIs, it becomes much slower to test. A faster way would be to simply `console.log` the success and failure conditions. 

So when the coding agent expresses confidence in its solution when it's verifiably not, it's a huge disappointment. When this happens to me, instead of copy pasting the console, I ask it to write the logs to file, and to read from the logs to verify. 

> `> It still doesn't work. Write the console.log to file instead, and verify yourself. Make sure you have read/write access to the file.`

Then it will go make a logging utility class that writes to a file, run the app again, and when you click the button to trigger the action, you can tell it to check again. 