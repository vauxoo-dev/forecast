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

from openerp.tests import common
import logging

_logger = logging.getLogger(__name__)


class TestForecasting(common.TransactionCase):

    """
    Test that the forecasting smothing model is working propertly.
    """

    def setUp(self):
        super(TestForecasting, self).setUp()
        self.forecast_obj = self.env['forecasting.smoothing.techniques']

    def compare_res(self, correct, real):
        """
        Compare the correct result with the real result. Print logger with
        error tag.
        """
        for (key, value) in correct.iteritems():
            if real.get(key) != value:
                _logger.error('%s %s != %s', key, real.get(key), value)

    def test_01(self):
        """
        Run 80 values, count for 1 to 30 and repeat.
        """
        values = self.get_test_01_in()
        forecast = self.forecast_obj.create(values)
        out = self.get_test_01_out()
        self.compare_res(out, forecast.read([])[0])

    def get_test_01_in(self):
        """
        config the values for the forecasting model to test.
        """
        data = {}
        val = 1
        for item in range(1, 81):
            fvfield = 'fv_{num:02d}'.format(num=item)
            data.update({fvfield: val})
            if val == 30:
                val = 1
            else:
                val += 1
        return data

    def get_test_01_out(self):
        """
        Return a dictionary with the expected result of the test.
        """
        return dict(
            ma_forecast=14.0,
            ma_ma_error=3.157895,
            wma_forecast=4.666667,
            wma_ma_error=10.684211,
            single_forecast=17.690605,
            single_ma_error=2.881943,
            double_forecast=19.755723,
            double_ma_error=5.155758,
            triple_forecast=19.580177,
            triple_ma_error=6.901317,
            holt_forecast=18.221501,
            holt_ma_error=3.003755
        )

    def test_02(self):
        """
        Run 10 values
        - Only 10 forecast values of the 80 spaces.
        """
        values = self.get_test_02_in()
        forecast = self.forecast_obj.create(values)
        out = self.get_test_02_out()
        self.compare_res(out, forecast.read([])[0])

    def get_test_02_in(self):
        """
        This method will return the forecast input values in a list.
        """
        data = {}
        val = 1
        for item in range(1, 11):
            fvfield = 'fv_{num:02d}'.format(num=item)
            data.update({fvfield: val})
            val += 1
        return data

    def get_test_02_out(self):
        """
        Return a dictionary with the expected result of the test.
        """
        return dict(
            ma_forecast=4.0,
            ma_ma_error=2,
            wma_forecast=1.333333,
            wma_ma_error=5.666667,
            single_forecast=7.760825,
            single_ma_error=1.577526,
            double_forecast=9.481168,
            double_ma_error=2.691897,
            triple_forecast=9.451321,
            triple_ma_error=3.432094,
            holt_forecast=11,
            holt_ma_error=0
        )
