---
layout: post
title: Menu of View Controllers
tags: coding
---

When requesting a change for a screen, designers or product owners often describe them with ways to navigate to their context. One such reference might be:

> That screen where you tap on the list and the picture shows up before you buy

And then you might say 

> The one for the regular items or the special items?

Then they say

> Wat

Or a change request through the kanban pipeline might look:

> To reproduce this issue, log in as an upgraded user, click on the settings button from the side bar, scroll down to the upgrade button, and remove the upgrade button, and replace the button with a label that tells the upgraded user when their subscription expires. Priority: very important.

And then you finally take those steps specified in the request to get to the screen, you have to pause and type into lldb, using [Live View Debugging](http://www.raywenderlich.com/98356/view-debugging-in-xcode-6) or [chisel](https://github.com/facebook/chisel):

{% highlight swift %}
(lldb) > pvc
{% endhighlight %}

and see which view controller is on screen. Then you finally command+c copy, command+shift+o open file, command+v paste, enter. All that took about one to two minutes to navigate to the issue where we can make the change. Those are two developer minutes, and at $100/hour, cost $2 per issue. That's real money, and we haven't even included the time it took for the change requester to write the issue.

English is great, but it has its limits. What if that time to navigate to the source took five seconds instead? What if there was a way for the change requester to refer to each screen by their view controller class name? And when you are cleaning up code, and look at the giant list of view controllers on the sidebar of Xcode, don't you wish you could just tap on that view controller class with your finger and the screen just pops up?

Now you can. 

![VCMenu](/assets/vcmenu.png)

Just provide a list of ViewControllers you want to see on the menu.

{% highlight swift %}
class VCMenuVC: UITableViewController {
  
  var viewControllersOnTheMenu:[UIViewController]{
    return [
      GrayVC(),
      ClearVC(),
      WhiteVC(),
      YellowVC(fakeObject()),
      GreenVC(fakeObject(), xibName: "GreenVC"),
      FoldoutCollectionVC(collectionViewLayout: RBCollectionViewInfoFolderLayout()),
      CyanVC(),
      
    ]
  }

  //some more code to populate the table view...

}
{% endhighlight %}

Usage:

{% highlight swift %}

func application(application: UIApplication, didFinishLaunchingWithOptions launchOptions: [NSObject: AnyObject]?) -> Bool {
  window = UIWindow(frame: UIScreen.mainScreen().bounds)
  window?.rootViewController = VCMenuWrapperVC()
  window?.makeKeyAndVisible()
  return true
}

{% endhighlight %}


Find the demo on [Github](https://github.com/kimjune01/VCMenuVC)

Copy paste the menu here:

{% highlight swift %}

import UIKit

class VCMenuVC: UITableViewController {
  
  var viewControllersOnTheMenu:[UIViewController]{
    return [
      //TODO: put some view controllers to inspect here
    ]
  }
  
  override func viewDidLoad() {
    super.viewDidLoad()
    addTableView()
    tableView.registerClass(UITableViewCell.self, forCellReuseIdentifier: "UITableViewCell")
  }
  
  func addTableView() {
    tableView.frame = view.bounds
    tableView.backgroundColor = UIColor.lightGrayColor()
  }
  
}

extension VCMenuVC {
  override func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
    if let navVC = navigationController {
      navVC.pushViewController(viewControllersOnTheMenu[indexPath.row], animated: true)
    } else {
      presentViewController(viewControllersOnTheMenu[indexPath.row], animated: true, completion: { () -> Void in
        //
      })
    }
  }
  override func numberOfSectionsInTableView(tableView: UITableView) -> Int { return 1 }
  
  override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int { return viewControllersOnTheMenu.count }
  
  override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
    let cell = tableView.dequeueReusableCellWithIdentifier("UITableViewCell", forIndexPath: indexPath)
    cell.textLabel?.text = viewControllersOnTheMenu[indexPath.row].name()
    return cell
  }
}

extension UIViewController {
  func name() -> String {
    return  NSStringFromClass(self.dynamicType).componentsSeparatedByString(".").last!
  }
}

{% endhighlight %}

If your view controller can only be instantiated from the storyboard, try 

{% highlight swift %}
func viewControllerFromMainStoryboard(vcName name:String) -> UIViewController {
  let storyboard = UIStoryboard(name: "Main", bundle: nil)
  return storyboard.instantiateViewControllerWithIdentifier(name)
}
{% endhighlight %}

If your view controller needs instances of objects from server, try using [fake objects](https://www.wikiwand.com/en/Mock_object) with [Decoupling ViewController](/decoupling-a-viewcontroller)

***

VCMenu is really a mini UI testing suite in disguise. It's most suitable for agile teams who are comfortable with making problems visible. Using multiple ways to instantiate a view controller requires good encapsulation with clean interfaces, and that's not a drawback – it's a benefit. I hope you enjoy the benefits of your designer/QA/product owner reminding you of bugs that are now quicker to fix than to be reported into a bug tracking system. Little nudges towards agility like VCMenu will allow you to say in the retrospective, "Wouldn't it be faster to just tell the dev about the problem instead of writing a ticket?"



