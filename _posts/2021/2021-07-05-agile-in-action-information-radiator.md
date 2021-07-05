---
layout: post
title: Agile in action – Information Radiator using Notion
tags: reflecting
---


When I was interviewing at startups for work, I had a strict requirement that the work itself had to be interesting. Leaving a megacorp meant that I was likely to take a pay cut, and I wouldn't do it for work that's not challenging. I was looking for growth. When it was time for me to ask the questions in the interview, I was probing into how I could get that growth. For me, I saw growth in two orthogonal directions: technical and organizational. 

The questions I would always ask are: What kind of improvements are you looking to make in your development process? If you could change one thing about the way you worked, what would that be? I could then ask follow-up questions about how long it has been since they addressed their pain. If that pain has been around forever, then it's a signal that they aren't into improvements. If they can't name any potential improvements, it shows stagnation and complacenty, much like a megacorp. 

This one startup that I interviewed was able to take the question beyond answering it, to inquiring about what I would do about it. For context, they were a 3-person development team with an informal co-located process around work planning and synchronization. Throughout the day, they would inquire to each other about the status of their work. Given that they built trust for over a year of working together daily, it was no big deal to ask for when stuff would get done. When I heard this situation, I immediately saw an opportunity for improvement.

Information Radiator is a Scrum pattern ([A Scrum Book](http://scrumbook.org/value-stream/information-radiator.html)) first described by Alistair Cockburn in his Agile book. Its patlet is rather dramatic:

> Without valuable and timely information, the organization dies. Therefore: Collaboratively maintain physical artifacts that keep information visible to all stakeholders.

I presented the idea as an efficiency boost, without going into the details about its potentially profound impact. I said, to paraphrase, "It's called Information Radiator. Instead of having to ping each other all the time about what got done, you can just have a company-wide visible board that anyone can update to show what's going on. If you have an extra screen, it can be on all the time and be dedicated to show what everyone's working on."

To my surprise, they took the suggestion on the spot. Traditionally, an information radiator would be implemented as a part of a kanban board, where an assigned task in Jira or Trello would be dragged from the backlog to WIP to Done. An even more old-school method is to use colored post-its to indicate who's doing what, and at what stage the work unit is at. For a completely co-located team, post-its would work just fine, but some members would be remote. What good is a radiator that can't radiate beyond the room?

Notion is a fantastic collaboration tool. I take it as a spiritual descendent of Google Wave, where real-time synchronization is a first-class use case. From what I've heard of other companies, they use it as an alternative to Google Docs, as a repository of documents to be referred to. But one of many feature that makes it distinct from Google Docs is its ability to show individuals' cursors when many people are focused on the same doc.

> Notion Official > Help & Support > Real-time Collaboration
> ![notion-real-time](/assets/collabTakeOne.gif)

Seeing where individuals are at in real-time gives more life to the doc, turning it into a place, where you can feel your teammates' presence. As my cursor hovers over my daily to-do tasks, the team can confidently trust that the status of my tasks are up-to-date to the minute. There is no asking for "Is this one done? How about that one?". Teams that use post-it notes as their source of truth need to take the fifteen seconds walk to the post-it board. Using Notion, it's an alt-tab away, less than two seconds. 

So what information goes on the information radiator? In our case, the most frequently-asked, and the under-asked. At the daily standup, the sprint goal is broken down, and turned into actionable items that can be checked off a list. This list takes up the bulk of the real estate for each team member. 

![notion-green](/assets/notion-green.png)

It's simply a to-do list that's shared. But the contents are fundamentally social, compared to a private to-do list. I've socially committed myself to complete these tasks in order, to the best of my ability. There is no expectation of punting them to tomorrow.

The under-asked is my visible status, in speed. [Visible Status](https://sites.google.com/a/scrumplop.org/published-patterns/value-stream/visible-status) is another pattern in the task synchronization sequence. 

![notion-red](/assets/notion-red.png)

There is a special feature in notion that allows a section of one document to be sync'd to a section of another. This allows me to copy-paste colors of the traffic light to indicate my speed, while having to persist that state between boards. When I'm cruising along my list, I'll be showing green. When I'm faced with a difficult problem, and potentially digging myself into a rabbit hole, I'm yellow. When I cannot progress any further, or if I'm afk, I'm red.

As pretty as this scheme is, no battle plan survives contact with the enemy. What was expected to happen was for all the commitments to be realistic at the beginning of a sprint, and for all of those checkboxes to be filled by the end of the production episode. There was this one time where I was refactoring my way into a large feature update in the app – and I didn't check off a single box that day.

I was the one who proposed to use this information radiator to organize our work, and here I am supposedly slacking off or being irresponsible, not going with the work plan. At the end of that day, the team confronted me with disappointment that I didn't get any work done at all. They were surprised that I didn't follow through with what was on the info radiator. I was surprised that they were surprised, because I didn't expect them to wait until the end of the day to talk to me about it. If they saw that nothing was getting done, why not intervene sooner?

The conflict was later identified to be a combination of [Granularity Gradient](https://sites.google.com/a/scrumplop.org/published-patterns/value-stream/product-backlog/granularity-gradient) and [Pigs Estimate](https://sites.google.com/a/scrumplop.org/published-patterns/value-stream/estimation-points/pigs-estimate). In English, the tasks were not broken down enough for me to be able to check off bits of it, and that I did not commit to such large tasks to be brought to completion that day. 

After resolving that issue, I realized that if it weren't for the info radiator, the surprise would have been delayed even further, and trust would have eroded. Whose job is it anyway to communicate what proportion of each of the tasks are completed? Not the developer's, obviously; the developer should be developing. Not the manager's; that's equivalent to asking for [TPS reports](https://www.google.com/search?q=tps+report+meme) each day!

The information radiator dynamically changing throughout the day gives information about which tasks are getting done; it not changing gives information about what's not getting done. The lack of update from me signaled that whatever I'm doing is going off the rails, and that it needs a course correction. The radiator radiated. It did its job.






