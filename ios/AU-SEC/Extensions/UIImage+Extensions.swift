//
//  UIImage+Extensions.swift
//  Funnel
//
//  Created by Haven Barnes on 4/21/17.
//  Copyright © 2017 Funnel. All rights reserved.
//

import UIKit

extension UIImage {
    /// Creates UIImage based off of UIView
    convenience init(view: UIView) {
        UIGraphicsBeginImageContext(view.frame.size)
        view.layer.render(in: UIGraphicsGetCurrentContext()!)
        let image = UIGraphicsGetImageFromCurrentImageContext()
        UIGraphicsEndImageContext()
        self.init(cgImage: image!.cgImage!)
    }
    
    /// Resizes UIImage based on specified CGSize
    func resize(targetSize: CGSize) -> UIImage {
        let size = self.size
        
        let widthRatio  = targetSize.width  / size.width
        let heightRatio = targetSize.height / size.height
        
        var newSize: CGSize
        if(widthRatio > heightRatio) {
            newSize = CGSize(width: size.width * heightRatio, height: size.height * heightRatio)
        } else {
            newSize = CGSize(width: size.width * widthRatio,  height: size.height * widthRatio)
        }
        
        let rect = CGRect(x: 0, y: 0, width: newSize.width, height: newSize.height)
        
        UIGraphicsBeginImageContextWithOptions(newSize, false, 0.0)
        draw(in: rect)
        let newImage = UIGraphicsGetImageFromCurrentImageContext()
        UIGraphicsEndImageContext()
        
        return newImage!
    }
    
    /// Sets a square UIIMage in circle
    func circle() -> UIImage {
        let imageView: UIImageView = UIImageView(image: self)
        var layer: CALayer = CALayer()
        layer = imageView.layer
        
        layer.masksToBounds = true
        layer.cornerRadius = CGFloat(imageView.frame.width / 2)
        
        UIGraphicsBeginImageContextWithOptions(imageView.bounds.size, false, 0.0)
        
        layer.render(in: UIGraphicsGetCurrentContext()!)
        let roundedImage = UIGraphicsGetImageFromCurrentImageContext()
        UIGraphicsEndImageContext()
        
        return roundedImage!
    }
    
    /// Crops a UIImage down to a square (centered)
    func square() -> UIImage {
        let minDimension = size.width < size.height ? size.width : size.height
        let squareSize = CGRect(x: (size.width - minDimension) / 2.0, y: (size.height - minDimension) / 2.0, width: minDimension, height: minDimension)
        
        let imageRef:CGImage = cgImage!.cropping(to: squareSize)!
        return UIImage(cgImage: imageRef)
    }
   
}
