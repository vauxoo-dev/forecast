.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Stock Forecast
==============

This module add the components to integrate the forecasting with the product
records.

Installation
============

To install this module, you need to:

- Download this module from `Vauxoo/stock-forecasting <https://github.com/vauxoo/stock-forecasting>`_
- Add the repository folder into your odoo addons-path.
- Go to ``Settings > Module list`` search for the current name and click in
  ``Install`` button.

Configuration
=============

To configure this module, you need to:

* There is not special configuration for this module.

Usage
=====

To use this module, you need to:

* Go to a ``Product`` form view and click on the ``Forecasting``
  button at the top right of the form. There you can check or create a new
  forecasting for you selected product product.

  .. image:: product_button_forcast.png
     :alt: Forecasting button at the Product Form View

  .. image:: forecast_buttons.png
     :alt: Forecast Buttons

  In the first view of the forecasting form view you can view a graph with
  the results of all the forecasting methods applied over the data you
  sumbit.

* In a more complete view of all the forecasting form view you can review the
  total forecasting summary and the forecasting methods paramters to configure
  to run the forecasting. If you have any doubt there is an explanation about
  every forecasting methods so will be more easy to use.

.. image:: forecast_form_view.png
   :alt: Forecast Form View

* When editing the forecast values (Click over the ``List of Values`` button)
  you can observe all the values in the table with all the detail forecasting
  results per data point with the mathematical absolute error (MAE).

.. image:: forecast_data_tree_view.png
   :alt: Forecast Data List View

Known issues / Roadmap
======================

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/Vauxoo/stock-forecasting/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/Vauxoo/stock-forecasting/issues/new?body=module:%20{stock_forecast}%0Aversion:%20{8.0.1.0.0}%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_

TODO
====

- This module future can change its dependency from
  forecasting_smoothing_techniques module to forecasting_rules.
- Maybe the display_name field and compute method can be defined in the
  forecasting_smoothing_techniques module and overwrite in every forecast
  module.

credits
=======

Contributors
------------

* Nhomar Hernandez <nhomar@vauxoo.com> (Planner/Auditor)
* Katherine Zaoral <kathy@vauxoo.com> (Developer)

Maintainer
----------

.. image:: https://s3.amazonaws.com/s3.vauxoo.com/description_logo.png
   :alt: Vauxoo
   :target: https://www.vauxoo.com
   :width: 200

This module is maintained by the Vauxoo.

To contribute to this module, please visit https://www.vauxoo.com.
