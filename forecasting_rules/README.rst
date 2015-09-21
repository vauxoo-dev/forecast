.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Forecasting Rules
=================

This module extend the forecasting functionality by adding a new model named
``Forecast Rule`` that it is a bridge to fulfill the forecast data with odoo
data.

Is expected in a future that this module will be the one that integrate the
forecasting results with the other odoo records that extract data from the
forecast.

Installation
============

To install this module, you need to:

- There is not extra requirement needed, you only need to install the odoo
  module like a regular module:

  - Download this module from `Vauxoo/stock-forecasting <https://github.com/vauxoo/stock-forecasting>`_ repository.
  - Add the repository folder into your odoo addons-path and reload you odoo
    server.
  - Go to ``Settings > Module list`` search for the current name and click 
    ``Install`` button.

Configuration
=============

You can find the Forecast Rules menu at ``Settings > Technical > Forecasting >
Forecasting Rules``.

.. image:: forecast_rule_menu.png
   :alt: Forecast Rule Menu

To access to the Forecast Rules you need to at least have Forecasting basic
permissions. To edit the Forecasting Rules you need to active a new group
permission named ``Forecast Rule Manager`` in the Forecasting category.

.. image:: forecast_rule_group.png
   :alt: Forecast Rule Group

Usage
=====

* This module let to determinate explicitly the way that the forecast data is
  filled. In the forecast form view you can see two new mutually exclusive
  fields:

  - ``Use Manual Data``: Forecast data is manually introduce by the user.
    This is possible by checking to True the new boolean field. To fill the
    forecast data just go to the ``List of values`` button and add/edit every
    forecast value.

    .. image:: forecast_form_manual.png
       :alt: Use Manual Forecast Data

  - ``Forecast Rule``: When the ``Use Manual Data`` is unset then the
    ``Forecast Rule`` field is shown. This last one give the parameters to
    extract odoo data. After add the rule record just click over the new
    button named ``Fill Values`` that will make the process to update the
    forecast data.

    .. image:: forecast_form_rule.png
       :alt: Forecast using a Forecast Rule

The Forecast Rule work this way: You need to define the odoo model where the
data will be extract and link an ``ir filter`` to indicate the context and
domain used to extract the data.

.. image:: forecast_rule_form.png
   :alt: Forecast Rule

The context will need two required keys ``['forecast_order',
'forecast_value']``: these keys will be used to know what float field and what
order the data will be extract. Also you can used ``'group_by'`` key in your
context to group the return data, but only one group_by element.

.. image:: forecast_ir_filter.png
   :alt: Forecast Filter Requirements

Known issues / Roadmap
======================

* There is not known issues.

TODO
====

- Add security unit test.
- Add a way to manage multiple group_by elements in the Forecast Filter.
- Separate the context of validate the ir.filter into a new generic module.
- Change the model field in the forecasting.rule module from string to related
  field pointing to ir.filter model.
- Try to integrate a way to make the search group_by using pandas.
- Change the forecasting.rule model to forecast.rule.
- Review the spanish translations terms.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/Vauxoo/stock-forecasting/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/Vauxoo/stock-forecasting/issues/new?body=module:%20{forecasting_rules}%0Aversion:%20{8.0.1.0.0}%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_

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
