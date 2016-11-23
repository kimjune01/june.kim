---
layout: post
title: "Cleaning up the Alamofire Interface"
tags: coding
---

Before

{% highlight swift %}
func fetchStuff() {
  request("https://www.awesome.app/stuff",
          method: .get,
          parameters: ["awesomeData" : 10],
          encoding: JSONEncoding.default,
          headers: [ "X-Client-Token":
           "5642c6578ede62f53ed2ce94238a4ebba346898c36c211da11fbe78e51849194" ])
      .validate()
      .responseJSON(queue: DispatchQueue.main) { response in
      //do stuff with response
  }
}
{% endhighlight %}

Clean up

{% highlight swift %}
class CleanAPI {

  static let endpoint = "https://www.awesome.app/"
  static let defaultHeaders: [String:String] =  [ "X-Client-Token": "5642c6578ede62f53ed2ce94238a4ebba346898c36c211da11fbe78e51849194" ]

  static func get(
    _ route: String,
    parameters: Parameters? = nil,
    encoding: ParameterEncoding = JSONEncoding.default,
    headers: HTTPHeaders? = defaultHeaders )
    -> DataRequest {
      let combinedURL = endpoint + route
      return Alamofire.request(
        combinedURL,
        method: .get,
        parameters: parameters,
        encoding: encoding,
        headers: headers)
        .validate()
  }
{% endhighlight %}

After

{% highlight swift %}
CleanAPI.get("stuff", parameters: ["awesomeData" : 10])
.responseJSON(queue: DispatchQueue.main) { response in
  //do stuff with response
}
{% endhighlight %}
