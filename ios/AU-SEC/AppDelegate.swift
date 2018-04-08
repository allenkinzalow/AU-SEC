//
//  AppDelegate.swift
//  AU-SEC
//
//  Created by Haven Barnes on 10/20/17.
//  Copyright © 2017 Haven Barnes. All rights reserved.
//

import UIKit
import UserNotifications

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate, UNUserNotificationCenterDelegate  {
    
    var window: UIWindow?
    
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplicationLaunchOptionsKey: Any]?) -> Bool {
        
        UNUserNotificationCenter.current().delegate = self
        NotificationManager.shared.setNotificationCategories()
        
        UNUserNotificationCenter.current().delegate = self
        let authOptions: UNAuthorizationOptions = [.alert, .badge, .sound]
        UNUserNotificationCenter.current().requestAuthorization(
            options: authOptions,
            completionHandler: {_, _ in })
        application.registerForRemoteNotifications()
        
        return true
    }
    
    func userNotificationCenter(_ center: UNUserNotificationCenter, willPresent notification: UNNotification, withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void) {
        
        
        
        completionHandler([.alert, .sound])
    }
    
    func userNotificationCenter(_ center: UNUserNotificationCenter,
                                didReceive response: UNNotificationResponse,
                                withCompletionHandler completionHandler: @escaping () -> Void) {
        
        switch response.actionIdentifier {
        case NotificationAction.deny.string:
            break
        case NotificationAction.authorize.string:
            print(response.notification.request.content.userInfo)
            if let id  = response.notification.request.content.userInfo["id"] as? String {
                NotificationManager.shared.sendAuthorizationResponse(true, id: id)
            }
        default:
            break
        }
        
        completionHandler()
    }
    
}

