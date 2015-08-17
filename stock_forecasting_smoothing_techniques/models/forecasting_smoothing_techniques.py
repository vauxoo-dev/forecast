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


class ForecastingSmoothingTechniques(models.Model):

    _name = 'forecasting.smoothing.techniques'
    _description = 'Forecasting Smoothing Techniques'

    name = fields.Char('Name')

    # Forecast Values range(80)
    fv_01 = fields.Float('Forecast Value 01')
    fv_02 = fields.Float('Forecast Value 02')
    fv_03 = fields.Float('Forecast Value 03')
    fv_04 = fields.Float('Forecast Value 04')
    fv_05 = fields.Float('Forecast Value 05')
    fv_06 = fields.Float('Forecast Value 06')
    fv_07 = fields.Float('Forecast Value 07')
    fv_08 = fields.Float('Forecast Value 08')
    fv_09 = fields.Float('Forecast Value 09')
    fv_10 = fields.Float('Forecast Value 10')
    fv_11 = fields.Float('Forecast Value 11')
    fv_12 = fields.Float('Forecast Value 12')
    fv_13 = fields.Float('Forecast Value 13')
    fv_14 = fields.Float('Forecast Value 14')
    fv_15 = fields.Float('Forecast Value 15')
    fv_16 = fields.Float('Forecast Value 16')
    fv_17 = fields.Float('Forecast Value 17')
    fv_18 = fields.Float('Forecast Value 18')
    fv_19 = fields.Float('Forecast Value 19')
    fv_20 = fields.Float('Forecast Value 20')
    fv_21 = fields.Float('Forecast Value 21')
    fv_22 = fields.Float('Forecast Value 22')
    fv_23 = fields.Float('Forecast Value 23')
    fv_24 = fields.Float('Forecast Value 24')
    fv_25 = fields.Float('Forecast Value 25')
    fv_26 = fields.Float('Forecast Value 26')
    fv_27 = fields.Float('Forecast Value 27')
    fv_28 = fields.Float('Forecast Value 28')
    fv_29 = fields.Float('Forecast Value 29')
    fv_30 = fields.Float('Forecast Value 30')
    fv_31 = fields.Float('Forecast Value 31')
    fv_32 = fields.Float('Forecast Value 32')
    fv_33 = fields.Float('Forecast Value 33')
    fv_34 = fields.Float('Forecast Value 34')
    fv_35 = fields.Float('Forecast Value 35')
    fv_36 = fields.Float('Forecast Value 36')
    fv_37 = fields.Float('Forecast Value 37')
    fv_38 = fields.Float('Forecast Value 38')
    fv_39 = fields.Float('Forecast Value 39')
    fv_40 = fields.Float('Forecast Value 40')
    fv_41 = fields.Float('Forecast Value 41')
    fv_42 = fields.Float('Forecast Value 42')
    fv_43 = fields.Float('Forecast Value 43')
    fv_44 = fields.Float('Forecast Value 44')
    fv_45 = fields.Float('Forecast Value 45')
    fv_46 = fields.Float('Forecast Value 46')
    fv_47 = fields.Float('Forecast Value 47')
    fv_48 = fields.Float('Forecast Value 48')
    fv_49 = fields.Float('Forecast Value 49')
    fv_50 = fields.Float('Forecast Value 50')
    fv_51 = fields.Float('Forecast Value 51')
    fv_52 = fields.Float('Forecast Value 52')
    fv_53 = fields.Float('Forecast Value 53')
    fv_54 = fields.Float('Forecast Value 54')
    fv_55 = fields.Float('Forecast Value 55')
    fv_56 = fields.Float('Forecast Value 56')
    fv_57 = fields.Float('Forecast Value 57')
    fv_58 = fields.Float('Forecast Value 58')
    fv_59 = fields.Float('Forecast Value 59')
    fv_60 = fields.Float('Forecast Value 60')
    fv_61 = fields.Float('Forecast Value 61')
    fv_62 = fields.Float('Forecast Value 62')
    fv_63 = fields.Float('Forecast Value 63')
    fv_64 = fields.Float('Forecast Value 64')
    fv_65 = fields.Float('Forecast Value 65')
    fv_66 = fields.Float('Forecast Value 66')
    fv_67 = fields.Float('Forecast Value 67')
    fv_68 = fields.Float('Forecast Value 68')
    fv_69 = fields.Float('Forecast Value 69')
    fv_70 = fields.Float('Forecast Value 70')
    fv_71 = fields.Float('Forecast Value 71')
    fv_72 = fields.Float('Forecast Value 72')
    fv_73 = fields.Float('Forecast Value 73')
    fv_74 = fields.Float('Forecast Value 74')
    fv_75 = fields.Float('Forecast Value 75')
    fv_76 = fields.Float('Forecast Value 76')
    fv_77 = fields.Float('Forecast Value 77')
    fv_78 = fields.Float('Forecast Value 78')
    fv_79 = fields.Float('Forecast Value 79')
    fv_80 = fields.Float('Forecast Value 80')

    # Moving Average
    period = fields.Integer('Period', default=5)

    # Simple Moving Average
    sma_forecast = fields.Float(
        'Forecast',
        compute='_compute_simple_move_average',
    )
    sma_ma_error = fields.Float(
        'MA Error',
        compute='_compute_simple_move_average',
    )

    # Cumulative Moving Average
    cma_forecast = fields.Float(
        'Forecast',
        compute='_compute_cummulative_move_average',
    )
    cma_ma_error = fields.Float(
        'MA Error',
        compute='_compute_cummulative_move_average',
    )

    # Weighted Moving Average
    wma_forecast = fields.Float(
        'Forecast',
        compute='_compute_weighted_move_average',
    )
    wma_ma_error = fields.Float(
        'MA Error',
        compute='_compute_weighted_move_average',
    )

    # Single, Double, & Triple Exponential Smoothing
    exp_alpha = fields.Float(
        'Alpha', default=0.3,
        help='A small alpha provides a detectable and visible smoothing.'
             ' While a large alpha provides a fast response to the recent'
             ' changes in the time series but provides a smaller amount'
             ' of smoothing')

    single_forecast = fields.Float(
        'Forecast',
        compute='_compute_exp_smoothing',
    )
    single_ma_error = fields.Float(
        'MA Error',
        compute='_compute_exp_smoothing',
    )
    double_forecast = fields.Float(
        'Forecast',
        compute='_compute_exp_smoothing',
    )
    double_ma_error = fields.Float(
        'MA Error',
        compute='_compute_exp_smoothing',
    )
    triple_forecast = fields.Float(
        'Forecast',
        compute='_compute_exp_smoothing',
    )
    triple_ma_error = fields.Float(
        'MA Error',
        compute='_compute_exp_smoothing',
    )

    # Holt's Linear Smoothing
    holt_alpha = fields.Float('Alpha', default=0.3)
    beta = fields.Float('Beta', default=0.03)
    holt_forecast = fields.Float(
        'Forecast',
        compute='_compute_holt'
    )
    holt_ma_error = fields.Float(
        'MA Error',
        compute='_compute_holt'
    )
    holt_period = fields.Float(
        'Period', default=1,
        help='forecasting K periods into the future')

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

    @api.multi
    def calculate(self):
        self._compute_simple_move_average()
        self._compute_cummulative_move_average()
        self._compute_weighted_move_average()
        self._compute_exp_smoothing()
        self._compute_holt()

    def fields_section(self, fsection):
        """
        This is used for get or clear section group fields.
        @return fields the list of fileds by section.  Dictionary (key group,
        values list of field names).
        """
        fields_section = dict(
            data=[
                'fv_01', 'fv_02', 'fv_03', 'fv_04', 'fv_05',
                'fv_06', 'fv_07', 'fv_08', 'fv_09', 'fv_10',
                'fv_11', 'fv_12', 'fv_13', 'fv_14', 'fv_15',
                'fv_16', 'fv_17', 'fv_18', 'fv_19', 'fv_20',
                'fv_21', 'fv_22', 'fv_23', 'fv_24', 'fv_25',
                'fv_26', 'fv_27', 'fv_28', 'fv_29', 'fv_30',
                'fv_31', 'fv_32', 'fv_33', 'fv_34', 'fv_35',
                'fv_36', 'fv_37', 'fv_38', 'fv_39', 'fv_40',
                'fv_41', 'fv_42', 'fv_43', 'fv_44', 'fv_45',
                'fv_46', 'fv_47', 'fv_48', 'fv_49', 'fv_50',
                'fv_51', 'fv_52', 'fv_53', 'fv_54', 'fv_55',
                'fv_56', 'fv_57', 'fv_58', 'fv_59', 'fv_60',
                'fv_61', 'fv_62', 'fv_63', 'fv_64', 'fv_65',
                'fv_66', 'fv_67', 'fv_68', 'fv_69', 'fv_70',
                'fv_71', 'fv_72', 'fv_73', 'fv_74', 'fv_75',
                'fv_76', 'fv_77', 'fv_78', 'fv_79', 'fv_80'],
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
                _('This section fields key is not valid') + ' ' + fsection)
        elif fsection:
            return fields_section.get(fsection)
        else:
            return fields_section

    @api.multi
    def clear(self):
        """
        Clear all the fields.
        """
        dtype = self._context.get('dtype', False)
        if not dtype:
            raise UserError(_('Indicate what you want to delete'))

        fields_section = self.fields_section()
        if dtype not in fields_section:
            raise UserError(_('There is not groups of fields defined'))

        self._clear_method(fields_section[dtype])
        return True

    @api.multi
    def _clear_method(self, field_list):
        """
        Clean the method forecast values.
        """
        values = {}.fromkeys(field_list, 0.0)
        self.write(values)

    @api.depends()
    def _compute_cummulative_move_average(self):
        """
        CUMULATIVE MOVING AVERAGE
        Note: Represente function compute1
        """
        fv_list = self.get_forecasting_values()
        if not fv_list:
            return True
        numv = len(fv_list)
        period = self.period
        avg = [None for item in range(period)]
        ma_error = []
        for item in range(period, numv+1):
            fv_set = fv_list[item-period:item]
            avg += [sum(fv_set) / float(period)]
            ma_error += [abs(avg[-1] - fv_set[-1])]
        self.cma_forecast = avg[-1]
        ma_error = sum(ma_error)/len(ma_error)
        self.cma_ma_error = ma_error
        return True

    @api.depends()
    def _compute_simple_move_average(self):
        """
        SIMPLE MOVING AVERAGE
        Note: Represente function compute1
        """
        fv_list = self.get_forecasting_values()
        if not fv_list:
            return True
        numv = len(fv_list)
        period = self.period
        avg = [None for item in range(period)]
        ma_error = []
        for item in range(period+1, numv+1):
            fv_set = fv_list[item-period-1:item-1]
            avg += [sum(fv_set) / float(period)]
            ma_error += [abs(avg[-1] - fv_list[item-1])]
        self.sma_forecast = avg[-1]
        ma_error = sum(ma_error)/len(ma_error)
        self.sma_ma_error = ma_error
        return True

    @api.multi
    def get_forecasting_values(self):
        """
        This method will return the forecast input values in a list.
        """
        fv_set = []
        field_list = self.fields_section('data')
        values = self.read(field_list)[0]
        for fname in field_list:
            val = values.get(fname)
            if val:
                fv_set.append(val)
        return fv_set

    @api.multi
    def set_test_forecast_values(self):
        """
        This method will return the forecast input values in a list.
        """
        val = 1
        for item in range(1, 81):
            fvfield = 'fv_{num:02d}'.format(num=item)
            setattr(self, fvfield, val)
            if val == 30:
                val = 1
            else:
                val += 1
        return True

    @api.depends()
    def _compute_weighted_move_average(self):
        """
        WEIGHTED MOVING AVERAGE
        Note: Represente function compute3
        """
        fv_list = self.get_forecasting_values()
        if not fv_list:
            return True
        numv = len(fv_list)
        period = self.period
        fperiod = float(period)
        avg = [None for item in range(4)]
        ma_error = []
        weight = (fperiod * (fperiod + 1.0)) / 2.0
        for item in range(period, numv+1):
            fv_set = fv_list[item-period:item]
            if len(fv_set) < period:
                break
            avg += [sum(
                [((day) / weight) * value
                 for (day, value) in enumerate(fv_set, 1)])]
            ma_error += [abs(avg[-1] - fv_set[-1])]
        self.wma_forecast = avg[-1]
        ma_error = sum(ma_error)/(float(len(ma_error)))
        self.wma_ma_error = ma_error
        return True

    @api.depends()
    def _compute_exp_smoothing(self):
        """
        Single, Double, & Triple Exponential Smoothing
        Note: Represente function compute3
        """
        # TODO check. this method do not use period at all.
        fv_list = self.get_forecasting_values()
        if not fv_list:
            return True
        numv = len(fv_list)
        alpha = self.exp_alpha
        st1 = [fv_list[1]]
        st2 = [fv_list[1]]
        st3 = [fv_list[1]]

        for value in range(1, numv):
            st1.append(alpha * fv_list[value] + (1.0 - alpha) * st1[value-1])
            st2.append(alpha * st1[value] + (1.0 - alpha) * st2[value-1])
            st3.append(alpha * st2[value] + (1.0 - alpha) * st3[value-1])

        a2 = 2.0 * st1[numv-1] - st2[numv-1]
        b2 = (alpha/(1.0-alpha)) * (st1[numv-1] - st2[numv-1])
        a3 = 3.0 * st1[numv-1] - 3.0 * st2[numv-1] + st3[numv-1]
        b3 = ((alpha/(2.0 * pow(1.0-alpha, 2.0))) * (
            (6.0 - 5.0 * alpha) * st1[numv-1] -
            (10.0 - 8.0 * alpha) * st2[numv-1] +
            (4.0 - 3.0 * alpha) * st3[numv-1]))
        c3 = (pow((alpha/(1.0 - alpha)), 2.0) *
              (st1[numv-1] - 2.0 * st2[numv-1] + st3[numv-1]))

        self.single_forecast = st1[-1]
        self.double_forecast = a2 + b2
        self.triple_forecast = a3 + b3 + 0.5 * c3

        st1_ma_error = 0.0
        st2_ma_error = 0.0
        st3_ma_error = 0.0

        for value in range(0, numv):
            st1_ma_error += abs((st1[value] - fv_list[value]))
            st2_ma_error += abs((st2[value] - fv_list[value]))
            st3_ma_error += abs((st3[value] - fv_list[value]))

        self.single_ma_error = st1_ma_error / float(numv)
        self.double_ma_error = st2_ma_error / float(numv)
        self.triple_ma_error = st3_ma_error / float(numv)
        return True

    @api.depends()
    def _compute_holt(self):
        """
        Holt's Linear Smoothing
        Note: Represente function compute20
        """
        fv_list = self.get_forecasting_values()
        if not fv_list:
            return True
        numv = len(fv_list)
        alpha = self.holt_alpha
        beta = self.beta
        period = self.holt_period

        level = [None]
        trend = [None]
        func = [None, None]

        level.append(fv_list[1])
        trend.append(fv_list[1] - fv_list[0])
        func.append(level[-1] + trend[-1])

        for item in range(2, numv):
            level.append(alpha * fv_list[item] + (1.0 - alpha) * func[item])
            trend.append((beta * (level[item] - level[item-1])
                          + (1.0 - beta) * trend[item-1]))
            func.append(level[item] + trend[item])

        self.holt_forecast = level[-1] + period * trend[-1]
        ma_error = 0.0
        for item in range(3, numv):
            ma_error += abs(func[item] - fv_list[item])
        self.holt_ma_error = ma_error / (float(numv) - 3.0)
        return True
