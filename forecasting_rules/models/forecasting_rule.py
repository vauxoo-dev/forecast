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

from openerp import fields, models, api, _
from openerp.exceptions import ValidationError


class ForecastingRule(models.Model):

    _name = 'forecasting.rule'
    _description = 'Forecasting Rule'

    name = fields.Char(requrired=True,
                       help='Name to identificate the Forecasting Rule')
    model = fields.Char(help='Model were this forecasting apply')
    filter_id = fields.Many2one(
        'ir.filters',
        string='Filter',
        help='Filter that indicate what values are going to be extract'
             ' for the forecast')

    # TODO review is the forecast_id field is really neccesary.
    forecast_id = fields.Many2one(
        'forecasting.smoothing.techniques',
        string='Forecast',
        help='Forecast where this Rule is used')

    display_name = fields.Char(
        string='Name', compute='_compute_display_name')

    @api.one
    @api.depends('name')
    def _compute_display_name(self):
        names = [str(self.id), self.name]
        self.display_name = ' '.join(names)

    # TODO: evaluate. this method could be change to a filter_id contraint and
    # check if there is any forecast related to the current rule.
    @api.constrains('forecast_id')
    def _check_forecast_id(self):
        """
        If the rule have a forecast related need to have a filter also.
        Raise a ValidationError when this condition do not fulfill.
        """
        if self.forecast_id and not self.filter_id:
            raise ValidationError(_(
                ' Missing Rule Filter: The Forecast Rule you related to'
                ' the forecast need to have a filter defined to filter'
                ' the forecast values.'))

    @api.constrains('model', 'filter_id')
    def _check_model_id(self):
        """
        Check that the model introduce by the user is the same of the
        irfilter model
        """
        if self.filter_id:
            model = self.model
            irfilter_model = self.filter_id.model_id
            error = str()
            if model != irfilter_model:
                error += _(
                    " - The rule model and filter model must be the same model"
                    " rule {rule_model} != filter {filter_model}").format(
                        rule_model=model,
                        filter_model=irfilter_model,
                    )
            if error:
                raise ValidationError(error)
