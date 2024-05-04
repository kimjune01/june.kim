---
layout: post
title: UIView+
tags: coding
---

Every iOS developer faces the dilemma between programmatic layout and storyboards. This was a common interview question back before SwiftUI came out. But if you're making a UI with custom interactive elements or complex animations, then SwiftUI is not an option. But programmatic layout is so clunky and reminiscent of `Objc`. Why should I have to write

```
NSLayoutConstraint.activate([
  bottomAnchor.constraint(equalTo: guide.bottomAnchor, constant: -margin),
])
```

Can this be turned into one line? See UIView+ in the [Github link](https://github.com/kimjune01/uiview-plus)