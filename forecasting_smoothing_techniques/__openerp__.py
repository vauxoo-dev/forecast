# -*- coding: utf-8 -*-
############################################################################
#    Module Writen For Odoo, Open Source Management Solution
#
#    Copyright (c) 2011 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#    coded by: Katherine Zaoral <kathy@vauxoo.com>
#    planned by: Nhomar Hernandez <nhomar@vauxoo.com>
#                Gabriela Quilarque <gabriela@vauxoo.com>
############################################################################

{
    "name": "Forecasting by Smoothing Techniques",
    "version": "8.0.1.0.0",
    "author": "Vauxoo",
    "website": "http://www.vauxoo.com/",
    "category": "",
    "depends": [
        "board", # Just because we need some graphic stuff from here
        "product", # may be we need refactor this in a separate module for such dependency.
        "web_widget_x2many_graph",  # To show one2many values as graphs
    ],
    "data": [
        "security/forecasting_smoothing_techniques_security.xml",
        "security/ir.model.access.csv",
        "views/forecasting_smoothing_techniques_view.xml",
        "views/product_view.xml",
    ],
    "demo": [
        "demo/forecasting_smoothing_techniques.xml",
    ],
    "test": [],
    "qweb": [],
    "js": [],
    "css": [],
    "installable": True,
}
