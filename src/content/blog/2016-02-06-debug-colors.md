---
variant: post
title: Debug Colors
tags: coding
image: "/assets/debugColors-before.png"
---
Debug all the views!!!

before:
![before](/assets/debugColors-before.png)
after:
![after](/assets/debugColors-after.png)

Usage:

```swift

override func viewDidAppear(animated: Bool) {
  super.viewDidAppear(animated)
  debugColors()
}

```


```swift

func layoutSubviews() {
  super.layoutSubviews()
  debugColors()
}

```


Implementation:


```swift

extension UIView {
  func debugColors() {
    func randomColor() -> UIColor {
      func randomCGFloat() -> CGFloat {
        return CGFloat(arc4random()) / CGFloat(UInt32.max)
      }
      return UIColor(
        red: randomCGFloat(),
        green: randomCGFloat(),
        blue: randomCGFloat(),
        alpha: 0.7)
    }
    
    for eachSubview in subviews {
      eachSubview.backgroundColor = randomColor()
      eachSubview.debugColors()
    }
  }
}

extension UIViewController {
  func debugColors() {
    view.debugColors()
  }
}

```
