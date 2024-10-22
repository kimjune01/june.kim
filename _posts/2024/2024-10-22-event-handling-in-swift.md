---
layout: post
title: Event handing in Swift
tags: coding
---

Passing events around is at the core of UI development. Understanding how it's changed through the years will help you appreciate how far we've come.

## Indirect Object Ownership

Way back, the standard way to own objects across viewControllers and views was to use `weak` variables. This was before Combine or RX. UIKit users will recognize this pattern:

```swift
class Counter {
	var count: Int
}
class CounterVC: ViewController {
	let counter = Counter()
	let upButtonView = UpButtonView()

	override func viewDidLoad() {
		super.viewDidLoad()
		upButtonView.counter = counter
	}
}
class UpButtonView: View {
	weak var counter: Counter?

	@objc func didPressUpButton() {
		counter?.count += 1
	}
}
```

Alternatively, `weak` delegates to consolidate event handling at the controller level:
```swift
class CounterVC: ViewController {
...
	override func viewDidLoad() {
		...
		upButtonView.delegate = self
	}
}
extension CounterVC: UpButtonViewDelegate {
	func didPressUp() {
		counter.count += 1
	}
}
protocol UpButtonViewDelegate: AnyObject {
	func didPressUp()
}
class UpButtonView: View {
	weak var delegate: UpButtonViewDelegate?

	@objc func didPressUpButton() {
		delegate?.didPressUp()
	}
}
```

This verbose pattern to send events around was explicitly representative of the legacy Objective-C patterns that preceded it. 

## Combine

Combine was a solution to reducee the hard-to-read verbosity of event handling with weak delegates. Objects can now publish and subscribe to events.

```swift
class CounterVC: ViewController {
	let counter = CurrentValueSubject<Int, Never>()
	...

	override func viewDidLoad() {
		...
		upButtonView.counter = counter
		counter.count.sink { ... }
	}
}
class UpButtonView: View {
	weak var counter: CurrentValueSubject<Int, Never>

	@objc func didPressUpButton() {
		counter.send(counter.value + 1)
	}
}
```

## SwiftUI

The latest iteration to work with SwiftUI is using `@Published` `@StateObject` and `@ObservedObject`.

```swift
class Counter {
	@Published var count: Int
}
struct CounterView: View {
	@StateObject var counter = Counter()
	var body: some View {
        VStack {
            Text("Your score is \(progress.score)")
            UpButtonView(counter: counter)
        }
    }

}
struct UpButtonView: View {
	@ObservedObject var counter

 	var body: some View {
		Button("Increase Score") {
		progress.score += 1
		}
	}
}
```

Here, `@ObservedObject` acts as a weak reference, while `@StateObject` expresses its ownership across re-renders. 

The new keywords are syntactic wrappers under the hood, but are now easier to read without leaking too much abstraction. 

----

Inspired in part by [HackingWithSwift's article on @ObservedObject](https://www.hackingwithswift.com/quick-start/swiftui/how-to-use-observedobject-to-manage-state-from-external-objects).








