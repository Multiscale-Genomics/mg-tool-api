HOWTO
=====

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   howto_tool
   howto_pipeline
   howto_config

The following is a walk through of developing a tool and pipeline wrapper to include new functionality within the MuG VRE. There are several stages covering the Tool development, using the tool within a pipeline and defining the configuration files required so that the final product can be smoothly integrated into the MuG VRE.

Common Coding Standards
-----------------------
When it comes to developing the code all the code should stick to a common standard. This has been defined within the `Coding Standards <http://multiscale-genomics.readthedocs.io/en/latest/coding_standards.html>`_ documentation as well as how to set up the licenses correctly so that your package can be integrated.

Adding a new function
---------------------

`Wrapping a Tool <howto_tool.html>`_
    This section guides you through how to wrap an external tool, or create a tool that utilises the pyCOMPSs framework and should be capable of running within the MuG VRE environment.

`Adding a tool to a pipeline <howto_pipeline.html>`_
    Once you have created a tool you can now one or multiple tools into a pipeline. This will handle the passing of variables from the VRE to the tool and the tracking of outputs ready for handing back to the VRE. This document will also help in creating test input metadata and file location JSON files that are required to run the pipeline.

`Configuration <howto_config.html>`_
    This takes you through creating JSON configuration files for your tool. This should define all the inputs, outputs and any arguments that are required by the pipelines and tools.