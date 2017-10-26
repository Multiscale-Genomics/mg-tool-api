HOWTO - Pipelines
=================

This document is a tutorial about creating pipelines that can be easily integrated into the MuG VRE. The aim of a pipeline is to bring together a number of tools (see `Creating a Tool <howto_tool.html>`_ ) and running them as part of a workflow for end to end processing of data.

Each pipeline consists of the main class for the pipeline, a main function for running the class and a section of global code to catch if the pipeline has been run from the command line. All functions should have full documentation describing the function, inputs and outputs. For details about the coding style please consult the `coding style documentation <http://multiscale-genomics.readthedocs.io/en/latest/coding_standards.html>`_.

Example Pipeline
----------------

This example code uses the testTool.py from the Creating a Tool tutorial.

There are 2 ways of calling this function, either directly from another program or via the command line.

.. code-block:: python
   :linenos:

   #!/usr/bin/env python

   """
   .. License and copyright agreement statement
   """
   from __future__ import print_function

   # Required for ReadTheDocs
   from functools import wraps # pylint: disable=unused-import

   import argparse

   from basic_modules.workflow import Workflow
   from basic_modules.metadata import Metadata

   from tools.testTool import testTool

   # ------------------------------------------------------------------------------

   class process_test(Workflow):
       """
       Functions for demonstrating the pipeline set up.
       """

       configuration = {}

       def __init__(self, configuration=None):
           """
           Initialise the tool with its configuration.

           Parameters
           ----------
           configuration : dict
               a dictionary containing parameters that define how the operation
               should be carried out, which are specific to each Tool.
           """

           if configuration is None:
               configuration = {}

           self.configuration.update(configuration)

       def run(self, input_files, metadata, output_files):
           """
           Main run function for processing a test file.

           Parameters
           ----------
           input_files : dict
               Dictionary of file locations
           metadata : list
               Required meta data
           output_files : dict
               Locations of the output files to be returned by the pipeline

           Returns
           -------
           output_files : dict
               Locations for the output txt
           output_metadata : dict
               Matching metadata for each of the files
           """

           # Initialise the test tool
           tt_handle = testTool(self.configuration)
           tt_files, tt_meta = tt_handle.run(input_files, metadata, output_files)

           return (
               tt_files,
               tt_meta
           )


   # ------------------------------------------------------------------------------

   def main_json(config, in_metadata, out_metadata):
       """
       Alternative main function
       -------------

       This function launches the app using configuration written in
       two json files: config.json and input_metadata.json.
       """
       # 1. Instantiate and launch the App
       print("1. Instantiate and launch the App")
       from apps.jsonapp import JSONApp
       app = JSONApp()
       result = app.launch(process_genome,
                           config,
                           in_metadata,
                           out_metadata)

       # 2. The App has finished
       print("2. Execution finished; see " + out_metadata)
       print(result)

       return result

   # ------------------------------------------------------------------------------

   if __name__ == "__main__":
       import sys
       sys._run_from_cmdl = True  # pylint: disable=protected-access

       # Set up the command line parameters
       PARSER = argparse.ArgumentParser(description="Index the genome file")
       PARSER.add_argument("--config", help="Configuration file")
       PARSER.add_argument("--in_metadata", help="Location of input metadata file")
       PARSER.add_argument("--out_metadata", help="Location of output metadata file")

       # Get the matching parameters from the command line
       ARGS = PARSER.parse_args()

       CONFIG = ARGS.config
       IN_METADATA = ARGS.in_metadata
       OUT_METADATA = ARGS.out_metadata

       RESULTS = main_json(CONFIG, IN_METADATA, OUT_METADATA)
       print(RESULTS)


Code Walk Through
-----------------
I'll step through each of the sections of the example code describing what is happening at each point.


Header
^^^^^^
This section defines the license and any modules that need to be loaded for the code to run correctly. As a bare minimum is shown in the example with the license, import of the Workflow and Metadata basic_tools and the Data Management (DM) API. Theoretically the pipeline does not have to call a tool, but for completeness this uses the Tool generated as part of the `HOWTO - Tools <howto_tool.html>`_ tutorial.


