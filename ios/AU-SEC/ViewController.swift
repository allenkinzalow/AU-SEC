//
//  InitialViewController.swift
//  AU-SEC
//
//  Created by Haven Barnes on 10/21/17.
//  Copyright © 2017 Haven Barnes. All rights reserved.
//

import UIKit

class InitialViewController: UIViewController {

    @IBOutlet weak var dashboardButton: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        dashboardButton.isHidden = UIDevice.current.userInterfaceIdiom == .phone
    }
}
