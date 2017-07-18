Creating a pipeline
===================

This document is a tutorial about the creation of a pipeline that can be easily integrated into the MuG VRE. The aim of a pipeline is to bring together a number of tools (see Creating a Tool) and running them as part of a workflow for end to end processing of data.

Each pipeline consists of the main class for the pipeline, a main function for running the class and a section of global code to catch if the pipeline has been run from the command line. All functions should have full documentation describing the function, inputs and outputs. For details about the coding style please consult the coding style documentation.

Example Pipeline
----------------

This example code uses the testTool.py from the Creating a Tool tutorial.

There are 2 ways of calling this function, either directly via the command line. As this is an example piece of code the integration with the data management API (DM API) has not been implemented within the pipeline to keep the test script concise.

.. code-block:: python
   :linenos:

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

        def __init__(self, configuration):
            """
            Initialise the tool with its configuration.


            Parameters
            ----------
            configuration : dict
                a dictionary containing parameters that define how the operation
                should be carried out, which are specific to each Tool.
            """
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

        #2. Register the data with the DMP
        PARAMS = [[FILE_LOC], [], []]

        # 3. Instantiate and launch the App
        RESULTS = main(PARAMS[0], PARAMS[1], PARAMS[2])

        print(RESULTS)
        print(DM_HANDLER.get_files_by_user("test"))

