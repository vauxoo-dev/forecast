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

from openerp.tools.safe_eval import safe_eval
from openerp.exceptions import ValidationError
from openerp.tests import common


class TestForecastingRules(common.TransactionCase):

    """
    Test that the forecasting rules model is working propertly.

    For the current test the res.partner model will be use as the forecasting
    rule model. Bellow information about some res.partner fields that will be
    used (type, list of fields, module defined):

        int:
            id
        float:
            credit_limit (base module)
            debilt_limit
            credit       (account module)
            debit        (account module)
        date:
            date
        datetime:
            last_reconciliation_data

    As forecast_value we are goin to use the credit_limit float field. This
    field is add in the base module but is show in the partner in the account
    module so will not be show in the partner form view.

    So far some partners already have a credit_limit value set in demo:

        [{'credit_limit': 15000.0, 'id': 19, 'name': u'Chamber Works'},
        {'credit_limit': 15000.0, 'id': 58, 'name': u'Angel Cook'},
        {'credit_limit': 15000.0, 'id': 59, 'name': u'Robert Anderson'},
        {'credit_limit': 1500.0, 'id': 60, 'name': u'Jacob Taylor'},
        {'credit_limit': 1500.0, 'id': 20, 'name': u'Millennium Industries'}
        ]
    """

    def setUp(self):
        super(TestForecastingRules, self).setUp()

        # Save in test the basic objects
        self.rule_obj = self.env['forecasting.rule']
        self.irfilter_obj = self.env['ir.filters']
        self.forecast_obj = self.env['forecast']

        # Get the data demo
        self.forecast = self.forecast_obj.browse(
            self.ref('forecasting_rules.forecast_demo_01'))
        self.rule = self.rule_obj.browse(self.ref(
            'forecasting_rules.forecast_rule_demo_01'))
        self.irfilter = self.irfilter_obj.browse(self.ref(
            'forecasting_rules.filter_demo_01'))
        self.partner_model = self.ref('base.model_res_partner')

        # First ensure that the filter to test correspond to the rule used
        # in this test.
        self.assertEqual(self.rule.filter_id, self.irfilter)

        # Second, ensure that the rule is related to the forecast test record.
        self.assertEqual(self.forecast.rule_id, self.rule)

    def create_rule(self, name='All Partners', model='res.partner',
                    wo_irfilter=False):
        """
        Create a ir filter with the specificated arguments

        :name: name of the ir.filter to create
        :model: model name to use in the ir.filter

        :return: recordset with the record create
        """
        values = {
            'name': ' Partner Credit Limit (Test %s)' % name,
            'model': model,
            'filter_id': self.irfilter.id,
        }
        if wo_irfilter:
            values.pop('filter_id')
        rule = self.rule_obj.create(values)
        return rule

    def test_01(self):
        """Basic CRUD
        """
        # Test Create (With Basic Values)
        rule = self.create_rule()
        self.assertTrue(rule)

        # Test Read (via recorset)
        rule_name = False
        rule_name = rule.name
        self.assertTrue(rule_name)

        # Test Read (via orm read())
        rule_dict = rule.read()[0]
        self.assertTrue(isinstance(rule_dict, (dict,)))

        # Test Write
        new_name = rule_name + ' [Rename in python unit test]'
        rule.name = new_name
        self.assertEqual(rule.name, new_name)

        # Test Duplicate
        rule2 = rule.copy()
        self.assertTrue(rule2)

    def test_02(self):
        """Constraint: Require a filter when a forecast is set.
        """
        # Create a new rule with forecast related but without a filter
        error_msg = (
            ' Missing Rule Filter: The current forecast rule have'
            ' not filter defined so can not generate the forecast values.')

        # Create a forecast with a rule without a filter.
        rule = self.create_rule(name='2', wo_irfilter=True)
        forecast = self.forecast_obj.create({
            'name': 'Constraint Rule - Forecast (Test 02)'})
        forecast.rule_id = rule.id

        with self.assertRaisesRegexp(ValidationError, error_msg):
            forecast.fill_value_ids()

    def test_03(self):
        """Constraint: Rule filter context without the required keys

        Remove context required key over an existing forecasting rule filter.
        The required keys are forecast_order and forecast_rule.
        In all the cases must raise an error.
        """
        # Remove forecast_order key
        context = safe_eval(self.rule.filter_id.context)
        with self.assertRaises(ValidationError):
            context.pop('forecast_order')
            self.rule.filter_id.context = str(context)

        # Remove forecast_value key
        context = safe_eval(self.rule.filter_id.context)
        with self.assertRaises(ValidationError):
            context.pop('forecast_value')
            self.rule.filter_id.context = str(context)

    def test_04(self):
        """Constraint: rule filter context forecast_value is not a valid field.
        """
        context = safe_eval(self.irfilter.context)

        # Use a not exist order field
        with self.assertRaises(ValidationError):
            context.update(forecast_order='nonexist_field')
            self.rule.filter_id.context = str(context)

        # Use a not exist value field
        with self.assertRaises(ValidationError):
            context.update(forecast_value='nonexist_field')
            self.rule.filter_id.context = str(context)

    def test_07(self):
        """Constraint: Required same ir_filter/rule model (both side check)
        """
        self.assertEqual(self.irfilter.model_id, self.rule.model)

        # Try to change the filter model
        error = 'filter/rule model do not match'
        with self.assertRaisesRegexp(ValidationError, error):
            self.irfilter.model_id = 'res.users'

        # Try to change the rule model
        error = 'The rule model and filter model must be the same model'
        with self.assertRaisesRegexp(ValidationError, error):
            self.rule.model = 'res.groups'

    def _test_XX(self):
        """Security: check groups permissions
        """
        self.user_obj = self.env['res.users']
        # TODO: make this test (not priority)
        # self.user_obj.create
        # forecast_user
        # forecast_manager
        # rule_user
        # rule_manager
