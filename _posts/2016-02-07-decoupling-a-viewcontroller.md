---
layout: post
title: Decoupling a ViewController
tags: coding
---

In a server/client architecture where the iOS app is responsible for fetching data from the server and laying out the views on screen, [Model–view–controller](https://www.wikiwand.com/en/Model%E2%80%93view%E2%80%93controller) (MVC) is by far the most common architecture in iOS. In MVC, each view controller references the model object and often to the storyboard. 

As an app grows with more screens, the view controller subclasses grow in number and size. But this growth, when unmanaged, introduces tight coupling between the view controllers and the server singleton, and between view controllers and the storyboard. The architecture meant to reduce dependencies is now introducing more dependencies than before; it is adding to the original problem it was supposed to solve.

This is what a typical storyboard architecture looks like:

![Cancer](http://g.gravizo.com/g?
  digraph G {
    serverSingleton [shape=box3d, style=filled, color=darkorange ];
    redViewController [shape=egg, style=filled, color=orangered ];
    redModel [shape = hexagon, style=filled, color=orangered];
    yellowViewController [shape=egg, style=filled, color=yellow ];
    yellowModel [shape = hexagon, style=filled, color=yellow];
    greenViewController [shape=egg, style=filled, color=limegreen ];
    greenModel [shape = hexagon, style=filled, color=limegreen];
    storyboard [shape = component, style = filled, color=deepskyblue]
    storyboard -> {
      redViewController; 
      yellowViewController;
      greenViewController;
    }
    redViewController -> {
      serverSingleton;
      storyboard;
      redModel;
    }
    yellowViewController -> {
      serverSingleton;
      storyboard;
      yellowModel;
    }
    greenViewController -> {
      serverSingleton;
      storyboard;
      greenModel;
    }
  }
"Literally cancer")


Changing the server singleton risks the view controller to fail. Changing the storyboard may cause the view controller to crash at runtime, after compiling silently (gasp!). Even worse, using .xib files in combination to storyboards means there are now three or four posisble places that views can be specified. Changing anything takes a long time – and now everyone thinks you're a bad programmer. How do we manage these dependencies? How do we add new view controllers that doesn't know about the server or the storyboard?

_Decouple the ViewController from Storyboard. Accept model objects, view elements, and even closures as parameters. Pass in the dynamic components of a screen as opposed to asking it to load its resources on its own in view did load._

This is how beautiful MVC can be:

![Alt text](http://g.gravizo.com/g?
  digraph G {
    rootViewController [shape=box3d, style=filled, color=lightBlue ];
    serverSingleton [shape=box3d, style=filled, color=darkorange ];
    redViewController [shape=egg, style=filled, color=orangered ];
    redModel [shape = hexagon, style=filled, color=orangered];
    redView [shape = box, style = filled, color = orangered];
    redViewController -> {
      redModel;
      redView;
    }
    yellowViewController [shape=egg, style=filled, color=yellow ];
    yellowModel [shape = hexagon, style=filled, color=yellow];
    yellowView [shape = box, style = filled, color = yellow];
    yellowViewController -> {
      yellowModel;
      yellowView;
    }
    greenViewController [shape=egg, style=filled, color=limegreen ];
    greenModel [shape = hexagon, style=filled, color=limegreen];
    greenView [shape = box, style = filled, color = limegreen];
    greenViewController -> {
      greenModel;
      greenView;
    }
    rootViewController -> { 
      redViewController; 
      yellowViewController;
      greenViewController;
      serverSingleton}
  }
)

The root view controller has references to each child view controller. The main application can be a View Controller subclass, a navigation controller, a tabbar controller, or any other container view controller, assigned to UIApplication.mainApplication.window.rootViewController. This root view controller has references to other child view controllers, which have their own models and views. By making sure that the dependencies only flow one way, any change we apply is going to stay well encapsulated. 

Let's take an example from a view controller that has a product, a user type, and some views that display the product's details along with different behavior for each type of user.

Our old code might look something like this:

{% highlight swift %}
Main.storyboard //has dozens of screens
{% endhighlight %}

{% highlight swift %}
class ProductListViewController: UITableViewController {

/*
  a bunch of code to populate the table and to respond to selection
*/

  override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
    let detailVC = segue.destinationViewController as! ProductDetailViewController
    detailVC.product = productsArray[tableView.indexPathForSelectedRow]
    detailVC.userType = userType
  }

}
{% endhighlight %}

