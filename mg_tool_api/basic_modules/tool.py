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
from utils import logger  # pylint: disable=ungrouped-imports


# -----------------------------------------------------------------------------
# Main Tool interface
# -----------------------------------------------------------------------------

class Tool(object):  # pylint: disable=too-few-public-methods
    """
    Abstract class describing a specific operation on a precise input data type
    to produce a precise output data type.

    The tool is executed by calling its "run()" method, which should support
    multiple inputs and outputs. Inputs and outputs are valid file names
    locally accessible to the Tool.

    The "run()" method also receives an instance of Metadata for each of the
    input data elements. It is the Tool's responsibility to generate the
    metadata for each of the output data elements, which are returned in a
    tuple (see code below).

    The "run()" method calls the relevant methods that perform the operations
    require to implement the Tool's functionality. Each of these methods should
    be decorated using the "@task" decorator. Further, the task constraints can
    be configured using the "@constraint" decorator.

    See also Workflow.
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

    # @constraint()
    @task(input_file=FILE_IN, output_file=FILE_OUT, isModifier=False)
    def _taskMethod(self, input_file, output_file):  # pylint: disable=no-self-use,invalid-name,unused-argument
        """
        This method performs the actions required to achieve the Tool's
        functionality. Note the use of the "@task" and "@constraint"
        decorators.
        """
        return True

    def run(self, input_files, input_metadata, output_files):  # pylint: disable=unused-argument
        """
        Perform the required operations to achieve the functionality of the
        Tool. This usually involves:
        0. Import tool-specific libraries
        1. Perform relevant checks on input data
        2. Optionally convert input data to internal formats
        3. Perform tool-specific operations
        4. Optionally convert output data to the output format
        5. Write metadata for the output data
        6. Handle failure in any of the above

        In case of failure, the Tool should return None instead of the output
        file name, AND attach an Exception instance to the output metadata (see
        Metadata.set_exception), to allow the wrapping App to report the
        error (see App).

        Note that this method calls the actual task(s). Ideally, each task
        should have a unique name that identifies the operation: these will be
        used by the COMPSs runtime to build a graph and trace.


        Parameters
        ----------
        input_file : dict
            a dict of absolute path names of the input data elements,
            associated with their role;
        input_metadata : dict
            a dict of metadatas for each of the input data elements,
            associated with their role;
        output_files : dict
            a dict of absolute path names of the output data elements,
            associated with their role.


        Returns
        -------
        (output_files, output_metadata)
          output_files : dict
              a dict of absolute path names of the output data elements created
              by the Tool, associated with their role;
          output_metadata : dict
              a dict of metadatas for each of the output data elements created
              by the Tool, associated with their role;


        Example
        -------
        >>> import Tool
        >>> tool = Tool(configuration = {})
        >>> tool.run(
        ... {"input1": <input_1>, "input2": <input_2>},
        ... {"input1": <in_data_1>, "input2": <in_data_2>})
        ({"output": <output_1>}, {"output": <out_data_1>})
        """
        # 0: not required
        # 1:
        assert len(input_files.keys()) == 1
        input_file = input_files["input"]
        output_file = output_files["output"]
        logger.info("Read 1 input file: {}", input_file)
        # 2: not required
        # 3:
        logger.info("Running task")
        task_status = self._taskMethod(input_file, output_file)

        # 4: not required
        # 5:
        output_metadata = Metadata(None, None)
        if task_status:
            logger.info("Task successful")
            return {"output": output_file}, {"output": output_metadata}

        logger.error("Task failed")
        return {}, {}
