---
layout: post
title: Reflexivity Code
tags: reflecting
---

Instead of using human language full of metaphors, I wanted to express my thoughts on the reflexivity process in code. I hope its precision would deliver the message more concisely than writing long paragraphs.

States are a reduction of all that we can observe. States can be compared.
```swift
protocol State {
   static func compare(_ left: State, _ right: State) -> Progress
}
```

Goals are a hypothetical state. Results are actual states as observed.
```swift
typealias Goal: State
typealias Result: State
```

Reflexivity is the act of modifying an activity.
```swift
protocol Reflexive {
   func reflex(_ activity: Activity) -> Activity 
}
```

Timeboxes can be used to allocate attention wholly to each phase of the PDCA cycle.
```swift
protocol Timeboxed {
   var phase: Phase
   async func updatePhase()
}
```

An activity is an effort to yield results. Its goal and initial conditions are mutable.
```swift
protocol Activity {
   var goal: Goal
   var start: State
   func act() -> Result
}
```

Scrum is a reflexive timeboxed activity that hosts a core activity. 
```swift
class Scrum: Reflexive, Timeboxed, Activity {
   var coreActivity: Activity

   var previousState: State?
   var currentState: State

   var goal: Goal

   var phase: Phase
   var improvements: [Improvement]

   // Apply improvements and set goals based on progress
   func reflex(_ activity: Activity) -> Activity {
      guard let previousState else { return activity }
      var nextActivity = copy(activity)
      let progress = State.compare(previousState, currentState)
      if let improvement = improvements.pop() {
         nextActivity.state = currentState + improvements.pop()
      }
      nextActivity.goal = currentState + progress
      return nextActivity
   }

   func act() -> Result {
      // Review
      previousState = currentState
      // Planning
      goal = plan(coreActivity)
      // Sprint
      while (phase == .sprint) {
         currentState = coreActivity.act()
      }
      // Retrospective
      coreActivity = reflex(coreActivity)
      return currentState
   }

   async func updatePhase() { ... }
}

```

Thus, it can reflex on itself; and it should. See [Scrumming the Scrum](http://scrumbook.org.datasenter.no/retrospective-pattern-language/scrumming-the-scrum.html)

```swift
class MetaScrum: Reflexive, Activity   {
   var coreActivity: Scrum
   ...
}
````

Mastery is also a reflexive activity, but it fixates on scope instead of time.

```swift
class Mastery: Reflexive, Activity {
   var coreActivity: Activity
   var goal: Goal
   var start: State
   var results: [Result]

   var improvements: [Improvement]

   // Apply improvements if any
   func reflex(_ activity: Activity) -> Activity {
      var nextActivity = copy(activity)
      if let improvement = improvements.pop() {
         nextActivity.start = activity.start + improvements.pop()
      }
      return nextActivity
   }

   // Acquire repeated instances of satisfactory results, however long it takes.
   func act() -> Result {
      while (isSatisfactory(results, goal)) {
         do {
            results.append(coreActivity.act())
            coreActivity = reflex(coreActivity)
         } while (results.last <= coreActivity.goal)
      }
      return results.last
   }
}
```

What does it mean to be a Scrum Master? It means to practice Scrum until repeated satisfactory results have been accumulated on a complex core activity.



