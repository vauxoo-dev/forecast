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

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError, Warning as UserError
import pandas as pd


class ForecastingSmoothingData(models.Model):
    _name = 'forecasting.smoothing.data'
    _description = 'Forecasting Smoothing Data'
    _rec_name = 'sequence'

    @api.model
    def _default_forecast(self):
        forecast_id = self._context.get('forecast_id', False)
        return forecast_id

    sequence = fields.Integer(
        help="Position in the list regarding this list and this forecast",
        default=10)
    value = fields.Float()
    forecast_id = fields.Many2one(
        'forecasting.smoothing.techniques',
        required=True,
        default=_default_forecast,
        help="Forecast which this data is related to")

    _sql_constraints = [
        ('sequence_uniq', 'unique(sequence, forecast_id)',
            'Several sequences with the same value do not make sense yet!'),
    ]


class ForecastingSmoothingResult(models.Model):
    _name = 'forecasting.smoothing.result'
    _description = 'Forecasting Smoothing Results'

    forecast_id = fields.Many2one(
        'forecasting.smoothing.techniques',
        # required=True,
        help="Forecast which this data is related to")
    value_id = fields.Many2one(
        'forecasting.smoothing.data', 'Forecast Data')
    sequence = fields.Integer(
        help="Position in the list regarding this list and this forecast")
    sma = fields.Float(
        'SMA', help="Simple Moving Average Forcasting (SMA)")
    sma_error = fields.Float(
        'SMA MA Error', help="Mean Absolute Error for SMA")
    cma = fields.Float(
        'CMA', help="Cumulative Moving Average Forcasting (CMA)")
    cma_error = fields.Float(
        'CMA MA Error', help="Mean Absolute Error for CMA")
    wma = fields.Float(
        'WMA', help="Weighted Moving Average Forecasting (WMA)")
    wma_error = fields.Float(
        'WMA MA Error', help="Mean Absolute Error for WMA")
    es1 = fields.Float(
        'ES1', help="Single Exponential Smoothing (ES1)")
    es1_error = fields.Float(
        'ES1 MA Error', help="Mean Absolute Error for ES1")
    es2 = fields.Float(
        'ES2', help="Double Exponential Smoothing (ES2)")
    es2_error = fields.Float(
        'ES2 MA Error', help="Mean Absolute Error for ES2")
    es3 = fields.Float(
        'ES3', help="Triple Exponential Smoothing (ES3)")
    es3_error = fields.Float(
        'ES3 MA Error', help="Mean Absolute Error for ES3")
    holt = fields.Float(
        'HOLT', help="Holt's Linear Smoothing (HOLT)")
    holt_error = fields.Float(
        'HOLT MA Error', help="Mean Absolute Error for HOLT")
    holt_level = fields.Float(
        'HOLT LEVEL', help="Holt's Linear Smoothing Level function")
    holt_trend = fields.Float(
        'HOLT TREND', help="Holt's Linear Smoothing Trend function")


