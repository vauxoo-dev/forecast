# -*- coding: utf-8 -*-
############################################################################
#    Module Writen For Odoo, Open Source Management Solution
#
#    Copyright (c) 2011 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#    coded by: Katherine Zaoral <kathy@vauxoo.com>
#    planned by: Nhomar Hernandez <nhomar@vauxoo.com>
############################################################################

{
    "name": "Stock Forecast",
    "version": "8.0.1.0",
    "license": "LGPL-3",
    "author": "Vauxoo",
    "website": "http://www.vauxoo.com/",
    "category": "",
    "depends": [
        "stock_account",
        "forecasting_rules",
    ],
    "data": [
        "views/forecasting_smoothing_techniques_view.xml",
        "views/product_view.xml",
        "wizard/stock_demand_view.xml",
    ],
    "demo": [
        "demo/stock.picking.csv",
        "demo/stock_forecast_demo.xml",
    ],
    "test": [],
    "qweb": [],
    "installable": True,
}
