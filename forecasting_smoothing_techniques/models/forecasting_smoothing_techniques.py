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

    _sql_constraints = [
        ('sequence_uniq', 'unique(sequence, forecast_id)',
            'Several sequences with the same value do not make sense yet!'),
    ]


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
        compute='_compute_simple_move_average',
        help="Simple Moving Average Forcasting (SMA)"
    )
    sma_ma_error = fields.Float(
        'MA Error',
        compute='_compute_simple_move_average',
        help="Mean Absolute Error for SMA"
    )

    # Cumulative Moving Average
    cma_forecast = fields.Float(
        'Forecast',
        compute='_compute_cummulative_move_average',
        help="Cumulative Moving Average Forcasting (CMA)"
    )
    cma_ma_error = fields.Float(
        'MA Error',
        compute='_compute_cummulative_move_average',
        help="Mean Absolute Error for CMA"
    )

    # Weighted Moving Average
    wma_forecast = fields.Float(
        'Forecast',
        compute='_compute_weighted_move_average',
        help="Weighted Moving Average Forecasting (WMA)"
    )
    wma_ma_error = fields.Float(
        'MA Error',
        compute='_compute_weighted_move_average',
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
        compute='_compute_exp_smoothing',
        help="Single Exponential Smoothing (SES)"
    )
    single_ma_error = fields.Float(
        'MA Error',
        compute='_compute_exp_smoothing',
        help="Mean Absolute Error for SES"
    )
    double_forecast = fields.Float(
        'Forecast',
        compute='_compute_exp_smoothing',
        help="Double Exponential Smoothing (DES)"
    )
    double_ma_error = fields.Float(
        'MA Error',
        compute='_compute_exp_smoothing',
        help="Mean Absolute Error for DES"
    )
    triple_forecast = fields.Float(
        'Forecast',
        compute='_compute_exp_smoothing',
        help="Triple Exponential Smoothing (TES)"
    )
    triple_ma_error = fields.Float(
        'MA Error',
        compute='_compute_exp_smoothing',
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

    @api.one
    @api.depends('value_ids', 'period')
    def _compute_cummulative_move_average(self):
        """
        This method calculate the CUMULATIVE MOVING AVERAGE forecasting
        smoothing method (CMA) and Mean Absolute error.
        """
        values = self.value_ids
        if not values:
            return True
        period = self.period
        values_to_forecast = values[period-1:]
        for value in values_to_forecast:
            value_set = values[value.sequence-period:value.sequence]
            value.write({
                'cma': sum([val.value for val in value_set])
                / float(period)})
            value.write({'cma_error': abs(value.cma - value_set[-1].value)})
        self.cma_forecast = values_to_forecast[-1].cma
        self.cma_ma_error = (
            sum([val.cma_error for val in values_to_forecast]) /
            len(values_to_forecast))
        return True

    @api.one
    @api.depends()
    def _compute_simple_move_average(self):
        """
        This method calculate the SIMPLE MOVING AVERAGE forecasting
        smoothing method (SMA) and Mean Absolute error.
        """
        forecast = self.read()[0]
        values = forecast.get('value_ids', [])
        period = forecast.get('period')
        if not values:
            return True
        fdata_obj = self.env['forecasting.smoothing.data']
        values = fdata_obj.browse(values).read(['value', 'sequence'])
        values_to_forecast = values[period:]
        value_ids = []
        sma_error_total = 0.0

        for value in values_to_forecast:
            sequence = value.get('sequence')
            first = sequence - period - 1
            last = sequence - 1
            value_set = values[first:last]
            sma = sum(
                [val.get('value') for val in value_set]) / float(period)
            sma_error = abs(sma - value.get('value'))
            value_ids.append(
                (1, value.get('id'), {'sma': sma, 'sma_error': sma_error}))
            sma_error_total += sma_error

        self.sma_forecast = sma
        self.sma_ma_error = sma_error_total/len(values_to_forecast)
        self.write({'value_ids': value_ids})

    @api.one
    @api.depends()
    def _compute_weighted_move_average(self):
        """
        This method calculate the WEIGHTED MOVING AVERAGE forecasting
        smoothing method (WMA) and Mean Absolute error.
        """
        forecast = self.read()[0]
        values = forecast.get('value_ids', [])
        period = forecast.get('period')
        if not values:
            return True
        fdata_obj = self.env['forecasting.smoothing.data']
        values = fdata_obj.browse(values).read(['value', 'sequence'])
        weight = (float(period) * (float(period) + 1.0)) / 2.0
        values_to_forecast = values[period-1:]

        value_ids = []
        wma_error_total = 0.0
        for value in values_to_forecast:
            sequence = value.get('sequence')
            value_set = values[sequence-period:sequence]
            wma = sum([((day) / weight) * item.get('value')
                        for (day, item) in enumerate(value_set, 1)])
            wma_error = abs(wma - value_set[-1].get('value'))
            wma_error_total += wma_error
            value_ids.append(
                (1, value.get('id'), {'wma': wma, 'wma_error': wma_error}))

        self.wma_forecast = wma
        self.wma_ma_error = wma_error_total / len(values_to_forecast)
        self.write({'value_ids': value_ids})

    @api.one
    @api.depends('value_ids', 'exp_alpha')
    def _compute_exp_smoothing(self):
        """
        Single, Double, & Triple Exponential Smoothing
        Note: Represente function compute3
        """
        values = self.value_ids
        if not values:
            return True

        alpha = self.exp_alpha

        values[0].write({'es1': values[1].value})
        values[0].write({'es2': values[1].value})
        values[0].write({'es3': values[1].value})

        values_to_forecast = values[1:]
        for value in values_to_forecast:
            value.write({'es1':
                         alpha * value.value +
                         (1.0 - alpha) * values[value.sequence-2].es1})
            value.write({'es2':
                         alpha * value.es1 +
                         (1.0 - alpha) * values[value.sequence-2].es2})
            value.write({'es3':
                         alpha * value.es2 +
                         (1.0 - alpha) * values[value.sequence-2].es3})

        last_value = values[-1]
        a2 = 2.0 * last_value.es1 - last_value.es2
        b2 = (alpha/(1.0-alpha)) * (last_value.es1 - last_value.es2)
        a3 = 3.0 * last_value.es1 - 3.0 * last_value.es2 + last_value.es3
        b3 = ((alpha/(2.0 * pow(1.0-alpha, 2.0))) * (
            (6.0 - 5.0 * alpha) * last_value.es1 -
            (10.0 - 8.0 * alpha) * last_value.es2 +
            (4.0 - 3.0 * alpha) * last_value.es3))
        c3 = (pow((alpha/(1.0 - alpha)), 2.0) *
              (last_value.es1 - 2.0 * last_value.es2 + last_value.es3))

        self.single_forecast = last_value.es1
        self.double_forecast = a2 + b2
        self.triple_forecast = a3 + b3 + 0.5 * c3

        for value in values:
            value.write({'es1_error': abs(value.es1 - value.value)})
            value.write({'es2_error': abs(value.es2 - value.value)})
            value.write({'es3_error': abs(value.es3 - value.value)})

        numv = float(len(values))
        self.single_ma_error = sum(values.mapped('es1_error')) / numv
        self.double_ma_error = sum(values.mapped('es2_error')) / numv
        self.triple_ma_error = sum(values.mapped('es3_error')) / numv
        return True

    @api.one
    @api.depends('value_ids', 'holt_alpha', 'beta', 'holt_period')
    def _compute_holt(self):
        """
        Holt's Linear Smoothing
        Note: It represent function compute20
        """
        values = self.value_ids
        if not values:
            return True
        numv = len(values)
        alpha = self.holt_alpha
        beta = self.beta
        period = self.holt_period

        values[0].write({
            'holt': 0.0, 'holt_level': 0.0, 'holt_trend': 0.0
        })

        values[1].write({
            'holt_level': values[1].value,
            'holt_trend': values[1].value - values[0].value,
            'holt': 0.0,
        })
        values_to_forecast = values[2:]
        for value in values_to_forecast:
            value.write({
                'holt': values[value.sequence-2].holt_level +
                values[value.sequence-2].holt_trend})
            value.write({'holt_level':
                         alpha * value.value + (1.0 - alpha) * value.holt})
            value.write({
                'holt_trend':
                    (beta * (value.holt_level -
                             values[value.sequence-2].holt_level)
                     + (1.0 - beta) * values[value.sequence-2].holt_trend)
            })
        self.holt_forecast = (values_to_forecast[-1].holt_level + period *
                              values_to_forecast[-1].holt_trend)
        for value in values_to_forecast:
            value.write({'holt_error': abs(value.holt - value.value)})
        self.holt_ma_error = sum(values.mapped('holt_error')) / (
            float(numv) - 3.0)
        return True
