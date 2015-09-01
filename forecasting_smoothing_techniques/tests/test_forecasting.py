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

from openerp import _, tools
from openerp.exceptions import ValidationError
from openerp.tests import common
import pandas as pd
import numpy.testing as npt
import numpy as np
import csv


class TestForecasting(common.TransactionCase):

    """
    Test that the forecasting smothing model is working propertly.
    """

    maxDiff = None

    def setUp(self):
        super(TestForecasting, self).setUp()
        self.forecast_obj = self.env['forecasting.smoothing.techniques']
        self.fdata_obj = self.env['forecasting.smoothing.data']

    def compare(self, expected, real):
        """
        Compare the correct result with the real result. Print logger with
        error tag.
        """
        elist = list()
        keys = expected.keys()
        keys.sort()
        for key in keys:
            vreal = real.get(key)
            vexpected = expected.get(key)

            if isinstance(vexpected, (float,)):
                elist += self.compare_values(key, vreal, vexpected)
            elif isinstance(vexpected, (pd.DataFrame,)):

                vexpected = vexpected.to_dict(orient='dict')

                # Get real result of the values
                fields_to_compare = vexpected.keys() + ['sequence']
                value_ids = self.fdata_obj.browse(vreal).read(
                    fields_to_compare)
                for item in value_ids:
                    item.pop('id')

                # Transform to DataFrame object to make it easy to manage.
                vreal = pd.DataFrame(value_ids)
                vreal.set_index('sequence', inplace=True)
                vreal = vreal.reindex_axis(sorted(vreal.columns), axis=1)

                # Compare actual and expected values (Transform to dict)
                vreal = vreal.to_dict(orient='dict')
                for (fname, values) in vreal.iteritems():
                    for val in values:
                        actual = vreal.get(fname).get(val)
                        if np.isnan(actual):
                            actual = np.nan_to_num(actual)
                        wanted = vexpected.get(fname).get(val)
                        elist += self.compare_values(
                            fname, actual, wanted, val=val)

        error_msg = '\n'.join(['\n', _('Fall forecast calculation ')] + elist)
        self.assertTrue(elist == [], error_msg)

    def compare_values(self, key, vreal, vexpected, val=False):
        """
        Compare two float values add return an error message.
        """
        error_msg = "{key:15} {real:15} != {expected:15} {ca} {diff:15}"
        if val:
            error_msg += '   at value with sequence {val}'
        vdiff = abs(vreal - float(vexpected))
        elist = []
        if not np.allclose([vreal], [float(vexpected)], 0.9):
            elist = [error_msg.format(
                key=key,
                real=vreal,
                expected=vexpected,
                ca=vexpected < vreal and '>' or '<',
                val=val,
                diff=vdiff)]
        return elist

    def get_expected_value_ids_results(self, test_file):
        """
        return a pandas.DataFrame object with the expected value_ids
        forecasting results.
        """
        infile = tools.file_open(test_file)
        reader = csv.DictReader(infile)
        result = {}
        for row in reader:
            key = int(row.pop('sequence'))
            if key in result:
                # implement your duplicate row handling here
                pass
            result[key] = dict([
                (kval, val != '' and float(val) or 0.0)
                for kval, val in row.iteritems()
            ])
        result = pd.DataFrame.from_dict(result, orient='index')
        result['sequence'] = result.index
        result.set_index('sequence', inplace=True)
        result = result.reindex_axis(sorted(result.columns), axis=1)
        return result

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
        values = forecast.value_ids
        self.assertFalse(any(values), 'Must be blank')
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
        forecast = self.forecast_obj.browse(self.ref(
            'forecasting_smoothing_techniques.fst_demo_01'))
        self.assertTrue(len(forecast.value_ids))
        forecast.clear()
        self.assertFalse(len(forecast.value_ids))

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
        test_file = 'forecasting_smoothing_techniques/tests/test_01_out.csv'
        value_ids = self.get_expected_value_ids_results(test_file)
        return dict(
            value_ids=value_ids,
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
        test_file = 'forecasting_smoothing_techniques/tests/test_02_out.csv'
        value_ids = self.get_expected_value_ids_results(test_file)
        return dict(
            value_ids=value_ids,
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
        test_file = 'forecasting_smoothing_techniques/tests/test_03_out.csv'
        value_ids = self.get_expected_value_ids_results(test_file)
        out.update(value_ids=value_ids)
        if period == 1:
            out.update(
                holt_period=1, holt_forecast=359.70, holt_ma_error=17.67,
                sma_forecast=292.60, sma_ma_error=76.4,
                cma_forecast=315.00, cma_ma_error=48.2,
            )
        elif period == 2:
            out.update(
                holt_period=2, holt_forecast=372.6,
            )
        elif period == 3:
            out.update(
                holt_period=3, holt_forecast=385.4,
            )
        elif period == 4:
            out.update(
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
        test_file = 'forecasting_smoothing_techniques/tests/test_04_out.csv'
        value_ids = self.get_expected_value_ids_results(test_file)
        return dict(
            value_ids=value_ids,
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
        test_file = 'forecasting_smoothing_techniques/tests/test_05_out.csv'
        value_ids = self.get_expected_value_ids_results(test_file)
        return dict(
            value_ids=value_ids,
            sma_forecast=101.66, sma_ma_error=14.07,
            cma_forecast=118.33, cma_ma_error=7.9,
        )
