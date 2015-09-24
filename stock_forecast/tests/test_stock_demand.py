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

from openerp.tests import common


class TestForecastDemand(common.TransactionCase):

    """
    """

    def setUp(self):
        super(TestForecastDemand, self).setUp()
        self.history_obj = self.env['stock.history']
        self.demand_obj = self.env['stock.demand']
        self.move_obj = self.env['stock.move']

    def test_01(self):
        """
        Return the action from the wizard
        """
        move_brw = self.move_obj.search([], limit=1)
        if move_brw:
            # Creating the wizard with the required values
            demand_brw = self.demand_obj.create({
                'product_id': move_brw.product_id.id,
                'location_id': move_brw.location_id.id,
                'date_from': '2015-01-01 00:00:00',
                'date_to': move_brw.create_date,
            })
            action = demand_brw.open_table()
            # Validating the type of the action returned
            self.assertTrue(isinstance(action, dict))
            domain = action.get('domain', [])
            for values in domain:
                # Validating the values in the domain
                if 'date' in values[0]:
                    self.assertTrue(values[2] == move_brw.create_date or
                                    values[2] == '2015-01-01 00:00:00')
                elif 'product' in values[0]:
                    self.assertEqual(values[2], move_brw.product_id.id)
                elif 'product' in values[0]:
                    self.assertEqual(values[2], move_brw.location_id.id)

    def test_02(self):
        """
        Validating that the compute field is computed
        """
        history_brw = self.history_obj.search([], limit=1)
        if history_brw:
            # Validating the new compute field was computed
            self.assertTrue(history_brw.quantity_required >= 0)
