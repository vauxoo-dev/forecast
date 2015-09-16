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
from datetime import date
import random


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

        # Get the data demo
        self.rule = self.env['forecasting.rule'].browse(self.ref(
            'forecasting_rules.forecast_rule_demo_01'))
        self.rfilter = self.irfilter_obj.browse(self.ref(
            'forecasting_rules.filter_demo_01'))

        # Modificate a sub group of res.partner with credit_limit 0.0 to a some
        # randomw value to make then count into the forecast values.
        self.prepare_test_data()

    def random_date(self):
        """
        :return: a random date/datetime for the current year
        """
        start_date = date.today().replace(day=1, month=1).toordinal()
        end_date = date.today().toordinal()

        random_day = date.fromordinal(random.randint(start_date, end_date))
        return random_day

    def prepare_test_data(self):
        """Prepare res.partner records to retrive usefull information in the
        forecasting to used in the test

            - Set credit random value > 0.0 for partner without credit limit
            - Set date random date for partners without date.
            - Set random signup_expiration datetime.
        """
        partner_obj = self.env['res.partner']

        # Set credit random value > 0.0 for partner without credit limit
        partners_wo_credit = \
            partner_obj.search([('credit_limit', '=', '0.0')])
        for partner in partners_wo_credit:
            partner.credit_limit = random.randrange(1.0, 15000.0)
        self.assertFalse(
            partners_wo_credit.filtered(
                lambda partner: partner.credit_limit == 0.0))

        # Set date random date for partners without date.
        partners_wo_date = \
            partner_obj.search([('date', '=', False)])
        for partner in partners_wo_date:
            partner.date = self.random_date()
        self.assertFalse(
            partners_wo_date.filtered(lambda partner: not partner.date))

        # Set random signup_expiration datetime.
        # TODO generate random seconds diff
        partners_wo_signup_expiration = \
            partner_obj.search([('signup_expiration', '=', False)])
        for partner in partners_wo_signup_expiration:
            partner.signup_expiration = self.random_date()
        self.assertFalse(partners_wo_signup_expiration.filtered(
            lambda partner: not partner.signup_expiration))

    def create_forecast(self, name='NOT ESPECIFIED'):
        """
        Create a forecast record with the specified arguments
        By default assing also the forecast rule.

        :name: name of the ir.filter to create

        :return: recordset with the record create
        """
        forecast_obj = self.env['forecasting.smoothing.techniques']
        forecast = forecast_obj.create({
            'name': 'Partner Credit Limit Forecast (Test %s)' % name,
            'rule_id': self.rule.id,
        })
        return forecast

    def create_filter(self, name='NOT ESPECIFIED', model_id='res.partner',
                      context='{}', domain='[]', link_rule=True):
        """
        Create a ir filter with the specificated arguments

        :name: name of the ir.filter to create
        :model_id: model name to use in the ir.filter
        :context: context field in the ir.filter record
        :domain: domain field in the ir.filter record
        :link_rule: boolean that tell if you want to link or not the created
                    irfilter to a forecast rule

        :return: recordset with the record create
        """
        irfilter = self.irfilter_obj.create({
            'name': 'All Partner (Test %s)' % name,
            'model_id': model_id,
            'context': context,
            'domain': domain,
        })
        if link_rule:
            self.rule.filter_id = irfilter.id
        return irfilter

    def fill_forecast_values(self, name, context):
        """
        Fill the forecast with the forecast rules
        and check if the values were fill

        :forecast: forecast recordset
        """
        self.create_filter(name=name, context=context)
        forecast = self.create_forecast(name=name)
        self.assertTrue(forecast)
        self.assertFalse(forecast.value_ids)
        forecast.fill_value_ids()
        self.assertTrue(forecast.value_ids)

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
        context = "{'forecast_order': 'id', 'forecast_value': 'credit_limit'}"
        self.fill_forecast_values('2', context)

    def test_03(self):
        """forecast_order is a date field (partner.date)
        """
        context = \
            "{'forecast_order': 'date', 'forecast_value': 'credit_limit'}"
        self.fill_forecast_values('3', context)

    def test_04(self):
        """forecast_order is a datetime field (
            partner.last_reconciliation_date)
            write_date
        """
        context = ("{'forecast_order': 'signup_expiration',"
                   " 'forecast_value': 'credit_limit'}")
        self.fill_forecast_values('4', context)

    def test_05(self):
        """ rule filter context containt a group_by for forecast_order
        """
        context = (
            "{'forecast_order': 'date', 'forecast_value': 'credit_limit',"
            " 'group_by': ['date:month']}")
        self.fill_forecast_values('5', context)
