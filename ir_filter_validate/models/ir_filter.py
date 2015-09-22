# -*- coding: utf-8 -*-
############################################################################
#    Module Writen For Odoo, Open Source Management Solution
#
#    Copyright (c) 2011 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#    coded by: Katherine Zaoral <kathy@vauxoo.com>
#    planned by: Katherine Zaoral <kathy@vauxoo.com>
#                Nhomar Hernandez <nhomar@vauxoo.com>
############################################################################

from openerp import models, api, _
from openerp.exceptions import ValidationError
from openerp.tools.safe_eval import safe_eval


class IrFilters(models.Model):

    _inherit = 'ir.filters'


    @api.constrains('context')
    def _check_context(self):
        """
        Check context introduce by user is valid, for that:

            - Check context is a valid python expression
            - Check context is a dictionary
        """
        error = _('The context value you introduce is not a valid context')

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

    @api.constrains('domain')
    def _check_domain(self):
        """ Check that the domain is valid:
            - Check domain is a python expression
            - Check domain is a list of tuples
        """
        error = _('The domain value you introduce is not a valid domain')

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
            if domain:
                list_item_type = set([type(item) for item in domain])
                if not list_item_type == set([type(tuple())]):
                    msg = _('Domain must be a list of tuples')
                    raise ValidationError('\n'.join([error, msg, self.domain]))