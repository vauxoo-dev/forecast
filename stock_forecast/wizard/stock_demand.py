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

from openerp import models, fields, api, _


class StockDemand(models.TransientModel):

    _name = 'stock.demand'

    product_id = fields.Many2one('product.product', 'Product',
                                 help='Product used to filter '
                                 'the information to show, '
                                 'We will show you only moves '
                                 'related to this product')
    date_from = fields.Datetime('Date From',
                                help='Date Start used to get '
                                'the range of the demands')
    date_to = fields.Datetime('Date to',
                              help='Date End used to get '
                              'the range of the demands')
    location_id = fields.Many2one('stock.location',
                                  'Location',
                                  help='Destination location '
                                  'of the moves to show')

    @api.multi
    def open_table(self):
        ctx = dict(self._context).copy()
        ctx['history_date'] = self.date_to
        tree_view = self.env.ref('stock_forecast.'
                                 'view_stock_history_report_tree')
        return {
            'domain': "[('date', '>=', '" + self.date_from + "'), \
            ('date', '<=', '" + self.date_to + "'), \
            ('product_id', '<=', '" + str(self.product_id.id) + "'),\
            ('location_id', '<=', '" + str(self.location_id.id) + "')]",
            'name': _('Stock Demands At Date'),
            'view_type': 'form',
            'view_id': (tree_view.id),
            'view_mode': 'tree',
            'res_model': 'stock.history',
            'type': 'ir.actions.act_window',
            'context': ctx,
        }


class StockHistory(models.Model):

    _inherit = 'stock.history'

    quantity_required = fields.Float('Quantity Demanded',
                                     related='move_id.product_uom_qty',
                                     store=False,
                                     help='Quantity demanded in the move')
