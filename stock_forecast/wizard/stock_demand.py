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

    _name = 'wizard.stock.demand'

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
        '''
        Open the stock history view using the info registered in the wizard
        '''
        ctx = dict(self._context).copy()
        ctx['history_date'] = self.date_to
        tree_view = self.env.ref('stock_forecast.'
                                 'view_stock_demand_history_report_tree')
        return {
            'domain': [('date', '>=', self.date_from),
                       ('date', '<=', self.date_to),
                       ('quantity', '<', 0.0),
                       ('product_id', '=', self.product_id.id),
                       ('location_id', '=', self.location_id.id)],
            'name': _('Stock Demands At Date'),
            'view_type': 'form',
            'views': [(tree_view.id, 'tree')],
            'view_mode': 'tree,graph',
            'res_model': 'stock.history',
            'type': 'ir.actions.act_window',
            'context': ctx,
        }


class StockHistory(models.Model):

    _inherit = 'stock.history'

    @api.multi
    def _get_current_value(self):
        '''
        Set the quantity available at the moment to delivery the product
        '''
        for history in self:
            history._cr.execute('''
                            SELECT sum(quantity)
                            FROM stock_history
                            WHERE product_id={prod} AND
                                date < '{date}'
                            '''.format(prod=history.product_id.id,
                                       date=history.date))
            result = history._cr.fetchall()
            qty = result and result[0][0] or 0.0
            history.quantity_onstock = qty

    quantity_onstock = fields.Float('Quantity Demanded',
                                    compute='_get_current_value',
                                    store=False,
                                    help='Quantity demanded in the move')
