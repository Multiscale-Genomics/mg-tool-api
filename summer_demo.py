#!/usr/bin/env python
"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from __future__ import print_function

from mg_tool_api.basic_modules.metadata import Metadata
from mg_tool_api.basic_modules.workflow import Workflow
from mg_tool_api.utils import remap
from mg_tool_api.utils import logger
from tools_demos.simpleTool1 import SimpleTool1
from tools_demos.simpleTool2 import SimpleTool2


class SimpleWorkflow(Workflow):  # pylint: disable=too-few-public-methods
    """
    Simple example of Workflow using PyCOMPSs, called using an App.

    - SimpleTool1:
      reads an integer from a file, increments it, and writes it to file
    - SimpleTool2:
      reads two integers from two file and writes their sum to file
    - SimpleWorkflow:
      implements the following workflow:

          1           2
          |           |
     SimpleTool1  SimpleTool1
          |           |
          +-----.-----+
                |
           SimpleTool2
                |
                3

      Where 1 and 2 are inputs, 3 is the output, Tool1 and Tool2 are the
      SimpleTool1 and SimpleTool2 defined above.

      The "main()" uses the WorkflowApp to launch SimpleWorkflow in order to
      unstage intermediate outputs.
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

        logger.info("\t0. perform checks")
        assert len(input_files.keys()) == 2
        assert len(metadata.keys()) == 2

        logger.info("\t1.a Instantiate Tool 1 and run")
        simple_tool1 = SimpleTool1(self.configuration)

        try:
            output1, outmd1 = simple_tool1.run(
                # Use remap to convert role "number1" to "input" for simpleTool1
                remap(input_files, input="number1"),
                remap(metadata, input="number1"),
                # Use a temporary file name for intermediate outputs
                {"output": 'file1.out'})
        except Exception as err:  # pylint: disable=broad-except
            logger.fatal("Tool 1, run 1 failed: {}", err)
            return {}, {}
        logger.progress(50)  # out of 100

        logger.info("\t1.b (Instantiate Tool) and run")
        try:
            output2, outmd2 = simple_tool1.run(
                # Use remap to convert role "number2" to "input" for simpleTool1
                remap(input_files, input="number2"),
                remap(metadata, input="number2"),
                # Use a temporary file name for intermediate outputs
                {"output": 'file2.out'})
        except Exception as err:  # pylint: disable=broad-except
            logger.fatal("Tool 1, run 2 failed: {}", err)
            return {}, {}
        logger.progress(75)  # out of 100

        logger.info("\t2. Instantiate Tool and run")
        simple_tool2 = SimpleTool2(self.configuration)
        try:
            output3, outmd3 = simple_tool2.run(
                # Instead of using remap, here we re-build dicts to convert input roles
                {"input1": output1["output"], "input2": output2["output"]},
                {"input1": outmd1["output"], "input2": outmd2["output"]},
                # Workflow output files are from this Tool
                output_files)
        except Exception as err:  # pylint: disable=broad-except
            logger.fatal("Tool 2 failed: {}", err)
            return {}, {}
        logger.progress(100)  # out of 100

        logger.info("\t4. Optionally edit the output metadata")
        logger.info("\t5. Return")
        return output3, outmd3


# -----------------------------------------------------------------------------

def main(input_files, input_metadata, output_files):
    """
    Main function
    -------------

    This function launches the app.
    """

    # 1. Instantiate and launch the App
    logger.info("1. Instantiate and launch the App")
    from mg_tool_api.apps.workflowapp import WorkflowApp
    app = WorkflowApp()
    result = app.launch(SimpleWorkflow, input_files, input_metadata,
                        output_files, {})

    # 2. The App has finished
    logger.info("2. Execution finished")

    return result


def main_json():
    """
    Alternative main function
    -------------

    This function launches the app using configuration written in
    two json files: config.json and input_metadata.json.
    """
    # 1. Instantiate and launch the App
    logger.info("1. Instantiate and launch the App")
    from mg_tool_api.apps.jsonapp import JSONApp
    app = JSONApp()
    result = app.launch(SimpleWorkflow,
                        "tools_demos/config.json",
                        "tools_demos/input_metadata.json",
                        "/tmp/results.json")

    # 2. The App has finished
    logger.info("2. Execution finished; see /tmp/results.json")

    return result


if __name__ == "__main__":
    # Note that the code that was within this if condition has been moved
    # to a function called 'main'.
    # The reason for this change is to improve performance.

    INPUT_FILE_1 = "/tmp/file1"
    INPUT_FILE_2 = "/tmp/file2"
    OUTPUT_FILE = "/tmp/outputFile"

    # The VRE has to prepare the data to be processed.
    # In this example we create 2 files for testing purposes.
    logger.info("1. Create some data: 2 input files")
    with open(INPUT_FILE_1, "w") as f:
        f.write("5")
    with open(INPUT_FILE_2, "w") as f:
        f.write("9")
    logger.info("\t* Files successfully created")

    # Maybe it is necessary to prepare a metadata parser from json file
    # when building the Metadata objects.
    INPUT_METADATA_F1 = Metadata("Number", "plainText")
    INPUT_METADATA_F2 = Metadata("Number", "plainText")

    main({"number1": INPUT_FILE_1,
          "number2": INPUT_FILE_2},
         {"number1": INPUT_METADATA_F1,
          "number2": INPUT_METADATA_F2},
         {"output": OUTPUT_FILE})

    main_json()
