.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Forecasting by Smoothing Techniques
===================================

Data collected over time is likely to show some form of random variation.
"Smoothing techniques" can be used to reduce or cancel the effect of these
variations. These techniques, when properly applied, will ``smooth`` out the
random variation in the time series data to reveal any underlying trends that
may exist.

**NOTE**: This module add a calculator to odoo that simulate the application in
`this link <http://home.ubalt.edu/ntsbarsh/Business-stat/otherapplets/ForecaSmo.htm>`_

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

* Go to a ``Products`` form view and click on the ``Forecasting``
  button at the top right of the form. There you can check or create a new
  forecasting. Forecasting list view show you a result summary ``ID`` and
  ``name`` and a forecasting parameters and resultis summary.

  .. image:: forecast_tree_view.png
     :alt: Forecast List View

* When click over a Forecasting record o over the ``Create`` button will take
  you to the Forecasting Form View. This view show up at the top the basic
  forecast data and some buttons:

  - ``Reset Details``: Reset the default parameters of the forecasting.
  - ``Clear``: Clear the forecasting incomming data values.
  - ``List of Values``: Go to the list of the forecating incomming data so
    you can edit them. Also you can see a table with all the forecasting
    results per data point (detail results).

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

* To edit the list of values just click over the value in the forecasting data
  list view to go tothe form view and edit the values. You can edit the
  Sequence and the Value itself indicating in the ``Data Information``
  section. As you can check all the ``Forecaasting Results`` for this
  particular point can be also review in the form view, this results fields
  are not editable only readonly.

.. image:: forecast_data_form_view.png
   :alt: Forecasr Data Form View

For further information, please visit:

* https://www.odoo.com/forum/help-1

Known issues / Roadmap
======================

* There is not known issues.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/Vauxoo/stock-forecasting/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/Vauxoo/stock-forecasting/issues/new?body=module:%20{forecasting_smoothing_techniques}%0Aversion:%20{8.0.1.0.0}%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_

Credits
=======

Contributors
------------

* Nhomar Hernandez <nhomar@vauxoo.com> (Planner/Auditor)
* Maria Gabriela Quilarque <gabriela@vauxoo.com> (Planner)
* Katherine Zaoral <kathy@vauxoo.com> (Developer)

Maintainer
----------

.. image:: https://s3.amazonaws.com/s3.vauxoo.com/description_logo.png
   :alt: Vauxoo
   :target: https://www.vauxoo.com
   :width: 200

This module is maintained by the Vauxoo.

To contribute to this module, please visit https://www.vauxoo.com.