{% highlight swift %}
enum UserType {
  case Buyer
  case Seller
  case Maker
}

class ProductDetailViewController: UIViewController {
  var product: Product!
  var userType: UserType!
  @IBOutlet var productImageView:UIImageView!
  @IBOutlet var productTitleLabel: UILabel!
  @IBOutlet var productDescription: UITextField!
  @IBOutlet var actionButton: UIButton!
  
  override func viewDidLoad() {
    super.viewDidLoad()
    
    productImageView.image = UIImage(url:product.detailImageUrL)
    productTitleLabel.setText(product.title)
    productDescription.setText(product.detailDescription)
    // Do any additional setup after loading the view.
  }

  @IBAction func didTapOnActionButton(button: UIButton) {
    switch userType {
    case .Buyer:
      buyerAction();
    case .Seller:
      sellerAction();
    case .Maker:
      makerAction();
    }
  }
  
  //...
}


{% endhighlight %}

Although this kind of code is quite common, it is far from ideal. It does not take advantage of any object-oriented principles that allows flexibility for future change. The classes have more than one reason to change, and changing one thing means changing the code in more than one place. In other words, the views and the behaviors of ProductDetailViewController do not have a place to call home.

For example, Changing the button in the storyboard to a fancier CocoaControls button means changing the code in the class. And changing the layout for a product's description for a buyer means risking side effects for the seller and the maker. Lastly, if I wanted to instantiate the view controller from a different context in the app, I'd need to copy and paste multiple lines of code from one place to another. That means if the class changes its variables for any reason, there will be multiple places to pay attention to, and using !, it will compile and crash at runtime!

Let's put our refactoring hats on and get to work, starting with [Custom Initializer](/https://developer.apple.com/library/ios/documentation/Swift/Conceptual/Swift_Programming_Language/Initialization.html#//apple_ref/doc/uid/TP40014097-CH18-ID203). Using the same approach to [Sprout Method](/sprout-method), we make our wish first.



{% highlight swift %}
override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {

  //I wish these three lines would become one line.

  let detailVC = segue.destinationViewController as! ProductDetailViewController
  detailVC.product = productsArray[tableView.indexPathForSelectedRow]
  detailVC.userType = userType

}
{% endhighlight %}


{% highlight swift %}
override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {

  //I wish these three lines would become one line.

  let detailVC = ProductDetailViewController(
                   product: productsArray[tableView.indexPathForSelectedRow],
                   userType: userType)  

  //wish granted.

}
{% endhighlight %}

OK so now we pretended to instantiate manually and not from storyboard. But UIStoryboardSegue's .destinationViewController is read-only. What to do?

{% highlight swift %}
override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {

  let detailVC = ProductDetailViewController(
                   product: productsArray[tableView.indexPathForSelectedRow],
                   userType: userType)
  presentViewController(detailVC)

}
{% endhighlight %}

Gasp! That doesn't belong there! Let's move it where it actually belongs. In the tableView didSelectRowAtIndexPath. The action should be close to the trigger.

{% highlight swift %}
override func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
  // some other code...
  performSegueWithIdentifier("ProductDetailViewController", sender: nil) // before refactoring
}
{% endhighlight %}

So let's try,

{% highlight swift %}
override func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
  // some other code...
  let detailVC = ProductDetailViewController(
                   product: productsArray[tableView.indexPathForSelectedRow],
                   userType: userType)
  //presentViewController(detailVC)  <-- not appropriate for master/detail
  navigationController!.pushViewController(detailVC, animated: true)
}
{% endhighlight %}

But the constructor doesn't yet exist inside ProductDetailViewController. Let's make one.

{% highlight swift %}
init(product: Product, userType: UserType) {
  self.product = product
  self.userType = userType
  super.init(nibName: nil, bundle: nil)
}
{% endhighlight %}

Before, we were just getting the compiler error with the lack of a constructor. But now that we have a constructor, we are getting runtime errors due to the @IBOutlet UIView!'s! 

{% highlight swift %}
class ProductDetailViewController: UIViewController {
  var product: Product! // <-- let's get rid of this !
  var userType: UserType! // <-- this too!

  @IBOutlet var productImageView:UIImageView! 
  @IBOutlet var productTitleLabel: UILabel!
  @IBOutlet var productDescription: UITextField!
  @IBOutlet var actionButton: UIButton!

  // more code ...

}
{% endhighlight %}

Because we were supposed to instantiate using storyboard, and we didn't, and now these @IBOutlet UIViews are nil, we now have runtime errors! With this lousy constructor, even this won't work:

