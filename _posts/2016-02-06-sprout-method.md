---
layout: post
title: Sprout Method
tags: coding
---


1. Close your eyes and make a wish
2. Write some pseudocode that will grant the wish
3. Turn the pseudocode into method names
4. Run, and watch as the empty method does nothing
5. Stare at the method name and sprout method


Let's try it.

Let's make a screen that tells us whether it's a good time to have ice cream. 

{% highlight swift %}
override func viewDidLoad(animated: Bool) {
  super.viewDidLoad(animated)
  //I wish this viewController told me whether it's a good time to have ice cream...
}
{% endhighlight %}

Writing some pseudocode

{% highlight swift %}
override func viewDidLoad(animated: Bool) {
  super.viewDidLoad(animated)
  //make some views that can tell me about ice cream
  //fetch some data from the ice cream server
  //then fill out the views with that data
}
{% endhighlight %}

Turn the pseudocode into unambiguous method calls

{% highlight swift %}
override func viewDidLoad(animated: Bool) {
  super.viewDidLoad(animated)
  makeSomeViews()
  fetchDataFromIcecreamServer()
  //TODO: then fill out the views with that data
}
{% endhighlight %}

Notice that the methods do not yet exist. Also, we lack the data from the server to grant the third wish. We'll leave that one as psudocode for now. Mark it as a TODO: so that we can quickly search and come back to it later.

{% highlight swift %}
override func viewDidLoad(animated: Bool) {
  super.viewDidLoad(animated)
  makeSomeViews()
  fetchDataFromIcecreamServer()
  //TODO: then fill out the views with that data
}

func makeSomeViews() {
  //TODO:
}

func fetchDataFromIcecreamServer() {
  //TODO:
}

{% endhighlight %}

Now it compiles. Run it for our sanity, so that we can be sure that any code that doesn't compile or run properly is due to the code that we wrote a few seconds ago, not minutes ago.

Now we stare at the method names, and repeat the process.

{% highlight swift %}
func makeSomeViews() {
  //make an ice cream image view in the middle
  //make a question label and put it at the top
  //make an answer label and put it at the bottom
}
{% endhighlight %}

We did not yet introduce any new behavior up to this point. We are simply elaborating the specifications in the right context.

{% highlight swift %}
func makeSomeViews() {
  makeIcecreamImageView() // put it in the middle
  makeQuestionLabel() // put it at the top
  makeAnswerLabel() 	// put it at the bottom
}
{% endhighlight %}
Here we see a common elements. We'll make the method signature common among the two labels. Let's refactor the method names, even before we write the methods.

{% highlight swift %}
func makeSomeViews() {
  makeIcecreamImageView() // put it in the middle
  makeLabel("IS IT A GOOD TIME FOR SOME ICE CREAM???") // put it at the top
  makeLabel("MAYBE") 	// put it at the bottom
}

{% endhighlight %}
Good. Let's make some blank methods with those names and parameters, then fill them in.

{% highlight swift %}
func makeIcecreamImageView() -> UIImageView {
  let image = UIImage(named:"icecream.png")
  let imageView = UIImageView(image:image)
  return imageView
}

func makeLabel(contentString: String) -> UILabel {
  let label = UILabel(text: contentString)
  label.font = UIFont(name: "Helvetica-Neue" size: 14)
  label.textColor = UIColor.blackColor()
  label.sizeToFit()
  return label
} 

{% endhighlight %}

We notice also that there is common behavior among the three view elements.

{% highlight swift %}
func makeSomeViews() {
  put(makeIcecreamImageView() 
    inThe:.Middle of:view)
  put(makeLabel("IS IT A GOOD TIME FOR SOME ICE CREAM???") 
    inThe:.Top of:view)
  put(makeLabel("MAYBE") 
    inThe:.Bottom of:view)
}
{% endhighlight %}

The common behavior is that we have to put the views in various positions of its superview. Meanwhile, refactor the order of these methods to reflect what's actually on screen.

{% highlight swift %}
func makeSomeViews() {
  put(makeLabel("IS IT A GOOD TIME FOR SOME ICE CREAM???") 
    inThe:.Top of:view)
  put(makeIcecreamImageView() 
    inThe:.Middle of:view)
  put(makeLabel("MAYBE") 
    inThe:.Bottom of:view)
}
{% endhighlight %}

Those enums don't exist, either. Let's make some.

{% highlight swift %}
func makeSomeViews() {
  put(makeIcecreamImageView()
    inThe:.Middle of:view)
  put(makeLabel("IS IT A GOOD TIME FOR SOME ICE CREAM???") 
    inThe:.Top of:view)
  put(makeLabel("MAYBE") 
    inThe:.Bottom of:view)
}

enum InsidePosition {
  case Top
  case Middle
  case Bottom
}

func put(subview:UIView, inThe position:InsidePosition, of superview:UIView) {
  var subviewFrame = CGRectZero
  switch position {
    case Top:
    //TODO:
    case Middle:
    //TODO:
    case Bottom:
    //TODO:
  }
  subview.frame = subviewFrame
  superview.addSubview(subview);
}

{% endhighlight %}
To see the actual implementation of put subview in the whichever position of superview, see [put this view over there](/put).

Let's now make the method for the networking.

{% highlight swift %}

func fetchDataFromIcecreamServer() {
  //I wish a server proxy should GET from the server, on whether I should eat ice cream.
  //Upon completion, the views should update to display whether I should eat ice cream.
}

{% endhighlight %}

{% highlight swift %}

func fetchDataFromIcecreamServer() {
  serverProxy.getShouldEatIcecream() {
    shouldEatIcecream:Bool -> Void in
    self.updateViewOnWhetherI(shouldEatIcecream)
  }
}

func updateViewOnWhetherI(shouldEatIcecream: Bool) {
  if shouldEatIceCream {
    //TODO:
  } else {
    //TODO:
  }
}
{% endhighlight %}

serverProxy is a global singleton that does not yet exist. updateViewOnWhetherI(Bool) is empty. To enable its function, those methods need to be filled out. Like a tree, the method keeps on sprouting until the behavior is added completely. 

***

Sprout method encourages human-readable, self-documenting code really easily. Because the code chunks are so short and parameters present themselves naturally, code re-use is natural and little refactoring is required after passing the tests. 

An additional benefit to sprout method for adding behavior is that you become immune to interruptions. By putting //TODO: heads where you're not finished, you can recontextualize really quickly after being interrupted by your boss or coworker. No grand plan survives a lengthy discussion in human memory.


See also: [YAGNI](http://www.wikiwand.com/en/You_aren't_gonna_need_it), [JIT](http://www.wikiwand.com/en/Just-in-time_manufacturing), [self-documenting code](https://www.wikiwand.com/en/Self-documenting_code), [refactoring: good to great](https://www.youtube.com/watch?v=DC-pQPq0acs), [Tell, don't ask](https://robots.thoughtbot.com/tell-dont-ask)

Reference to the name "Sprout Method": [Working Effectively with Legacy Code](/legacy-code) 
