HOWTO - Pipelines
=================

This document is a tutorial about the creation of a pipeline that can be easily integrated into the MuG VRE. The aim of a pipeline is to bring together a number of tools (see Creating a Tool) and running them as part of a workflow for end to end processing of data.

Each pipeline consists of the main class for the pipeline, a main function for running the class and a section of global code to catch if the pipeline has been run from the command line. All functions should have full documentation describing the function, inputs and outputs. For details about the coding style please consult the coding style documentation.

Example Pipeline
----------------

This example code uses the testTool.py from the Creating a Tool tutorial.

There are 2 ways of calling this function, either directly via the command line. As this is an example piece of code the integration with the data management API (DM API) has not been implemented within the pipeline to keep the test script concise.

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

   from dmp import dmp

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

       def run(self, file_ids, output_files, metadata):
           """
           Main run function for processing a test file.

           Parameters
           ----------
           files_ids : list
               List of file locations
           metadata : list
               Required meta data
           output_files : list
               List of output file locations

           Returns
           -------
           outputfiles : list
               List of locations for the output txt
           """

           file_loc = file_ids[6]

           # Initialise the test tool
           tt_handle = testTool(self.configuration)
           results = tt_handle.run([file_loc], [])

           return (
               results[0],
               []
           )


   # ------------------------------------------------------------------------------

   def main(input_files, output_files, input_metadata):
       """
       Main function
       -------------

       This function launches the app.
       """

       # import pprint  # Pretty print - module for dictionary fancy printing

       # 1. Instantiate and launch the App
       print("1. Instantiate and launch the App")
       from apps.workflowapp import WorkflowApp
       app = WorkflowApp()
       result = app.launch(process_test, input_files, output_files, input_metadata,
                           {})

       # 2. The App has finished
       print("2. Execution finished")
       print(result)
       return result

   # ------------------------------------------------------------------------------

   if __name__ == "__main__":
       # Set up the command line parameters
       PARSER = argparse.ArgumentParser(description="Test pipeline")
       PARSER.add_argument("--file", help="Location of test input file")

       # Get the matching parameters from the command line
       ARGS = PARSER.parse_args()

       FILE_LOC = ARGS.file

       #
       # MuG Tool Steps
       # --------------
       #
       # 1. Create data files
       DM_HANDLER = dmp(test=True)

       # Add FILE_LOC to the DM_HANDLER

       #2. Register the data with the DMP
       PARAMS = [[FILE_LOC], [], []]

       # 3. Instantiate and launch the App
       RESULTS = main(PARAMS[0], PARAMS[1], PARAMS[2])

       print(RESULTS)
       print(DM_HANDLER.get_files_by_user("test"))


Code Walk Through
-----------------
I'll step through each of the sections of the example code describing what is happening at each point.


Header
^^^^^^
This section defines the license and any modules that need to be loaded for the code to run correctly. As a bare minimum is shown in the example with the license, import of the Workflow and Metadata basic_tools and the Data Management (DM) API. Theoretically the pipeline does not have to call a tool, but for completeness this uses the Tool generated as part of the `HOWTO - Tools`_ tutorial.


`def main()` and `__main__`
^^^^^^^^^^^^^^^^^^^^^^^^^^^
These are the main entry points into the pipeline. Having both allows the pipeline to be run either locally or as part of a series of function calls within the VRE.

The `main()` function is the primary function of the script and is what initiates running the pipeline. It is from here that the VRE or locally run function will call to with any matching input file, defined output files (is required) and any necessary meta data.

At the bottom of the script the `__main__` is triggered when being run from the command line. It can take in parameters from the command line and pass them to the `main()` function. As the VRE is responsible for loading of files into the Data Management (DM) API, if files that are used locally are to be tracked then they should also be loaded into the DM API at this point. For clarity of creating a pipeline this has not been included within the example.

Once main has been called it launches the WorkflowApp() with the name of the pipeline (process_test in this case) along with the input files, output files (if known) and relevant meta data for running the application.

`process_test` - `__init__`
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Instantiates the pipeline and passes on any configuration data to the WorkFlowApp.


`process_test` - `run`
^^^^^^^^^^^^^^^^^^^^^^^^^^^
This is a required function which is called by the `main()` function. It is responsible for orchestrating the flow of data within the pipeline. The run function ensures that the Tools are initiated correctly and are passed the correct variables. If there are multiple Tools in the pipeline each relying on the output from the previous then the `run()` function is responsible for handing the output files from one tool to the next. At this point the handling of files is managed by the pyCOMPSs API and files only become accessible from the final location once the `run()` function has returned to `main()`. This means that testing for a files existence can cause the pipeline to break.