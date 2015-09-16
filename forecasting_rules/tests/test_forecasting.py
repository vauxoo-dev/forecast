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


class TestForecasting(common.TransactionCase):

    """
    Test that the forecasting model values are been fill with the forecasting
    rule propertly.
    """

    def setUp(self):
        super(TestForecasting, self).setUp()

        # Save in test the basic objects
        self.irfilter_obj = self.env['ir.filters']
        self.user_obj = self.env['res.users']
        self.forecast_obj = self.env['forecast']

        # Get the data demo
        self.rule = self.env['forecasting.rule'].browse(self.ref(
            'forecasting_rules.forecast_rule_demo_01'))
        self.rfilter = self.irfilter_obj.browse(self.ref(
            'forecasting_rules.filter_demo_01'))

    def create_forecast(self, name='NOT ESPECIFIED'):
        """
        Create a forecast record with the specified arguments
        By default assing also the forecast rule.

        :name: name of the ir.filter to create

        :return: recordset with the record create
        """
        forecast = self.forecast_obj.create({
            'name': 'Partner Credit Limit Forecast (Test %s)' % name,
            'rule_id': self.rule.id,
        })
        return forecast

    def test_01(self):
        """Forecasting.Rule fill the Forecasting values

        Create a new forecasting and assing an exist forecast rule with the
        demo ir.filter.
        """
        name = '1'
        forecast = self.create_forecast(name=name)
        self.assertTrue(forecast)
        self.assertFalse(forecast.value_ids)
        forecast.fill_value_ids()
        self.assertTrue(forecast.value_ids)

    def test_02(self):
        """forecast_order is an integer field (partner.id)
        """
        forecast = self.forecast_obj.browse(
            self.ref('forecasting_rules.forecast_demo_02'))
        forecast.fill_value_ids()

    def test_03(self):
        """forecast_order is a date field (partner.date)
        """
        forecast = self.forecast_obj.browse(
            self.ref('forecasting_rules.forecast_demo_03'))
        forecast.fill_value_ids()

    def test_04(self):
        """forecast_order is a datetime field (
            partner.last_reconciliation_date)
            write_date
        """
        forecast = self.forecast_obj.browse(
            self.ref('forecasting_rules.forecast_demo_04'))
        forecast.fill_value_ids()

    def test_05(self):
        """ rule filter context containt a group_by for forecast_order
        """
        forecast = self.forecast_obj.browse(
            self.ref('forecasting_rules.forecast_demo_05'))
        forecast.fill_value_ids()
