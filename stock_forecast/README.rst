.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Stock Forecast
==============

This module add a way to generate forecasting from the product demand.

**Features**:

- Integrate forecasting with products. Add button ``Forecasting`` in the
  product form view and add product field to the forecast record.
- Add wizard at ``Reporting > Warehouse > Stock Demand`` to calculate demand
  for a product in a specific location. Also can have a date margin to extract
  demand only in a certain group (required Forecast Manager permission).
- Add demo data so you can check how the product demand forecast works. You
  can go to ``Settings > Technical > Forecasting > Forecast`` and select the
  forecast with the prefix ``(ST Test 01)``.

Installation
============

To install this module, you need to:

- Not special pre-installation is required, just install as a regular odoo
  module:

  - Download this module from `Vauxoo/forecast
    <https://github.com/vauxoo/forecast>`_
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

* Once in the forecast form view you can check that is associated to what
  product in the section ``Done for product``.

  .. image:: forecast_buttons.png
     :alt: Forecast Buttons

Known issues / Roadmap
======================

Bug Tracker
===========

Bugs are tracked on
`GitHub Issues <https://github.com/Vauxoo/forecast/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and
welcomed feedback
`here <https://github.com/Vauxoo/forecast/issues/new?body=module:%20
stock_forecast%0Aversion:%20
8.0.1.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_

TODO
====

- Maybe the display_name field and compute method can be defined in the
  forecasting_smoothing_techniques module and overwrite in every forecast
  module.
- Stock picking data demo:

  - Make that data demo is generated dynamically in the last 3 months from the
    date that the database is created.
  - Add more entries to have at least 9 values for every product/location.
  - Evaluate if is necessary to move the stock picking data demo to xml data.

Credits
=======

**Contributors**

* Nhomar Hernandez <nhomar@vauxoo.com> (Planner/Auditor)
* Katherine Zaoral <kathy@vauxoo.com> (Developer)

Maintainer
==========

.. image:: https://s3.amazonaws.com/s3.vauxoo.com/description_logo.png
   :alt: Vauxoo
   :target: https://www.vauxoo.com
   :width: 200

This module is maintained by the Vauxoo.

To contribute to this module, please visit https://www.vauxoo.com.
