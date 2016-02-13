---
layout: post
title: Server Singleton
tags: coding
---

In a client-server application, there needs to be a way to communicate effectively between the client application and the server application. Similarly, there also needs to be a way to communicate between the front-end developers and the back-end developers. The client sends and requests data from the server, and the server dutifully serves that data. Similarly, the front-end developers and the back-end developers share information about how that data transfer is to be done. 

Using the REST protocol, there is going to be a back-end that serves JSON from an endpoint that looks like:

{% highlight MATLAB %}
https://staging.server.io/api/v1/some-stuff
{% endhighlight %}

There's a lot going on under the hood. The front-end team is looking at this and dividing it into two or three components, to be able to compose dynamically. The back-end team is making JSON representations of model objects, possibly using [JBuilder](https://github.com/rails/jbuilder). Each JSON representation might have properties such as `imageURL` among `title`, `description`, `price`, `epoch`, etc. 

Then there are view controllers that need to interpret this data into user interfaces. That's us. We are the view controllers. 

## A Communication Problem

If the view controllers call the server using [AFNetworking](http://nshipster.com/afnetworking-2/) or [AlamoFire](http://nshipster.com/alamofire/) directly, the code might look something like this:

{% highlight swift %}

override func viewDidLoad() {
  super.viewDidLoad()
  fetchFromServer()
  layoutViews()
  promptIfNeeded()
}

func fetchFromServer() {
  Alamofire.request(.GET, "https://beverages.io/api/v1/beers",
    parameters: ["range": ["from": 0, "to": 50]],
    encoding: .JSON).responseJSON { response in
      switch response.result {
      case .Success(let JSON):
        let jsonBeers = JSON as! [NSDictionary]
        for eachJsonBeer in jsonBeers {
          let eachBeer = Beer()
          eachBeer.name = eachJsonBeer["name"] as! String
          eachBeer.size = eachJsonBeer["size"] as! Int
          eachBeer.description = eachJsonBeer["description"] as! String
          eachBeer.price = eachJsonBeer["price"] as! Double
          self.beers.append(eachBeer)
        }
      case .Failure(let error):
        self.showErrorMessage(error);
      }
  }
}
{% endhighlight %}

Pew wee! Stinky code! It looks like a [Pyramid of Doom](https://www.wikiwand.com/en/Pyramid_of_doom_(programming))! Newer programmers might ask:

> It works, so let's move on. What's the problem?

Yes, it works for now. But this method has too many reasons to change. This view controller has too many responsibilities. Some of them are:

- choose the starting index of the beers to be shown
- choose the number of beers to be shown
- remember the server API endpoint
- talk to Alamofire
- handle error
- parse JSON
- and all the other user interactions that ViewControllers handle

That means the view controller is going to get really big really fast, and when it comes time to squashing bugs, they become difficult to find. And when the server call changes, the two dozen view controllers that interface with the api may need to change as well. And when it's hard to read, its difficult to change for other developers that come after you, even if you were to remember it six months from now.

External documentation doesn't help much either. Documentation that lists endpoints and examples of their parameters and JSON outputs are non-value-adding activities. And they tend to get outdated faster than the time it takes for you to finish reading it. At that point, you can either ask the API developer to either update the documentation or ask directly about what the key value encoding structure looks like. Then he explains in server-talk gibberish variables, which you have to decode.

What can we do to address these issues? How do we make it super fast to change when change inevitably happens? 

## Refactored Solution

Let's refactor the ugly code shown previously into something that's more modular, better encapsulated, and easier to read. Furthermore, if the code is self-documenting and in sync with the server, then the human latency between the two sides can be shortened, as well. Before we comtinue, you may want to review some of these design patterns, to get a better understanding of what we're doing.

- [Singleton](https://sourcemaking.com/design_patterns/singleton)
- [Decorator](https://sourcemaking.com/design_patterns/decorator)
- [Sprout Method](/sprout-method)
- [Static Method](https://developer.apple.com/library/ios/documentation/Swift/Conceptual/Swift_Programming_Language/Methods.html)
- [Single Responsibility Principle](http://www.oodesign.com/single-responsibility-principle.html)
- [Crash Early](http://principles-wiki.net/principles:Fail%20Fast)

***

Let's get started! First, let's factor out some of the variables from within the function.

### Extract Variable

{% highlight swift %}

func fetchFromServer() {

  let serverURL = "https://beverages.io/api/v1/"
  let beersSuffix = "beers"

  Alamofire.request(.GET, serverURL + beersSuffix,
    parameters: ["range": ["from": 0, "to": 50]],
    encoding: .JSON).responseJSON { response in
      switch response.result {
      case .Success(let JSON):
        let jsonBeers = JSON as! [NSDictionary]
        for eachJsonBeer in jsonBeers {
          let eachBeer = Beer()
          eachBeer.name = eachJsonBeer["name"] as! String
          eachBeer.size = eachJsonBeer["size"] as! Int
          eachBeer.description = eachJsonBeer["description"] as! String
          eachBeer.price = eachJsonBeer["price"] as! Double
          self.beers.append(eachBeer)
        }
      case .Failure(let error):
        self.showErrorMessage(error);
      }
  }
}

{% endhighlight %}

### Rename method 

{% highlight swift %}
override func viewDidLoad() {
  super.viewDidLoad()
  //fetchFromServer()
  getBeersList() // <-- new method name

  layoutViews()
  promptIfNeeded()
}
{% endhighlight %}

I would've been ok with the method name if I hadn't changed it, but I'm feeling uneasy about the new name. It feels like I'm missing something. Aha!

{% highlight swift %}
override func viewDidLoad() {
  super.viewDidLoad()
  layoutViews()
  promptIfNeeded()

  getBeersList() {
    beers in
    self.beers = beers
    self.collectionView.reloadData()
  }

}
{% endhighlight %}

That's what I wanted to do. I want to receive the beers where I ask for them, not buried deep, nested inside a pyramid. Let's make it happen.

### Parameterize method

{% highlight swift %}
func getBeersList(completion: ([Beer] -> ())) {
  let serverURL = "https://beverages.io/api/v1/"
  let beersSuffix = "beers"
  Alamofire.request( ... )
  // ...
}
{% endhighlight %}

I want to continue, but the endpoint is shared across all my API endpoints. And sometimes I need to switch between develop, staging, and production endpoints. We can either make the endpoint a global variable or encapsulate it into a singleton, where we're also allowed to keep behavior without contaminating the global namespace. Let's make a wish.

### Sprout Method

{% highlight swift %}
override func viewDidLoad() {
  super.viewDidLoad()
  layoutViews()
  promptIfNeeded()

  BeverageServer.getBeersList() {
    beers in
    self.beers = beers
    self.collectionView.reloadData()
  }
}
{% endhighlight %}

I like the way it sounds, but there's a compiler error! Let's fix it.

{% highlight swift %}
class BeverageServer {
  class func getBeersList (completion: Beer -> ()) {
    //TODO:
  }
}
{% endhighlight %}

We're getting closer. But before we continue, let's conceptualize what we are trying to do with a diagram:

![MVCS](http://g.gravizo.com/g?
  digraph G {
    graph [fontname="helvetica"]
    node [fontname="helvetica" fontsize=13]
    edge [fontname="helvetica" fontsize=11]
    user [shape=egg style = filled color=deepskyblue]
    ViewController [shape=box style=filled color=goldenrod]
    serverSingleton [shape=component style=filled color=limegreen label="Beverage\nServer"]
    Alamofire [shape = hexagon style=filled color=orange]
    Internet [shape=star style=filled color=gold ]
    user -> ViewController [label="\ \ tap"]
    ViewController -> serverSingleton [label="\ \ getBeersList()"]
    serverSingleton -> Alamofire [label="\ \ request(GET, serverURL)"]
    Alamofire -> Internet [label="\ \ JSON Request"]
  }
"MVCS call out")

The user is accessing the database on the Internet through the user interface. It's starting to look like a kitchen with a menu, as opposed to each customer trying to ask the chef what they want to eat.

![MVCS](http://g.gravizo.com/g?
  digraph G {
    graph [fontname="helvetica"]
    node [fontname="helvetica" fontsize=13]
    edge [fontname="helvetica" fontsize=11]
    user [shape=egg, style = filled, color=deepskyblue]
    ViewController [shape=box, style=filled, color=goldenrod]
    serverSingleton [shape=component, style=filled, color=limegreen label="Beverage\nServer"]
    Alamofire [shape = hexagon, style=filled, color=orange]
    Internet [shape=star, style=filled, color=gold ]
    Internet -> Alamofire [label="\ \ JSON Response"]
    Alamofire -> serverSingleton [label="\ \ response.data"]
    serverSingleton -> ViewController [label="\ \ beers"]
    ViewController -> user [label="\ \ Update View"]
  }[fontName = "Helvetica"]
"MVCS listen in")

The stream of data comes back full circle from the server. Let's continue refactoring.

{% highlight swift %}
class BeverageServer {
  class func getBeersList (completion: Beer -> ()) {
    let serverURL = "https://beverages.io/api/v1/"
    let beersSuffix = "beers"
    
    Alamofire.request(.GET, serverURL + beersSuffix,
      parameters: ["range": ["from": 0, "to": 50]],
      encoding: .JSON).responseJSON { response in
        switch response.result {
        case .Success(let JSON):
          let jsonBeers = JSON as! [NSDictionary]
          for eachJsonBeer in jsonBeers {
            let eachBeer = Beer()
            eachBeer.name = eachJsonBeer["name"] as! String
            eachBeer.size = eachJsonBeer["size"] as! Int
            eachBeer.description = eachJsonBeer["description"] as! String
            eachBeer.price = eachJsonBeer["price"] as! Double
            self.beers.append(eachBeer) //!!
          }
        case .Failure(let error):
          self.showErrorMessage(error); //!!
        }
    }
  }
}
{% endhighlight %}

I copy pasted the code from earlier into the new method body. But there's a compiler error! Referring to an unexisting self is not allowed in a static method. By leaning on the compiler, we can see exactly what we need to work on. The priority of work is arranged for us already.

{% highlight swift %}
var beers = [Beer]()
//..
      beers.append(eachBeer)
    }
    completion(beers)
//..
{% endhighlight %}

How about the failure? How will we handle that? For now, handling failure is not the responsibility of this method. Such a failure in a GET request is most likely a connectivity issue or a server issue, so we route that to where it's appropriate: away.

{% highlight swift %}
//..
  case .Failure(let error):
    BeverageServer.handle(error)
  }
//..

class func handle(error: NSError) {
  //TODO:
  assert(false, error.localizedDescription)
}

{% endhighlight %}

We put a //TODO: tag in the new method, with an assertion message. That will let us know whether the miscommunication is coming from the client side of the server side. Later, when our green path (see [Railway Oriented Programming](http://www.slideshare.net/ScottWlaschin/railway-oriented-programming)) is complete, we can tidy up our red paths. Moving on.

{% highlight swift %}
  static let serverURL = "https://beverages.io/api/v1/"
{% endhighlight %}

static-ifying our serverURL, to be shared among all the other calls in this class.

#### Parameterize method

{% highlight swift %}
class func getBeersList (beginningIndex: Int, endingIndex: Int, completion: [Beer] -> ()) {
//..
    parameters:
          ["range":
            ["from": beginningIndex,
               "to": endingIndex]],
//..
}
{% endhighlight %}

#### Extract method

{% highlight swift %}
switch response.result {
        case .Success(let JSON):
          completion(Beer.listFrom(JSON))
        case .Failure(let error):
          print(error.localizedDescription)
        }
{% endhighlight %}

{% highlight swift %}
class Beer {
//..
  static func listFrom(JSON:AnyObject) -> [Beer] {
    var beers = [Beer]()
    let jsonBeers = JSON as! [NSDictionary]
    for eachJsonBeer in jsonBeers {
      let eachBeer = Beer()
      eachBeer.name = eachJsonBeer["name"] as! String
      eachBeer.size = eachJsonBeer["size"] as! Int
      eachBeer.description = eachJsonBeer["description"] as! String
      eachBeer.price = eachJsonBeer["price"] as! Double
      beers.append(eachBeer)
    }
    return beers
  }
//..
}
{% endhighlight %}

We leave the ! inside during development so that we know where the translation is failing. Also, we keep the JSON parsing as a method to the Beer class because when changing one, the other will change as well. One change corresponds to one class. 

#### Parameterize constructor

{% highlight swift %}
class Beer {
//..
  static func from(JSON:AnyObject) -> [Beer] {
    var beers = [Beer]()
    let jsonBeers = JSON as! [NSDictionary]
    for eachJsonBeer in jsonBeers {
      beers.append(Beer(
                        name: eachJsonBeer["name"] as! String,
                        size: eachJsonBeer["size"] as! Int,
                        description: eachJsonBeer["description"] as! String,
                        price: eachJsonBeer["price"] as! Double))
    }
    return beers
  }
//..
}
{% endhighlight %}

{% highlight swift %}
class Beer {
  let name: String
  let size: Int
  let description: String
  let price: Double
  
  init(name: String, size: Int, description: String, price: Double) {
    self.name = name
    self.size = size
    self.description = description
    self.price = price
  }
//..
}
{% endhighlight %}

It's starting to look closer to JBuilder. Try to see if you can match the variable names to the JSON strings. That way, there will be no confusion between developers when referring to the variables. 

{% highlight ruby %}
json.beers @beers do |beer|
  json.name beer.name
  json.size beer.size
  json.price beer.price
  json.description beer.description
end
{% endhighlight %}

The code is the documentation. It never goes out of date.

Once the code compiles, we run it and see if it behaves as expected. This might be a good time to write a fake beer list using the same constructor, to test some UI. 

***

If you've enjoyed this, you might also enjoy [Refactoring from Good to Great](https://www.youtube.com/watch?v=DC-pQPq0acs). 

