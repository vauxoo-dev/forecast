.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
    :alt: License: LGPL-3

Validate Filters
================

This module extend the review of the if.filter records.
Will check if the context, domain and model fields are valid one, if not will
raise the correspond message error.

Installation
============

To install this module, you need to:

- There is not extra requirement needed, you only need to install the odoo
  module like a regular module:

  - Download this module from `Vauxoo/forecast <https://github.com/vauxoo/forecast>`_ repository.
  - Add the repository folder into your odoo addons-path and reload you odoo
    server.
  - Go to ``Settings > Module list`` search for the current name and click
    ``Install`` button.

Configuration
=============

There is not configuration needed. Just start working in you ir.filters.

Usage
=====

* When try to update a ``ir.filter`` record will validate its fields:

  - Check context is a valid python expression
  - Check context is a dictionary
  - Check domain is a python expression
  - Check domain is a list of tuples
  - Check if model exists

Known issues / Roadmap
======================

* There is not known issues.

TODO
====

- Check if the context value is a valid field. The check method is already
  added but not used yet.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/Vauxoo/forecast/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/Vauxoo/forecast/issues/new?body=module:%20{ir_filter_validate}%0Aversion:%20{8.0.1.0.0}%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_

Credits
=======

Contributors
------------

* Nhomar Hernandez <nhomar@vauxoo.com> (Planner/Auditor)
* Katherine Zaoral <kathy@vauxoo.com> (Planner/Developer)

Maintainer
----------

.. image:: https://s3.amazonaws.com/s3.vauxoo.com/description_logo.png
   :alt: Vauxoo
   :target: https://www.vauxoo.com
   :width: 200

This module is maintained by the Vauxoo.

To contribute to this module, please visit https://www.vauxoo.com.