class ForecastingSmoothingTechniques(models.Model):

    _name = 'forecasting.smoothing.techniques'
    _description = 'Forecasting Smoothing Techniques'

    @api.model
    def _default_product(self):
        '''
        Usability feature -
        TODO: move for product_forecasting module
        :return:
        '''
        product_id = self._context.get('product_tmpl_id', False)
        return product_id

    @api.model
    def _default_name(self):
        '''
        Usability feature -
        TODO: move for product_forecasting module
        :return:
        '''
        product_id = self._context.get('product_tmpl_id', False)
        return '%s: ' % self.env['product.template'].browse(product_id).name

    name = fields.Char(
        help='Name given by the user to quick reference the forecasting',
        default=_default_name)

    value_ids = fields.One2many(
        'forecasting.smoothing.data',
        'forecast_id',
        string='Values',
        copy=False,
        help='List of values to be used to compute this forecast')

    result_ids = fields.One2many(
        'forecasting.smoothing.result',
        'forecast_id',
        'Results')

    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Product',
        help='Product related to the current forecasting',
        default=_default_product,
        track_visibility='always')

    # Moving Average
    period = fields.Integer(
        'Period', default=5, help="Moving Average Period")

    # Simple Moving Average
    sma_forecast = fields.Float(
        'Forecast',
        compute='_compute_sma',
        help="Simple Moving Average Forcasting (SMA)"
    )
    sma_ma_error = fields.Float(
        'MA Error',
        compute='_compute_sma',
        help="Mean Absolute Error for SMA"
    )

    # Cumulative Moving Average
    cma_forecast = fields.Float(
        'Forecast',
        compute='_compute_cma',
        help="Cumulative Moving Average Forcasting (CMA)"
    )
    cma_ma_error = fields.Float(
        'MA Error',
        compute='_compute_cma',
        help="Mean Absolute Error for CMA"
    )

    # Weighted Moving Average
    wma_forecast = fields.Float(
        'Forecast',
        compute='_compute_wma',
        help="Weighted Moving Average Forecasting (WMA)"
    )
    wma_ma_error = fields.Float(
        'MA Error',
        compute='_compute_wma',
        help="Mean Absolute Error for WMA"
    )

    # Single, Double, & Triple Exponential Smoothing
    exp_alpha = fields.Float(
        'Alpha', default=0.3,
        help='Exponential Alpha. A small alpha provides a detectable and'
             ' visible smoothing. While a large alpha provides a fast'
             ' response to the recent changes in the time series but'
             ' provides a smaller amount of smoothing')

    single_forecast = fields.Float(
        'Forecast',
        compute='_compute_exp',
        help="Single Exponential Smoothing (SES)"
    )
    single_ma_error = fields.Float(
        'MA Error',
        compute='_compute_exp',
        help="Mean Absolute Error for SES"
    )
    double_forecast = fields.Float(
        'Forecast',
        compute='_compute_exp',
        help="Double Exponential Smoothing (DES)"
    )
    double_ma_error = fields.Float(
        'MA Error',
        compute='_compute_exp',
        help="Mean Absolute Error for DES"
    )
    triple_forecast = fields.Float(
        'Forecast',
        compute='_compute_exp',
        help="Triple Exponential Smoothing (TES)"
    )
    triple_ma_error = fields.Float(
        'MA Error',
        compute='_compute_exp',
        help="Mean Absolute Error for TES"
    )

    # Holt's Linear Smoothing
    holt_alpha = fields.Float(
        'Alpha', default=0.3,
        help="Holt's Alpha Parameter"
    )
    beta = fields.Float(
        'Beta', default=0.03,
        help="Holt's Beta Parameter"
    )
    holt_period = fields.Float(
        "Holt's Period", default=1,
        help="Forecasting K periods into the future to calculate Holt's"
             " Linear Smoothing")
    holt_forecast = fields.Float(
        'Forecast',
        compute='_compute_holt',
        help="Holt's Linear Smoothing (HOLT)"
    )
    holt_ma_error = fields.Float(
        'MA Error',
        compute='_compute_holt',
        help="Mean Absolute Error for HOLT"
    )

    @api.constrains('period')
    def _check_period(self):
        if self.period <= 1:
            raise ValidationError(
                _("Period must be an integer greater than 1."))

    @api.constrains('exp_alpha')
    def _check_exp_alpha(self):
        if self.exp_alpha <= 0 or self.exp_alpha >= 1:
            raise ValidationError(_("Alpha should be between 0 and 1."))

    @api.constrains('holt_alpha')
    def _check_holt_alpha(self):
        if self.holt_alpha <= 0 or self.holt_alpha >= 1:
            raise ValidationError(_("Alpha should be between 0 and 1."))

    @api.constrains('beta')
    def _check_beta(self):
        if self.beta <= 0 or self.beta >= 1:
            raise ValidationError(_("Beta should be between 0 and 1."))

    def fields_section(self, fsection='all'):
        """
        This is used for get or clear section group fields.
        @return fields the list of fileds by section.  Dictionary (key group,
        values list of field names).
        """
        fields_section = dict(
            sma=['sma_forecast', 'sma_ma_error'],
            cma=['cma_forecast', 'cma_ma_error'],
            wma=['wma_forecast', 'wma_ma_error'],
            single=['single_forecast', 'single_ma_error'],
            double=['double_forecast', 'double_ma_error'],
            triple=['triple_forecast', 'triple_ma_error'],
            holt=['holt_forecast', 'holt_ma_error'],
        )
        fields_section.update({'all': [
            fname
            for fgroup in fields_section.values()
            for fname in fgroup]})

        if fsection not in fields_section.keys():
            raise UserError(
                _('There is not groups of fields defined') + ' ' + fsection)
        elif fsection:
            return fields_section.get(fsection)
        else:
            return fields_section

    @api.multi
    def reset_defaults(self):
        """
        Reset defaults for the variables used in the current calc.
        ['period', 'exp_alpha', 'holt_alpha', 'beta', 'holt_period']
        """
        parameter_fields = [
            'period', 'exp_alpha', 'holt_alpha', 'beta', 'holt_period']
        defaults = self.default_get(parameter_fields)
        self.write(defaults)
        return True

    @api.multi
    def clear(self):
        """
        Clear all the fields.
        """
        self.write({
            'value_ids': [(2, value.id) for value in self.value_ids]})
        return True

    @api.multi
    def get_result_ids_dict(self, data):
        """
        @param data: DataFrame object with the forecasting results per
        point.
        return a list with the to update the o2m values value_ids in the
        forecasting object.
        """
        result_ids = list()
        for index in range(1, len(data) + 1):
            new_values = data.loc[index].to_dict()
            new_values.pop('value')
            value_id = int(new_values.pop('id'))
            new_values.update(value_id=value_id, forecast_id=self.id)
            result_ids.append((0, 0, new_values))
        return result_ids

    @api.multi
    def get_values_dataframe(self, values, forecast_cols):
        """
        Transform value data to pandas.DataFrame object
        """
        fdata_obj = self.env['forecasting.smoothing.data']
        values = fdata_obj.browse(values).read(['value', 'sequence'])
        cols = ['id', 'value', 'sequence'] + forecast_cols
        data = pd.DataFrame(values, columns=cols)
        data.set_index('sequence', inplace=True)
        data.insert(0, 'sequence', data.index)
        return data

    @api.one
    @api.depends('period')
    def _compute_cma(self):
        """
        This method calculate the CUMULATIVE MOVING AVERAGE forecasting
        smoothing method (CMA) and Mean Absolute error.
        """
        # Get basic parameters to calculate
        forecast = self.read()[0]
        values = forecast.get('value_ids', [])
        period = forecast.get('period')

        # Check minimum data
        if not values:
            return True

        # Transform value data to Dataframe pandas object
        data = self.get_values_dataframe(values, ['cma', 'cma_error'])

        # Calculate Forecasting for the other points
        for index in range(period, len(data) + 1):
            value_set = data[:index].tail(period)
            cma = value_set.value.sum() / float(period)
            data.at[index, 'cma'] = cma

        # Calculate mean errors
        # TODO can be improve using mean() method
        data = data.assign(
            cma_error=lambda x: abs(x.cma - x.value),
        )
        data.fillna(0.0, inplace=True)
        data.set_index('sequence', inplace=True)

        # Save individual values results
        result_ids = self.get_result_ids_dict(data)

        # Save global results
        cma_forecast = cma
        cma_ma_error = data.cma_error.sum() / data.cma.count()

        # Write values
        self.cma_forecast = cma_forecast
        self.cma_ma_error = cma_ma_error

        # Write individual values
        self.result_ids.unlink()
        self.write({'result_ids': result_ids})

        # TODO check what to do with this
        # result = fres_obj.create(new_values)
        # fres_obj = self.env['forecasting.smoothing.result']

    @api.one
    @api.depends('period')
    def _compute_sma(self):
        """
        This method calculate the SIMPLE MOVING AVERAGE forecasting
        smoothing method (SMA) and Mean Absolute error.
        """
        # Get basic parameters to calculate
        forecast = self.read()[0]
        values = forecast.get('value_ids', [])
        period = forecast.get('period')

        # Check minimum data
        if not values:
            return True

        # Transform value data to Dataframe pandas object
        data = self.get_values_dataframe(values, ['sma', 'sma_error'])

        # Calculate Forecasting for the other points
        for index in range(period+1, len(data) + 1):
            value_set = data[:index-1].tail(period)
            sma = value_set.value.sum() / float(period)
            data.at[index, 'sma'] = sma

        # Calculate mean errors
        # TODO can be improve using mean() method
        data = data.assign(
            sma_error=lambda x: abs(x.sma - x.value),
        )
        data.fillna(0.0, inplace=True)
        data.set_index('sequence', inplace=True)

        # Save individual values results
        result_ids = self.get_result_ids_dict(data)

        # Save global results
        sma_forecast = sma
        sma_ma_error = data.sma_error.sum() / data.sma.count()

        # Write values
        self.sma_forecast = sma_forecast
        self.sma_ma_error = sma_ma_error

        # Write individual values
        self.result_ids.unlink()
        self.write({'result_ids': result_ids})

    @api.one
    @api.depends('period')
    def _compute_wma(self):
        """
        This method calculate the WEIGHTED MOVING AVERAGE forecasting
        smoothing method (WMA) and Mean Absolute error.
        """
        # Get basic parameters to calculate
        forecast = self.read()[0]
        values = forecast.get('value_ids', [])
        period = forecast.get('period')

        # Check minimum data
        if not values:
            return True

        # Transform value data to Dataframe pandas object
        data = self.get_values_dataframe(values, ['wma', 'wma_error'])

        weight = (float(period) * (float(period) + 1.0)) / 2.0

        # Calculate Forecasting for the other points
        for index in range(period, len(data) + 1):
            value_set = data[:index].tail(period)
            wma = sum([
                ((day) / weight) * value
                for (day, value) in enumerate(value_set.value.values, 1)])
            data.at[index, 'wma'] = wma

        # Calculate mean errors
        # TODO can be improve using mean() method
        data = data.assign(
            wma_error=lambda x: abs(x.wma - x.value),
        )
        data.fillna(0.0, inplace=True)
        data.set_index('sequence', inplace=True)

        # Save individual values results
        result_ids = self.get_result_ids_dict(data)

        # Save global results
        wma_forecast = wma
        wma_ma_error = data.wma_error.sum() / data.wma.count()

        # Write values
        self.wma_forecast = wma_forecast
        self.wma_ma_error = wma_ma_error

        # Write individual values
        self.result_ids.unlink()
        self.write({'result_ids': result_ids})

    @api.one
    @api.depends('exp_alpha')
    def _compute_exp(self):
        """
        Single, Double, & Triple Exponential Smoothing
        Note: Represente function compute3
        """

        # Get basic parameters to calculate
        forecast = self.read()[0]
        values = forecast.get('value_ids', [])
        alpha = forecast.get('exp_alpha')

        # Check minimum data
        if not values:
            return True

        # Transform value data to Dataframe pandas object
        data = self.get_values_dataframe(values, ['es1', 'es1_error',
                                                  'es2', 'es2_error',
                                                  'es3', 'es3_error'])

        # Calculate Forecasting per first point
        val1 = data.loc[2].value
        data[:1] = data.query('sequence == 1').assign(
            es1=val1, es2=val1, es3=val1)

        # Calculate Forecasting for the other points
        for index in range(2, len(data) + 1):
            value = data.loc[index].value
            last_item = data.loc[index-1]
            es1 = alpha * value + (1.0 - alpha) * last_item.es1
            es2 = alpha * es1 + (1.0 - alpha) * last_item.es2
            es3 = alpha * es2 + (1.0 - alpha) * last_item.es3
            data.at[index, 'es1'] = es1
            data.at[index, 'es2'] = es2
            data.at[index, 'es3'] = es3

        # Calculate mean errors
        # TODO can be improve using mean() method
        data = data.assign(
            es1_error=lambda x: abs(x.es1 - x.value),
            es2_error=lambda x: abs(x.es2 - x.value),
            es3_error=lambda x: abs(x.es3 - x.value),
        )
        data.fillna(0.0, inplace=True)
        data.set_index('sequence', inplace=True)

        # Save individual values results
        result_ids = self.get_result_ids_dict(data)

        # Save global results
        last = data.tail(1).iloc[-1]
        a2 = 2.0 * last.es1 - last.es2
        b2 = (alpha/(1.0-alpha)) * (last.es1 - last.es2)
        a3 = 3.0 * last.es1 - 3.0 * last.es2 + last.es3
        b3 = ((alpha/(2.0 * pow(1.0-alpha, 2.0))) * (
            (6.0 - 5.0 * alpha) * last.es1 - (10.0 - 8.0 * alpha) * last.es2
            + (4.0 - 3.0 * alpha) * last.es3))
        c3 = (pow((alpha/(1.0 - alpha)), 2.0) *
              (last.es1 - 2.0 * last.es2 + last.es3))
        single_forecast = last.es1
        double_forecast = a2 + b2
        triple_forecast = a3 + b3 + 0.5 * c3

        # Write values
        self.single_forecast = single_forecast
        self.double_forecast = double_forecast
        self.triple_forecast = triple_forecast
        self.single_ma_error = data.es1_error.sum() / len(data)
        self.double_ma_error = data.es2_error.sum() / len(data)
        self.triple_ma_error = data.es3_error.sum() / len(data)

        # Write individual values
        self.result_ids.unlink()
        self.write({'result_ids': result_ids})

    @api.one
    @api.depends('holt_alpha', 'beta', 'holt_period')
    def _compute_holt(self):
        """
        Holt's Linear Smoothing forecasting calculation
        """
        # Get basic parameters to make the forecasting calculation
        forecast = self.read()[0]
        values = forecast.get('value_ids', [])
        alpha = forecast.get('holt_alpha')
        beta = forecast.get('beta')
        period = forecast.get('holt_period')

        # Check minimum data
        if not values:
            return True

        # Transform value data to pandas.Dataframe object
        data = self.get_values_dataframe(values, [
            'holt', 'holt_level', 'holt_trend', 'holt_error'])

        # NOTE: Forecasting first point do not exist for this forcasting

        # Calculate Forecasting second point
        holt_level = data.loc[2].value,
        holt_trend = data.loc[2].value - data.loc[1].value,

        data[1:2] = data.query('sequence == 2').assign(
            holt_level=holt_level, holt_trend=holt_trend)

        # Calculate Forecasting for the other 2+n points
        for index in range(3, len(data) + 1):
            value = data.loc[index].value
            prev = data.loc[index-1]
            holt_func = prev.holt_level + prev.holt_trend
            holt_level = alpha * value + (1.0 - alpha) * holt_func
            holt_trend = (
                beta * (holt_level - prev.holt_level) + (1.0 - beta) *
                prev.holt_trend)
            data.at[index, 'holt'] = holt_func
            data.at[index, 'holt_level'] = holt_level
            data.at[index, 'holt_trend'] = holt_trend

        # Calculate mean error
        # TODO can be improve using mean() method?
        data = data.assign(holt_error=lambda x: abs(x.holt - x.value))
        data.fillna(0.0, inplace=True)
        data.set_index('sequence', inplace=True)

        # Save individual values results
        result_ids = self.get_result_ids_dict(data)

        # Save global results
        last = data.tail(1).iloc[-1]
        holt_forecast = last.holt_level + period * last.holt_trend
        holt_ma_error = data.holt_error.sum() / (len(data) - 3.0)

        # Write values
        self.holt_forecast = holt_forecast
        self.holt_ma_error = holt_ma_error

        # Write individual values
        self.result_ids.unlink()
        self.write({'result_ids': result_ids})
