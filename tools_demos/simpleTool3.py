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

    from utils.dummy_pycompss import FILE_IN, FILE_OUT
    from utils.dummy_pycompss import task

from basic_modules.metadata import Metadata
from basic_modules.tool import Tool
from utils import logger  # pylint: disable=ungrouped-imports


# -----------------------------------------------------------------------------
class SimpleTool3(Tool):
    """
    Mockup Tool that defines a task with two FILE_IN inputs and one
    FILE_OUT output. The Tool accepts multiple input files and cumulatively
    uses the task to sum them up, producing an output file at each step.
    """

    # @constraint()
    @task(file1=FILE_IN, file2=FILE_IN, file3=FILE_OUT,
          returns=bool, isModifier=False)
    def sumTwoFiles(self, file1, file2, file3):  # pylint: disable=invalid-name,no-self-use
        """
        Task that merges the contents of two files and returns the value.
        @param file1 The first input file with initial content
        @param file2 The second input file with initial content
        @param file3 The file where the results will be
        @return bool True if done successfully. False on the contrary.
        """
        result = 0
        try:
            with open(file1, 'r+') as f1_handle:
                result += int(f1_handle.read())
            with open(file2, 'r+') as f2_handle:
                result += int(f2_handle.read())
            with open(file3, 'w') as f3_handle:
                f3_handle.write(str(result))
            return True
        except (IOError, OSError):
            return False

    def run(self, input_files, input_metadata, output_files):
        """
        Standard function to call tasks
        """

        # perform checks
        assert len(input_files["input"]) == len(input_metadata["input"])

        # prepare outputs
        logger.info("SimpleTool3: Preparing outputs")
        output_pattern = output_files["output"]
        output_files["output"] = []
        output_metadata = {}
        output_metadata["output"] = []

        # Iteratively run the task
        previous_input = input_files["input"][0]
        previous_metadata = input_metadata["input"][0]

        for i in range(len(input_files["input"]) - 1):
            logger.info("SimpleTool3: Summing input {}", i)
            # Add next input file:
            next_input = input_files["input"][i+1]
            next_metadata = input_metadata["input"][i+1]
            # Pre-calculate output path and metadata
            file_out = output_pattern.format(i)
            metadata_out = Metadata.get_child(
                (previous_metadata, next_metadata), file_out)

            # run task
            success = self.sumTwoFiles(previous_input,
                                       next_input,
                                       file_out)
            if success:
                # keep track of successful iterations
                output_files["output"].append(file_out)
                # input and outputs share most metadata
                output_metadata["output"].append(metadata_out)
                previous_input = file_out
                previous_metadata = metadata_out
                logger.info("SimpleTool3: Input {} successful", i)
            else:
                logger.warn("SimpleTool3: Input {} failed", i)

        return output_files, output_metadata

# ------------------------------------------------------------------------------