`def main_json()` and `__main__`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
These are the main entry points into the pipeline. Having both allows the pipeline to be run either locally or as part of a series of function calls within the VRE.

The `main_json()` function is the primary function of the script and is what initiates running the pipeline. It is from here that the VRE or locally run function will call to with any matching input file, defined output files (is required) and any necessary meta data.

At the bottom of the script the `__main__` is triggered when being run from the command line. It can take in parameters from the command line and pass them to the `main_json()` function. As the VRE is responsible for loading of files into the Data Management (DM) API, if files that are used locally are to be tracked then they should also be loaded into the DM API at this point. For clarity of creating a pipeline this has not been included within the example.

Once `main_json()` has been called it launches the `WorkflowApp()` with the name of the pipeline (`process_test` in this case) along with the input files, output files (if known) and relevant meta data for running the application.

`process_test` - `__init__`
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Instantiates the pipeline and passes on any configuration data to the WorkFlowApp.


`process_test` - `run`
^^^^^^^^^^^^^^^^^^^^^^^^^^^
This is a required function which is called by the `main_json()` function. It is responsible for orchestrating the flow of data within the pipeline. The run function ensures that the Tools are initiated correctly and are passed the correct variables. If there are multiple Tools in the pipeline each relying on the output from the previous then the `run()` function is responsible for handing the output files from one tool to the next. At this point the handling of files is managed by the pyCOMPSs API and files only become accessible from the final location once the `run()` function has returned to `main_json()`. If you require the output of a tool locally for launching the next then you need to stream the file out of compss, this can be done with the following snippet:

.. code-block:: python
   :linenos:

   if hasattr(sys, '_run_from_cmdl') is True:
       pass
   else:
       with compss_open(intermediate_file_in_compss, "rb") as f_in:
           with open(local_loc_for_file, "wb") as f_out:
               f_out.write(f_in.read())

This will only work within the COMPSS environment so you will need to test for how your code is getting run.


Running the Code
----------------
To run the code it needs a config.json file and an input_metadata.json file to provide the input.

config.json
^^^^^^^^^^^

Defines the configurations required for by the pipeline including parameters that need to be passed from the VRE submission form, file and the related metadata as well as the output files that need to be produced by the pipeline.

.. code-block:: none
   :linenos:

   {
       "input_files": [
           {
               "required": true,
               "allow_multiple": false,
               "name": "genome",
               "value": "<unique_file_id>"
           }
       ],
       "arguments": [
           {
               "name": "project",
               "value": "run001"
           },
           {
               "name": "description",
               "value": null
           }
       ],
       "output_files": [
           {
               "required": true,
               "allow_multiple": false,
               "name": "bwa_index",
               "file": {
                   "file_type": "TAR",
                   "meta_data": {
                       "visible": true,
                       "tool": "bwq_indexer",
                       "description": "Output"
                   },
                   "file_path": "tests/data/macs2.Human.GCA_000001405.22.fasta.bwa.tar.gz",
                   "data_type": "sequence_mapping_index_bwa",
                   "compressed": "gzip"
               }
           }
       ]
   }


input_file_metadata.json
^^^^^^^^^^^^^^^^^^^^^^^^

Lists the file location that are used as input. The configuration names should match those that are in the config.json file defined above.

.. code-block:: none
   :linenos:

   [
       {
           "_id": "<unique_file_id>",
           "data_type": "sequence_dna",
           "file_type": "FASTA",
           "file_path": "tests/data/macs2.Human.GCA_000001405.22.fasta",
           "compressed": 0,
           "sources": [],
           "creation_time": {
               "sec": 1503567524,
               "usec": 0
           },
           "taxon_id": "0",
           "meta_data": {
               "visible": true,
               "validated": 1,
               "assembly": "GCA_000001405.22"
           }
       }
   ]

Running the pipeline manually
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: none
   :linenos:

   python process_test.py --config config.json --in_metadata input_files.json --out_metadata output_metadata.json