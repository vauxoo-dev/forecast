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

from openerp import models, api, _
from openerp.exceptions import ValidationError
from openerp.tools.safe_eval import safe_eval


class IrFilters(models.Model):

    _inherit = 'ir.filters'

    @api.model
    def is_field(self, model_obj, value):
        """
        Check if a given name correspond as field in the given model.

        :model_obj: string with the name of the model
        :value: the name of the field that want to check.
        :return: True or False
        """
        if isinstance(value, (str,)):
            field_list = model_obj.fields_get().keys()
            if value in field_list:
                return True
        return False

    @api.model
    def process_context_value(self, model_obj, value):
        """
        Get the key in the context and return the way to process.

         - If value is a field into the model defined in the rule then will
           return a string with the field name
         - If value is not a field is suppost to be is a field into the model
           defined in the rule then will return a string with the field name

        If not a field then raise an error.

        :value: a string value extract from the context.
        :return: string with the field name to be execute
        """
        res = False
        value_type = False
        if self.is_field(model_obj, value):
            res = value
            value_type = 'field'
        else:
            raise ValidationError('\n'.join([
                _('Not valid context value.'), value,
                _(' is not a valid field in'), model_obj._name]))
        return res, value_type

    @api.multi
    def process_filter_data(self):
        """
        Read and pre-process the rule data (rule_id field) that will be use
        to fulfill the value_ids field.

        :return:
        """
        context = safe_eval(self.context)
        domain = safe_eval(self.domain)
        model_obj = self.env[self.model_id]
        group_by = context.get('group_by', False)

        # process order
        order = context.get('forecast_order')
        order, otype = self.process_context_value(model_obj, order)

        # process value
        value = context.get('forecast_value')
        value, vtype = self.process_context_value(model_obj, value)

        return model_obj, domain, order, value, group_by, vtype

    @api.multi
    def search_group(self, model_obj, domain, order, group_by, value):
        """
        Run a read_group field with the given argumetns and then return a
        procesed result to create the forecast.data records.

        NOTE: If the order and the groupby field are the same then need to make
        a validation over the type of the groupby. If the groupby is a
        compossed group like 'date:month', 'date:year', etc then the order
        field need to be the same compossed element. This is nedeed because in
        the result the order field will not be found and will return an error.

        :model_obj: model object where to do the searh
        :domain: the domain to apply to the search
        :order: the field used to order the retrieve elements.
        :group_by: how to group by the results
        :value: the field to extract from the result to use as value

        :return: a list of tuples od the form (0, 0, {}) with the basic data to
        create new forecasting data objects.
        """
        # process group_by info, return real group_by field
        group_info = group_by[0].split(':')
        if len(group_info) == 2:
            groupfield, subgroup = group_info
            if order == groupfield:
                order = group_by[0]
        data = model_obj.read_group(
            domain, [order, groupfield, value], group_by, orderby=order)
        value_ids = [
            (0, 0, dict(sequence=num,
                        label=item.get(group_by[0]),
                        value=item.get(value)))
            for (num, item) in enumerate(data, 1)]
        return value_ids

    @api.multi
    def special_search(self):
        """
        Read and pre-process the filter data and then peform the search

        :return: a list with the dictionary need to fill the forecast data
                 values. keys = ['sequence', 'label', 'value']
        """
        value_ids = []
        (model_obj, domain, order, value, group_by, value_type) = \
            self.process_filter_data()

        if value_type == 'field':
            if group_by:
                value_ids = self.search_group(
                    model_obj, domain, order, group_by, value)
            else:
                data = model_obj.search(domain, order=order)
                value_ids = [
                    (0, 0, dict(sequence=num, label=getattr(item, order),
                                value=getattr(item, value)))
                    for (num, item) in enumerate(data, 1)]
        else:
            raise ValidationError(_('Development error'))
        return value_ids

    @api.multi
    def get_related_rules(self):
        """
        :return: the recordset list of related rules
        """
        rule_obj = self.env['forecasting.rule']
        return rule_obj.search([('filter_id', 'in', self.ids)])

    @api.constrains('context')
    def _check_context(self):
        """
        Check context introduce by user is valid, for that:

            - Check context is a valid python expression
            - Check context is a dictionary
            - Check context have ['forecast_order', 'forecast_value'] keys
            - Check context ['forecast_order', 'forecast_value'] keys are valid

        """
        error = _('The context value you introduce is not a valid context')
        related_rules = self.get_related_rules()
        if related_rules:

            # Check context is a valid python expression
            try:
                context = safe_eval(self.context)
            except:
                msg = _('Context is not a valid python expression')
                raise ValidationError('\n'.join([error, msg, self.context]))

            # Check context is a dictionary
            if not isinstance(context, (dict,)):
                msg = _('Context must be a dictionary')
                raise ValidationError('\n'.join([error, msg, self.context]))

            # Check context have ['forecast_order', 'forecast_value'] keys
            missing_key_error = str()
            for nkey in ['forecast_order', 'forecast_value']:
                if nkey not in context.keys():
                    missing_key_error += _(
                        " - The {context_key} key must exist in the filter"
                        " record to be use as forcasting rule.\n").format(
                            context_key=nkey)
            if missing_key_error:
                raise ValidationError('\n'.join([error, missing_key_error,
                                                 self.context]))

            # Check context ['forecast_order', 'forecast_value'] keys are valid
            self.process_filter_data()

    @api.constrains('domain')
    def _check_domain(self):
        """ Check that the domain is valid:

            - Check domain is a python expression
            - Check domain is a list of tuples
        """
        error = _('The domain value you introduce is not a valid domain')
        related_rules = self.get_related_rules()
        if related_rules:

            # Check domain is a valid python expression
            try:
                domain = safe_eval(self.domain)
            except:
                msg = _('Domain is not a valid python expression')
                raise ValidationError('\n'.join([error, msg, self.domain]))

            # Check domain is a list of tuples
            if not isinstance(domain, (list,)):
                msg = _('Domain must be a list')
                raise ValidationError('\n'.join([error, msg, self.domain]))
            else:
                list_item_type = set([type(item) for item in domain])
                if not list_item_type == set([type(tuple())]):
                    msg = _('Domain must be a list of tuples')
                    raise ValidationError('\n'.join([error, msg, self.domain]))

    @api.constrains('model_id')
    def _check_model_id(self):
        """
        Check that the model_id introduce by the user is the same of the
        forecasting rule related

            - Check if model exists
            - Check if the filter/rule model match
        """
        related_rules = self.get_related_rules()
        error = _('Not valid model')
        if related_rules:

            # Check if model exists
            model = self.env['ir.model'].search(
                [('model', '=', self.model_id)])
            if not model:
                msg = _('Model do not exists in the database')
                raise ValidationError('\n'.join([error, msg, self.model_id]))

            # Check if the filter/rule model match
            diff_model_rules = related_rules.filtered(
                lambda rule: rule.model != self.model_id)
            if diff_model_rules:
                diff_msg = _(
                    ' - This filter have related forecast.rule "{rule}"'
                    ' and the filter/rule model do not match.'
                    ' (rule) {rule_model} != (filter) {filter_model}')
                msg = '/n'.join([diff_msg.format(rule=rule.display_name,
                                                 rule_model=rule.model,
                                                 filter_model=self.model_id)
                                 for rule in diff_model_rules])
                raise ValidationError('\n'.join([error, self.model_id, msg]))
