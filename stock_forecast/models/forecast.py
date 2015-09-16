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

from openerp import models, fields, api


class ForecastingSmoothingTechniques(models.Model):

    _inherit = 'forecast'

    @api.model
    def _default_product(self):
        """Usability feature -

        :return: product.template id.
        """
        product_id = self._context.get('product_tmpl_id', False)
        product = self.env['product.template'].search([(
            'id', '=', product_id)])
        return product

    @api.one
    @api.depends('name', 'product_tmpl_id')
    def _compute_display_name(self):
        """
        Usability feature -

        Check if the name of the product are set in the forecast and used to
        overwrite the display name.

        :return: the forecasting name with the product.template name as prefix.
        """
        name = self.name
        product = self.product_tmpl_id and self.product_tmpl_id.name or False
        if name and product:
            display_name = '{product}: {name}'
        elif name:
            display_name = '{name}'
        elif product:
            display_name = '{product}: No Forecast Name'
        self.display_name = display_name.format(product=product, name=name)

    display_name = fields.Char(
        string='Name', compute='_compute_display_name')

    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Product',
        help='Product related to the current forecasting',
        default=_default_product,
        track_visibility='always')