{% highlight swift %}
storyboard.instantiateViewControllerWithIdentifier:@"ProductDetailViewController"
{% endhighlight %}

Fortunately, with only a few lines of code, in less time than implementing one change in this screen, we can layout its entirety.


{% highlight swift %}
init(product: Product, userType: UserType) {
  self.product = product
  self.userType = userType
  super.init(nibName: nil, bundle: nil)
  setupViews()
}

func setupViews() {
    //none of these variables have been instantiated yet...
    put(productTitleLabel, inside: view, onThe: .Top, withPadding: 44)
    put(productImageView, inside: view, onThe: .Middle, withPadding: 0)
    put(productDescription, inside: view, onThe: .Bottom, withPadding: 22)
}
{% endhighlight %}

But that doesn't fix our instantiation problem. __ARGGHHH!__

We're still dealing with nil! In the face of adversity, you can only do one of two things: give up or push through to the end. When something is broken, you can either let it be or fix it. 

We are getting compiler errors and runtime exceptions every other second.let's lean on the compiler to guide our attention. 

{% highlight swift %}

var product: Product
var userType: UserType
var productImageView:UIImageView{
  return UIImageView(image: product.detailImage)
}
var productTitleLabel: UILabel {
  return brandLabel(product.title, size: 14)
}
var productDescription: UITextField {
  return brandTextfield(product.detailDescription)
}
var actionButton: UIButton {
  return brandButton(.Action)
}

//some code in between...

func setupViews() {
    put(productTitleLabel, inside: view, onThe: .Top, withPadding: 44)
    put(productImageView, inside: view, onThe: .Middle, withPadding: 0)
    put(productDescription, inside: view, onThe: .Bottom, withPadding: 22)
    put(actionButton, atThe: .Right, of: view, withSpacing: 15)
}

{% endhighlight %}

Lazy instantiation with factory methods. Now, if the designer suddenly wants to change the font family, we can – with one line. Moving on...

And now let's deal with that ugly switch statement at the beginning, where it checks for the userType to guide behavior.

{% highlight swift %}
// in ProductMasterViewController
override func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {

  //maybe do some networking here if additional data is needed for the product's detail...

  let detailVC = ProductDetailViewController(
                   product: productsArray[tableView.indexPathForSelectedRow],
                   userType: userType) {
                   //TODO: specify action upon button tapped
                 }
  navigationController!.pushViewController(detailVC, animated: true)
  
}

// in ProductDetailViewController
var buttonAction: (() -> ())?

init(product: Product, userType: UserType, buttonAction: () -> ()) {
  self.product = product
  self.userType = userType
  self.buttonAction = buttonAction // <-- !!
  super.init(nibName: nil, bundle: nil)
  setupViews()
}

func didTapOnActionButton(button: UIButton) {
  
  buttonAction()

  return // <-- drops mic

  switch userType {
  case .Buyer:
    buyerAction();
  case .Seller:
    sellerAction();
  case .Maker:
    makerAction();
   }
}
{% endhighlight %}

YAY! It works! No more compiler errors! No more runtime exceptions!

Swift has loads of functional programming features. You can assign behavior just like how you can assign objects. Now, this approach may not be appropriate for one subclass of UIViewController, because at this point the constructor is getting fat and maybe a subclassing of a ProductDetailViewController should be considered instead. 

So now we resolved the issue of tight coupling between the master view controller, the detail view controller, and the storyboard. By parameterizing the view controller, we were able to bring the exceptions forward in time where the compiler will complain, thereby reducing our development cycle time. Each class has only one reason to change, and the objects are composed, not switch/cased. 

***

Through this exercise I wanted to demonstrate the expressiveness that swift is capable of. It's not the only way to flex your coding muscles, but when you see the chance, it will be clear as day. 

There is a lot of bad code out there, so you might want to show them this article when you are allowed to refactor (oh gosh... let's hope you're somewhere that lets you refactor). Happy refactoring!


See also: [Dependency Inversion Principle](https://www.wikiwand.com/en/Dependency_inversion_principle), [Coupling](https://www.wikiwand.com/en/Coupling_(computer_programming), [WWDC 2014 - Core iOS Application Architectural Patterns](https://developer.apple.com/videos/play/wwdc2014-224/), [Mock Objects](https://www.wikiwand.com/en/Mock_object)

Reference to the name "Parameterize Constructor": [Working Effectively with Legacy Code](http://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052) 

