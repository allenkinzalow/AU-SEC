//
//  UIColor+Extensions.swift
//

import Foundation
import UIKit
import CoreGraphics

// Custom Social colors
extension UIColor {
    open class var twitterBlue: UIColor {
        return UIColor(hex: "1DA1F2")
    }
}

extension UIColor {
    
    convenience init(hex: String?) {
        guard let hex = hex else {
            self.init(white: 0.5, alpha: 1)
            return
        }
        
        let hexString = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int = UInt32()
        Scanner(string: hexString).scanHexInt32(&int)
        let a, r, g, b: UInt32
        switch hexString.characters.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }
        self.init(red: CGFloat(r) / 255, green: CGFloat(g) / 255, blue: CGFloat(b) / 255, alpha: CGFloat(a) / 255)
    }

    /**
     Converts a UIColor object to a string with it's hex code representation
     
     
     - parameter color: The input UIColor object representing the desired color
     
     - returns:   String The representation of the color in hexadecimal
     */
    func hex() -> String {
        let hexString = String(format: "%02X%02X%02X",
                               Int((self.cgColor.components?[0])! * 255.0),
                               Int((self.cgColor.components?[1])! * 255.0),
                               Int((self.cgColor.components?[2])! * 255.0))
        return hexString
    }
    
    func lighter(by percentage: CGFloat = 30.0) -> UIColor? {
        return self.adjust(by: abs(percentage) )
    }
    
    func darker(by percentage: CGFloat = 30.0) -> UIColor? {
        return self.adjust(by: -1 * abs(percentage) )
    }
    
    func adjust(by percentage: CGFloat = 30.0) -> UIColor? {
        var r:CGFloat=0, g:CGFloat=0, b:CGFloat=0, a:CGFloat=0;
        if(self.getRed(&r, green: &g, blue: &b, alpha: &a)){
            return UIColor(red: min(r + percentage/100, 1.0),
                           green: min(g + percentage/100, 1.0),
                           blue: min(b + percentage/100, 1.0),
                           alpha: a)
        } else {
            return nil
        }
    }
    
    /**
     Adjusts the hue of the UIColor by the desired value and returns a new UIColor
     
     - Parameter degree: Amount (in degrees) to adjust hue.
     
     - Returns: Color with adjusted hue.
     */
    func adjustHue(by degree: CGFloat) -> UIColor {
        var hue: CGFloat = 0.0, sat: CGFloat = 0.0, brightness: CGFloat = 0.0, alpha: CGFloat = 0.0
        var adjustedHue = degree / 360
        
        self.getHue(&hue, saturation: &sat, brightness: &brightness, alpha: &alpha)
        
        adjustedHue = hue + adjustedHue
        
        if !((0.0..<1.0).contains(adjustedHue)) {
            adjustedHue = abs(1 - abs(adjustedHue))
        }
        
        return UIColor(hue: adjustedHue, saturation: sat, brightness: brightness, alpha: alpha)
    }
    
    /**
     Creates a three color gradient from a single color.
     
     - Parameter bounds: The bounds of the gradent.
     
     - Returns: CAGradientLayer with three colors.
     */
    func gradientFromColor(bounds: CGRect) -> CAGradientLayer {
        let gradient = CAGradientLayer()
        
        let color1 = self.adjustHue(by: 20)
        let color2 = self
        let color3 = self.adjustHue(by: -20)
        gradient.colors = [color1.cgColor, color2.cgColor, color3.cgColor]
        
        gradient.startPoint = CGPoint(x: 0, y: 0.3)
        gradient.endPoint = CGPoint(x: 1, y: 0.8)
        
        gradient.frame = bounds
        
        return gradient
    }
    
    func interpolateColorTo(end: UIColor, fraction: CGFloat) -> UIColor? {
        var f = max(0, fraction)
        f = min(1, fraction)
        
        guard let c1 = self.cgColor.components, let c2 = end.cgColor.components else { return nil }
        
        let r: CGFloat = CGFloat(c1[0] + (c2[0] - c1[0]) * f)
        let g: CGFloat = CGFloat(c1[1] + (c2[1] - c1[1]) * f)
        let b: CGFloat = CGFloat(c1[2] + (c2[2] - c1[2]) * f)
        let a: CGFloat = CGFloat(c1[3] + (c2[3] - c1[3]) * f)
        
        return UIColor(red: r, green: g, blue: b, alpha: a)
    }
}
