//
//  JSON+Extensions.swift
//  Funnel
//
//  Created by Jonathan Hart on 4/6/17.
//  Copyright © 2017 Funnel. All rights reserved.
//

import SwiftyJSON

extension JSON {
    public var dateValue: Date {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-MM-dd'T'HH:mm:ss.SSSZ"
        dateFormatter.timeZone = TimeZone(identifier: "UTC")
        guard let date = dateFormatter.date(from: self.stringValue) else {
            return Date()
        }
        return date
    }
}
