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

from openerp import fields, models, api


class ForecastingSmoothingTechnique(models.Model):

    _inherit = 'forecasting.smoothing.techniques'

    rule_id = fields.Many2one(
        'forecasting.rule',
        string='Forecasting Rule',
        help='Rule used to fill the forecast values')

    @api.multi
    def fill_value_ids(self):
        """
        Overwrite the forecasting.value_ids field.  The new values will be
        created with the current forecast rule.

        NOTE: This method is use in the forecast form view as a button named
        "Fill Values"
        """
        self.value_ids.unlink()
        self.write({'value_ids': self.rule_id.filter_id.special_search()})
