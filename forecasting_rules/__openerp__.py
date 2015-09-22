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
    "name": "Forecasting Rules",
    "summary": "Manage forecasting data and results",
    "version": "8.0.1.0",
    "license": "LGPL-3",
    "author": "Vauxoo",
    "website": "http://www.vauxoo.com/",
    "category": "",
    "depends": [
        "forecasting_smoothing_techniques",
        ],
    "data": [
        "security/forecasting_rules_security.xml",
        "security/ir.model.access.csv",
        "views/forecasting_rule_view.xml",
        ],
    "demo": [
        "demo/res_partner.xml",
        "demo/forecasting_rules_demo.xml",
        ],
    "test": [],
    "qweb": [],
    "js": [],
    "installable": True,
}
