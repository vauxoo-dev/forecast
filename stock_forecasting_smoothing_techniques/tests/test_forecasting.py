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

    def test_01(self):
        """
        Run 80 values, count for 1 to 30 and repeat.
        """
        values = self.get_test_01_in()
        forecast = self.forecast_obj.create(values)
        forecast.calculate()
        out = self.get_test_01_out()
        self.compare(out, forecast.read(out.keys())[0])

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
        values = self.get_test_02_in()
        forecast = self.forecast_obj.create(values)
        forecast.calculate()
        out = self.get_test_02_out()
        self.compare(out, forecast.read(out.keys())[0])

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
            sma_forecast=7.0, sma_ma_error=3.0,
            cma_forecast=8.0, cma_ma_error=2.0,
            wma_forecast=8.66666, wma_ma_error=1.33,
            single_forecast=7.760825, single_ma_error=1.577526,
            double_forecast=9.481168, double_ma_error=2.691897,
            triple_forecast=9.451321, triple_ma_error=3.432094,
            holt_forecast=11, holt_ma_error=0
        )

    def get_test_data(self, test_name):
        """
        return tupla in, out with the values to use in the test.
              values, out = self.get_test_data(test_name)
        """
        data = {
            'test_01': self.get_test_01_data(),
            'test_02': self.get_test_02_data(),
            'test_03': {'in': self.get_test_03_in(),
                        'out': self.get_test_03_out(),
                        },
            'test_04': {'in': self.get_test_04_in(),
                        'out': self.get_test_04_out(),
                        },
        }
        test_data = data.get(test_name)
        return test_data.get('in'), test_data.get('out')

    def get_test_01_data(self):
        """
        return dictionary with the keys (in, out).
        - in: values to create the forecast record. Used to config the test.
        - out: the expected results of the test.
        """
        values = {}
        val = 1
        for item in range(1, 81):
            fvfield = 'fv_{num:02d}'.format(num=item)
            values.update({fvfield: val})
            if val == 30:
                val = 1
            else:
                val += 1

        out = dict(
            cma_forecast=14.0,
            cma_ma_error=3.157895,
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
        return {'in': values, 'out': out}


    def get_test_02_data(self):
        """
        return dictionary with the keys (in, out).
        - in: values to create the forecast record. Used to config the test.
        - out: the expected results of the test.
        """
        values = {}
        val = 1
        for item in range(1, 11):
            fvfield = 'fv_{num:02d}'.format(num=item)
            values.update({fvfield: val})
            val += 1
        out = dict(
            cma_forecast=4.0,
            cma_ma_error=2,
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
        return {'in': values, 'out': out}

    def _test_03(self, period):
        """ base for various periods """
        values = self.get_test_03_in()
        values.update(holt_period=period)
        forecast = self.forecast_obj.create(values)
        forecast.calculate()
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

    def get_test_03_in(self):
        """
        This method will return the forecast input values in a list.
        """
        data = {
            'fv_01': 133,
            'fv_02': 155,
            'fv_03': 165,
            'fv_04': 171,
            'fv_05': 194,
            'fv_06': 231,
            'fv_07': 274,
            'fv_08': 312,
            'fv_09': 313,
            'fv_10': 333,
            'fv_11': 343,
            'holt_alpha': 0.7,
            'beta': 0.6,
        }
        return data

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
        values = self.get_test_04_in()
        forecast = self.forecast_obj.create(values)
        forecast.calculate()
        out = self.get_test_04_out()
        self.compare(out, forecast.read(out.keys())[0])

    def get_test_04_in(self):
        """
        This are data to run the forecast test_04
        """
        data = {
            'fv_01': 105,
            'fv_02': 100,
            'fv_03': 105,
            'fv_04': 95,
            'fv_05': 100,
            'fv_06': 95,
            'fv_07': 105,
            'fv_08': 120,
            'fv_09': 115,
            'fv_10': 125,
            'fv_11': 120,
            'fv_12': 120,
        }
        return data

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
        values = self.get_test_05_in()
        forecast = self.forecast_obj.create(values)
        forecast.calculate()
        self.assertEqual(forecast.period, 3)
        out = self.get_test_05_out()
        self.compare(out, forecast.read(out.keys())[0])

    def get_test_05_in(self):
        """
        This are data to run the forecast test_05
        """
        data = {
            'fv_01': 80,
            'fv_02': 90,
            'fv_03': 85,
            'fv_04': 70,
            'fv_05': 80,
            'fv_06': 105,
            'fv_07': 100,
            'fv_08': 105,
            'fv_09': 100,
            'fv_10': 105,
            'fv_11': 100,
            'fv_12': 150,
            'period': 3,
        }
        return data

    def get_test_05_out(self):
        """
        Return a dictionary with the expected result of the test.
        """
        return dict(
            sma_forecast=101.66, sma_ma_error=14.07,
            cma_forecast=118.33, cma_ma_error=7.9,
        )
