//
//  Networking.swift
//  AU-SEC
//
//  Created by Haven Barnes on 10/21/17.
//  Copyright © 2017 Haven Barnes. All rights reserved.
//

import Foundation
import UserNotifications

enum NotificationTopic: String {
    case notify = "notify"
    case authorize = "authorize"
    
    var string: String {
        return self.rawValue
    }
}

enum NotificationAction: String {
    case authorize = "authorize"
    case deny = "deny"
    var string: String {
        return self.rawValue
    }
}

class NotificationManager {
    
    static let shared = NotificationManager()
        
    func setNotificationCategories() {
        let authorizeAction = UNNotificationAction(identifier: NotificationAction.authorize.string, title: "Authorize", options: [])
        
        let denyAction = UNNotificationAction(identifier: NotificationAction.deny.string, title: "Deny", options: [.destructive])
        
        let authCategory = UNNotificationCategory(
                                    identifier: NotificationTopic.authorize.string,
                                    actions: [authorizeAction, denyAction],
                                    intentIdentifiers: [],
                                    options: [])
        
        let notifyCategory =  UNNotificationCategory(
            identifier: NotificationTopic.notify.string,
            actions: [],
            intentIdentifiers: [],
            options: [])
        
        UNUserNotificationCenter.current().setNotificationCategories([authCategory, notifyCategory])
    }
    
    func sendAuthorizationResponse(_ response: Bool, id: String) {
        
    }
}
