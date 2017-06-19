Requirements and Installation
=============================

Requirements
------------

Software
^^^^^^^^

- Python 2.7.10+

Python Modules
^^^^^^^^^^^^^^

- pytest

Installation
------------

Directly from GitHub:

.. code-block:: none
   :linenos:

   git clone https://github.com/Multiscale-Genomics/mg-tool-api.git

Using pip:

.. code-block:: none
   :linenos:

   pip install git+https://github.com/Multiscale-Genomics/mg-tool-api.git


Documentation
-------------

To build the documentation:

.. code-block:: none
   :linenos:

   pip install Sphinx
   pip install sphinx-autobuild
   cd docs
   make html
