=============
Installation
=============

Only with Python/django
========================

Install with:

.. code-block:: bash
   :linenos:

    pip3 install django-partitialajax

Than put partitialajax into your INSTALLED_APPS:


.. code-block:: python
   :linenos:

    INSTALLED_APPS = [
    ...
        partitialajax
    ]

Add the JS libary to each page you have Partitials:


.. code-block:: html
   :linenos:

    ...
    {% static 'partitialajax/index.js' %}
    </head>
    ...

JS / Python Setup
=================

You can also use the js src to build your own javascript set for every page

Install with

.. code-block:: bash
   :linenos:

    pip3 install django-partitialajax
    npm install django-partitialajax --save

Tipp: If you use webpack for your js code use the django-webpack-loader libary.

To use the "autodiscover" for elements with partitial loading use the following JS code:

.. code-block:: js
   :lineos:

   import PartitialAjax from "django-partitialajax";

   PartitialAjax.initialize();



General Setup
====================

You can define a partitial without a line of your own js code:

.. code-block:: html
   :linenos:

    {% load partitialajax %}

    {% direct_partitial ".content" %}

All options, see: :ref:`partitial-ajax-options` can be set as element Attribute:


.. code-block:: html
   :linenos:

    {% load partitialajax %}

    {% direct_partitial ".content" url:"remotepath" %}

