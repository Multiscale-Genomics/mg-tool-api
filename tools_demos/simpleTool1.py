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
import sys

try:
    if hasattr(sys, '_run_from_cmdl') is True:
        raise ImportError
    from pycompss.api.parameter import FILE_IN, FILE_OUT
    from pycompss.api.task import task
except ImportError:
    print("[Warning] Cannot import \"pycompss\" API packages.")
    print("          Using mock decorators.")

    from utils.dummy_pycompss import FILE_IN, FILE_OUT  # pylint: disable=ungrouped-imports
    from utils.dummy_pycompss import task  # pylint: disable=ungrouped-imports

from basic_modules.metadata import Metadata
from basic_modules.tool import Tool
from utils import logger


# -----------------------------------------------------------------------------
class SimpleTool1(Tool):
    """
    Mockup Tool that defines a task with one FILE_IN input and one
    FILE_OUT output
    """

    # @constraint()
    @task(input_file=FILE_IN, output_file=FILE_OUT,
          returns=int, isModifier=False)
    def inputPlusOne(self, input_file, output_file):  # pylint: disable=invalid-name,no-self-use
        """
        Task that writes a file with the content from a file plus one
        @param input_file Input file where the initial content is
        @param output_file Output file where the result is stored
        @return bool True if done successfully. False on the contrary.
        """
        try:
            data = None
            with open(input_file, 'r+') as input_file_handle:
                data = input_file_handle.readline()
            print("DATA: ", data)
            with open(output_file, 'w') as output_file_handle:
                output_file_handle.write(str(int(data) + 1))
            return True
        except (IOError, OSError):
            return False

    def run(self, input_files, input_metadata, output_files):
        """
        Standard function to call a task
        """

        # input and output share most metadata
        output_metadata = Metadata.get_child(
            input_metadata["input"], output_files["output"])

        # Run the tool
        logger.info("SimpleTool1: Running task inputPlusOne")
        task_status = self.inputPlusOne(input_files["input"],
                                        output_files["output"])
        logger.info("SimpleTool1: task inputPlusOne done")

        if task_status:
            logger.info("SimpleTool1: run successful")
            return ({"output": output_files["output"]},
                    {"output": output_metadata})

        logger.fatal("SimpleTool1: run failed")
        return {}, {}

# -----------------------------------------------------------------------------
