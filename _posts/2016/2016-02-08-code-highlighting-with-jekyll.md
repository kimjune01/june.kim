---
layout: post
title: Code Highlighting in Jekyll
tags: coding
---
Instead of this default:

written with triple backticks

{% highlight swift %}
``` swift
//some code
```
{% endhighlight %}


``` swift
import UIKit

class ClearVC: UIViewController {
  
  override func viewDidLoad() {
    super.viewDidLoad()
    
    let middleView = UIView(width: 100, height: 100)
    middleView.backgroundColor = UIColor.blueColor()
    view.put(middleView,
      inside: view,
      onThe: .BottomLeft,
      withPadding: 10)
    
    let someOtherView = UIView(width: 50, height: 50)
    someOtherView.backgroundColor = UIColor.greenColor()
    view.put(someOtherView,
      atThe: .TopRight,
      of: middleView,
      withSpacing: 20)
    
  }
  
  override func didReceiveMemoryWarning() {
    super.didReceiveMemoryWarning()
    // Dispose of any resources that can be recreated.
  }

}
```


write with liquid tags:

{% highlight swift %}
{% raw %}
{% highlight swift %}
//some code
{% endhighlight %}
{% endraw %}
{% endhighlight %}

and get:

{% highlight swift %}
import UIKit

class ClearVC: UIViewController {
  
  override func viewDidLoad() {
    super.viewDidLoad()
    
    let middleView = UIView(width: 100, height: 100)
    middleView.backgroundColor = UIColor.blueColor()
    view.put(middleView,
      inside: view,
      onThe: .BottomLeft,
      withPadding: 10)
    
    let someOtherView = UIView(width: 50, height: 50)
    someOtherView.backgroundColor = UIColor.greenColor()
    view.put(someOtherView,
      atThe: .TopRight,
      of: middleView,
      withSpacing: 20)
    
  }
  
  override func didReceiveMemoryWarning() {
    super.didReceiveMemoryWarning()
    // Dispose of any resources that can be recreated.
  }

}
{% endhighlight %}


1. Find a highlighting style at [jekyll-pygments-themes](http://jwarby.github.io/jekyll-pygments-themes/languages/javascript.html)
2. Copy-paste into [css-to-scss converter](http://sebastianpontow.de/css2compass/)
3. Copy-paste into /syntax.scss


