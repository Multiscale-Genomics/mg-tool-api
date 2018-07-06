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
from mg_tool_api.utils import logger
from tools_demos.simpleTool1 import SimpleTool1
from tools_demos.simpleTool3 import SimpleTool3


class SimpleWorkflow2(Workflow):  # pylint: disable=too-few-public-methods
    """
    Simple example of Workflow using PyCOMPSs, called using an App.

    - SimpleTool1:
      reads an integer from a file, increments it, and writes it to file
    - SimpleTool3:
      reads N integers from N files and cumulatively sums them, writing
      each intermediate result to file; for example, if 4 files are input
      (A, B, C, D), then 3 files are output: O1 = A+B, O2 = O1+C, O3 = O2+D.
    - SimpleWorkflow:
      implements the following workflow:

          1           2            3           ...
          |           |            |            |
     SimpleTool1  SimpleTool1  SimpleTool1  SimpleTool1
          |           |            |            |
          +-----------+------.-----+------------+
                             |
                        SimpleTool3
                             |
                 +-----------+-----------+
                 |           |           |
                 4           5          ...

      Where 1, 2, 3, ... are a variable number of inputs; 4, 5, ... are
      a variable number of outputs, and SimpleTool1 and SimpleTool3 are
      defined above.

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

    def run(self, input_files, metadata, output_files):  # pylint: disable=too-many-locals

        logger.info("\t0. perform checks")
        assert len(input_files.keys()) == 1
        assert len(metadata.keys()) == 1
        assert len(input_files["number"]) == len(metadata["number"])

        # Prepare lists to collect outputs of first step
        outputs = []
        out_mds = []

        # Run through inputs and apply SimpleTool1 to each
        logger.info("\t1.a Instantiate Tool1")
        simple_tool1 = SimpleTool1(self.configuration)

        for i, path in enumerate(input_files["number"]):
            input_metadata = metadata["number"][i]
            logger.info("\t1.b run {}".format(i))
            try:
                output, outmd = simple_tool1.run(
                    {"input": path},
                    {"input": input_metadata},
                    {"output": path + '.out'})
                outputs.append(output["output"])
                out_mds.append(outmd["output"])
            except Exception as err:  # pylint: disable=broad-except
                logger.error("Tool 1, run {} failed: {}", i, err)
            logger.progress(75 * i / len(input_files["number"]))
        logger.info("\t2. Instantiate Tool and run")

        # Apply SimpleTool3 to all outputs of first step
        simple_tool3 = SimpleTool3(self.configuration)
        try:
            output3, outmd3 = simple_tool3.run(
                {"input": outputs},
                {"input": out_mds},
                output_files)
        except Exception as err:   # pylint: disable=broad-except
            logger.fatal("Tool 2 failed: {}", err)
            return {}, {}
        logger.progress(100)

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
    result = app.launch(SimpleWorkflow2, input_files, input_metadata,
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
    result = app.launch(SimpleWorkflow2,
                        "tools_demos/config2.json",
                        "tools_demos/input_metadata2.json",
                        "/tmp/results.json")

    # 2. The App has finished
    logger.info("2. Execution finished; see /tmp/results.json")

    return result


if __name__ == "__main__":

    INPUT_FILE_1 = "/tmp/file1"
    INPUT_FILE_2 = "/tmp/file2"
    INPUT_FILE_3 = "/tmp/file3"
    OUTPUT_FILE = "/tmp/outputFile{}"  # allow_multiple = True

    # The VRE has to prepare the data to be processed.
    # In this example we create 2 files for testing purposes.
    logger.info("1. Create some data: 2 input files")
    with open(INPUT_FILE_1, "w") as f:
        f.write("5")
    with open(INPUT_FILE_2, "w") as f:
        f.write("9")
    with open(INPUT_FILE_3, "w") as f:
        f.write("13")
    logger.info("\t* Files successfully created")

    # Maybe it is necessary to prepare a metadata parser from json file
    # when building the Metadata objects.
    INPUT_METADATA_F1 = Metadata("Number", "plainText")
    INPUT_METADATA_F2 = Metadata("Number", "plainText")
    INPUT_METADATA_F3 = Metadata("Number", "plainText")

    main({"number": [INPUT_FILE_1, INPUT_FILE_2, INPUT_FILE_3]},
         {"number": [INPUT_METADATA_F1, INPUT_METADATA_F2, INPUT_METADATA_F3]},
         {"output": OUTPUT_FILE})

    main_json()
