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

from openerp import _
from openerp.exceptions import ValidationError
from openerp.tests import common


class TestForecasting(common.TransactionCase):

    """
    Test that the forecasting smothing model is working propertly.
    """

    maxDiff = None

    def setUp(self):
        super(TestForecasting, self).setUp()
        self.forecast_obj = self.env['forecasting.smoothing.techniques']

    def compare(self, expected, real):
        """
        Compare the correct result with the real result. Print logger with
        error tag.
        """
        elist = list()
        keys = expected.keys()
        keys.sort()
        error_msg = "{key:15} {real:15} != {expected:15} {ca} {diff:15}"
        for key in keys:
            vreal = real.get(key)
            vexpected = expected.get(key)
            vdiff = abs(vreal - float(vexpected))
            allowed_error = 2
            if int(round(vdiff)) > allowed_error:
                elist += [error_msg.format(
                    key=key,
                    real=vreal,
                    expected=vexpected,
                    ca=vexpected < vreal and '>' or '<',
                    diff=vdiff)]

        error_msg = '\n'.join(['\n', _('Fall forecast calculation ')] + elist)
        self.assertTrue(elist == [], error_msg)

    def test_00(self):
        """ Test CRUD, Check models constrains and empty fields """
        # TODO: integrete test with users groups (secutiry)

        # Test Create
        forecast = self.forecast_obj.create({})

        # Test Read + Check defaults values
        defaults = {
            'period': 5, 'exp_alpha': 0.3, 'holt_alpha': 0.3,
            'beta': 0.03, 'holt_period': 1,
        }
        self.compare(defaults, forecast.read(defaults.keys())[0])

        # Test Write
        forecast.period = 3

        # Test Duplicate
        forecast2 = forecast.copy()
        self.compare(defaults, forecast2.read(defaults.keys())[0])

        # Test Contraints
        for item in [1, 0, -2]:
            with self.assertRaisesRegexp(
                    ValidationError,
                    "Period must be an integer greater than 1."):
                forecast.period = item

        for item in [0, 1, 2, -2]:
            with self.assertRaisesRegexp(
                    ValidationError, 'Alpha should be between 0 and 1.'):
                forecast.exp_alpha = item

        for item in [0, 1, 2, -2]:
            with self.assertRaisesRegexp(
                    ValidationError, 'Beta should be between 0 and 1.'):
                forecast.beta = item

        for item in [0, 1, 2, -2]:
            with self.assertRaisesRegexp(
                    ValidationError, 'Alpha should be between 0 and 1.'):
                forecast.holt_alpha = item

        # Check that forecasting = 0.0 when data is 0.0
        fv_list = forecast.get_forecasting_values()
        self.assertFalse(any(fv_list), 'Must be blank')
        keys = [
            'sma_forecast',
            'sma_ma_error',
            'cma_forecast',
            'cma_ma_error',
            'wma_forecast',
            'wma_ma_error',
            'single_forecast',
            'single_ma_error',
            'double_forecast',
            'double_ma_error',
            'triple_forecast',
            'triple_ma_error',
            'holt_forecast',
            'holt_ma_error',
        ]
        out = {}.fromkeys(keys, 0.0)
        self.compare(out, forecast.read(keys)[0])

    def test_00_1(self):
        """ Check Clear method/button works propertly """
        sections = ['data']
        for section in sections:
            forecast0 = self.forecast_obj.browse(self.ref(
                'forecasting_smoothing_techniques.fst_demo_01'))
            forecast = forecast0.copy()
            self._clear_section_test(forecast, section)

    def _clear_section_test(self, forecast, dtype):
        """ Clear a specific section onyl clear the section """
        # Prepare compare dictionaries
        field_to_clear = forecast.fields_section(dtype)
        forecast_full = forecast.read(field_to_clear)[0]
        forecast_clean = forecast_full.copy()
        forecast_clean.update({}.fromkeys(field_to_clear, 0.0))

        # Clear section and check that result is the expected
        forecast.with_context(dtype=dtype).clear()
        forecast_res = forecast.read(field_to_clear)[0]
        self.compare(forecast_clean, forecast_res)

    def test_01(self):
        """
        Run 80 values, count for 1 to 30 and repeat.
        """
        forecast = self.forecast_obj.browse(self.ref(
            'forecasting_smoothing_techniques.fst_demo_01'))
        out = self.get_test_01_out()
        self.compare(out, forecast.read(out.keys())[0])

    def get_test_01_out(self):
        """
        Return a dictionary with the expected result of the test.
        """
        return dict(
            cma_forecast=18.0, cma_ma_error=3.15,
            sma_forecast=17.0, sma_ma_error=4.6,
            wma_forecast=18.666667, wma_ma_error=2.10,
            single_forecast=17.690605, single_ma_error=2.881943,
            double_forecast=19.755723, double_ma_error=5.155758,
            triple_forecast=19.580177, triple_ma_error=6.901317,
            holt_forecast=18.221501, holt_ma_error=3.003755
        )

    def test_02(self):
        """ All Table with 10 values """
        forecast = self.forecast_obj.browse(self.ref(
            'forecasting_smoothing_techniques.fst_demo_02'))
        out = self.get_test_02_out()
        self.compare(out, forecast.read(out.keys())[0])

    def get_test_02_out(self):
        """
        Return a dictionary with the expected result of the test.
        """
        return dict(
            sma_forecast=7.0, sma_ma_error=3.0,
            cma_forecast=8.0, cma_ma_error=2.0,
            wma_forecast=8.66666, wma_ma_error=1.33,
            single_forecast=7.760825, single_ma_error=1.577526,
            double_forecast=9.481168, double_ma_error=2.691897,
            triple_forecast=9.451321, triple_ma_error=3.432094,
            holt_forecast=11, holt_ma_error=0
        )

    def _test_03(self, period):
        """ base for various periods """
        forecast = self.forecast_obj.browse(self.ref(
            'forecasting_smoothing_techniques.fst_demo_03'))
        forecast.write({'holt_period': period})
        out = self.get_test_03_out(period)
        self.compare(out, forecast.read(out.keys())[0])

    def test_03_1(self):
        """ holt(k=1) for 11 values """
        self._test_03(1)

    def test_03_2(self):
        """ holt(k=2) for 11 values """
        self._test_03(2)

    def test_03_3(self):
        """ holt(k=3) for 11 values """
        self._test_03(3)

    def test_03_4(self):
        """ holt(k=4) for 11 values """
        self._test_03(4)

    def get_test_03_out(self, period=1):
        """
        Return a list with the result values.
        """
        out = dict()
        if period == 1:
            out = dict(
                holt_period=1, holt_forecast=359.70, holt_ma_error=17.67,
                sma_forecast=292.60, sma_ma_error=76.4,
                cma_forecast=315.00, cma_ma_error=48.2,
            )
        elif period == 2:
            out = dict(
                holt_period=2, holt_forecast=372.6,
            )
        elif period == 3:
            out = dict(
                holt_period=3, holt_forecast=385.4,
            )
        elif period == 4:
            out = dict(
                holt_period=4, holt_forecast=398.3,
            )
        else:
            raise Exception(
                _('There is not output for the enter count of periods'))
        return out

    def test_04(self):
        """ SMA(5) and WMA(5) in 12 integer values """
        forecast = self.forecast_obj.browse(self.ref(
            'forecasting_smoothing_techniques.fst_demo_04'))
        out = self.get_test_04_out()
        self.compare(out, forecast.read(out.keys())[0])

    def get_test_04_out(self):
        """
        Return a dictionary with the expected result of the test.
        """
        return dict(
            sma_forecast=117.00, sma_ma_error=10.42,
            cma_forecast=120.00, cma_ma_error=6.37,
            wma_forecast=120.33, wma_ma_error=4.37,
        )

    def test_05(self):
        """ SMA(3) in 12 integer values """
        forecast = self.forecast_obj.browse(self.ref(
            'forecasting_smoothing_techniques.fst_demo_05'))
        self.assertEqual(forecast.period, 3)
        out = self.get_test_05_out()
        self.compare(out, forecast.read(out.keys())[0])

    def get_test_05_out(self):
        """
        Return a dictionary with the expected result of the test.
        """
        return dict(
            sma_forecast=101.66, sma_ma_error=14.07,
            cma_forecast=118.33, cma_ma_error=7.9,
        )
