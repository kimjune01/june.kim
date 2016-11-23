---
layout: post
title: Coordinators in practice
tags: coding
---

Navigation Coordinator: the superclass

{% highlight swift %}

//
//  NavigationCoordinator.swift
//

import Foundation
import UIKit

protocol NavigationCoordinatorDelegate: class {
  func rootwillAppear(_ root:UIViewController)
  func present(_ vc:UIViewController, onto frame:CGRect)
  func detailViewWillAppear()
  func masterViewWillAppear()
}

class NavigationCoordinator {
  var nav: UINavigationController
  weak var delegate: NavigationCoordinatorDelegate?
  var rootVC: UIViewController { return nav.viewControllers.first! }
  
  init(vc: UIViewController) {
    self.nav = UINavigationController(rootViewController:vc)
  }
  func popToRoot() {
    nav.popToRootViewController(animated: false)
  }
  func push(_ vc: UIViewController) {
    nav.pushViewController(vc, animated: true)
  }
  func hideNavBar() {
    nav.navigationBar.isHidden = true
  }
  func showNavBar() {
    nav.navigationBar.isHidden = false
  }
  func topDistance() -> CGFloat {
    return nav.navigationBar.frame.size.height + UIApplication.shared.statusBarFrame.height
  }
  
}

{% endhighlight %}


Main Coordinator: inherits, and specifies the flow

{% highlight swift %}

protocol MainCoordinatorDelegate: NavigationCoordinatorDelegate {
  func didDismissSettings()
  func settingsButtonTapped()
}

class MainCoordinator: NavigationCoordinator {
  
  override init(vc: UIViewController) {
    let mainVC = vc as! MainVC
    super.init(vc:mainVC)
    mainVC.delegate = self
  }

}

extension MainCoordinator: MainVCDelegate {

  func willAppear() {
    delegate?.rootwillAppear(nav.viewControllers.first!)
    nav.navigationBar.isHidden = false
  }

  func didTapSettingsButton() {
    (delegate as? MainCoordinatorDelegate).settingsButtonTapped()
    let settingsVC = SettingsVC()
    settingsVC.delegate = self
    nav.pushViewController(settingsVC, animated: true)
  }

}  

extension MainCoordinator: SettingsVCDelegate {
  //TODO:
}

{% endhighlight %}

Now MainVC and SettingsVC have no references to each other or to its parent view controllers. Hooray!

[Thanks to Khanlou](http://khanlou.com/2015/10/coordinators-redux/)
[Video](https://vimeo.com/144116310)