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

from openerp.tests import common
from openerp.exceptions import ValidationError


class TestIrFilters(common.TransactionCase):

    """
    Test that the ir.filters model validation work properly
    """

    def setUp(self):
        super(TestIrFilters, self).setUp()
        self.irfilter_obj = self.env['ir.filters']

    def create_filter(self, name='UNDEFINED', model_id='res.partner',
                      context='{}', domain='[]'):
        """
        Create a irfilter with the specified arguments

        :name: name of the ir.filter to create
        :model_id: model name to use in the ir.filter
        :context: context field in the ir.filter record
        :domain: domain field in the ir.filter record
        :link_rule: boolean that tell if you want to link or not the created
                    irfilter to a forecast rule

        :return: recordset with the record create
        """
        irfilter = self.irfilter_obj.create({
            'name': 'All Partner (Test %s)' % name,
            'model_id': model_id,
            'context': context,
            'domain': domain,
        })
        return irfilter

    def test_01(self):
        """Basic CRUD
        """
        # Test Create (W Basic Values)
        # NOTE: can not create a irfilter without the next list of values.
        irfilter_name = 'All Partners'
        irfilter = self.irfilter_obj.create({
            'name': irfilter_name,
            'model_id': 'res.partner',
            'context': '{}',
            'domain': '[]',
        })
        self.assertTrue(irfilter)

        # Test Read (via recorset)
        self.assertEquals(irfilter.name, irfilter_name)

        # Test Read (via orm read())
        irfilter_dict = irfilter.read()[0]
        self.assertTrue(isinstance(irfilter_dict, (dict,)))
        self.assertEquals(irfilter_dict.get('name', False), irfilter_name)

        # Test Write
        new_name = irfilter_name + ' [Rename in python unit test]'
        irfilter.name = new_name
        self.assertEqual(irfilter.name, new_name)

        # TODO Fix this test is falling.
        # # Test Duplicate
        # irfilter2 = irfilter.copy()
        # self.assertTrue(irfilter2)

    def test_02(self):
        """Create a filter with a invalid domain
        """
        irfilter = self.create_filter(name='3')
        error = 'The domain value you introduce is not a valid domain'
        invalid_domain = [
            'this is an error',
            '[this is an error]',
            '{}',
        ]

        for domain in invalid_domain:
            with self.assertRaisesRegexp(ValidationError, error):
                irfilter.domain = domain

    def test_03(self):
        """Create a filter with a invalid context
        """
        irfilter = self.create_filter(name='4')
        error = 'The context value you introduce is not a valid context'
        invalid_context = [
            'this is an error',
            '[]',
            '{value: bad}',
        ]
        for context in invalid_context:
            with self.assertRaisesRegexp(ValidationError, error):
                irfilter.context = context
