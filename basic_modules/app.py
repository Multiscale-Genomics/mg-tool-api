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
from basic_modules.metadata import Metadata  # pylint: disable=unused-import
from utils import logger


# -----------------------------------------------------------------------------
# Main App Interface
# -----------------------------------------------------------------------------
class App(object):  # pylint: disable=too-few-public-methods
    """
    The generic App interface.

    The App abstracts details of the particular local execution environment
    in order for Tools to run smoothly. For example, a subclass of App may
    exist that deals with execution of Tools in a Virtual Machine.
    Apps should be compatible with all Tools.

    In general, App deals with:

    1) instantiate and configure the Tool, and
    2) call its "run" method

    The App.launch() method is called in order to run a Tool within the App,
    with each call wrapping a single Tool class. The App.launch method calls
    the Tool.run() method; the App._pre_run() and App._post_run() methods
    should be called to execute operations before and after, in order to
    facilitate the accumulation of features in App subclasses in a way similar
    to the mixin pattern (see for example WorkflowApp).

    As Apps need to be compatible with any Tool, it is unpractical to use Apps
    to combine Tools. Instead, Workflows can be implemented (see Workflow) in
    order to take advantage of the VRE's capabilities to optimise the data flow
    according to the specific requirements of the workflow, by ensuring that
    data is staged/unstaged only once.

    This general interface outlines the App's workload, independent of the
    execution environment and runtime used (e.g. it does not rely on PyCOMPSs,
    see PyCOMPSsApp).
    """

    def launch(self, tool_class,  # pylint: disable=too-many-arguments
               input_files, input_metadata,
               output_files, configuration):
        """
        Run a Tool with the specified inputs and configuration.


        Parameters
        ----------
        tool_class : class
            the subclass of Tool to be run;
        input_files : dict
            a dict of absolute path names of the input data elements required
            by the Tool, associated with their role;
        input_metadata : dict
            a dict of metadatas for each of the input data elements required
            by the Tool, associated with their role;
        output_files : dict
            a dict of absolute path names of the output data elements created
            by the Tool, associated with their role;
        configuration : dict
            a dictionary containing information on how the tool should be
            executed.


        Returns
        -------
        (output_files, output_metadata)
          output_files : dict
              a dict of absolute path names of the output data elements created
              by the Tool, associated with their role;
          output_metadata : dict
              a dict of metadatas for each of the output data elements created
              by the Tool, associated with their role.


        Example
        -------
        >>> import App, Tool
        >>> app = App()
        >>> app.launch(Tool, {"input": <input_file>}, {})
        """

        logger.info("1) Instantiate and configure Tool")
        tool_instance = self._instantiate_tool(tool_class, configuration)

        logger.info("2) Run Tool")
        input_files, input_metadata = self._pre_run(tool_instance,
                                                    input_files,
                                                    input_metadata)

        output_files, output_metadata = tool_instance.run(input_files,
                                                          input_metadata,
                                                          output_files)

        output_files, output_metadata = self._post_run(tool_instance,
                                                       output_files,
                                                       output_metadata)

        logger.info("Output_files: ", output_files)
        return output_files, output_metadata

    def _instantiate_tool(self, tool_class, configuration):  # pylint: disable=no-self-use
        """
        Instantiate the Tool with its configuration.
        Returns instance of the specified Tool subclass.
        """
        return tool_class(configuration)

    def _pre_run(self, tool_instance, input_files, input_metadata):  # pylint: disable=no-self-use,unused-argument
        """
        Subclasses can specify here operations to be executed BEFORE running
        Tool.run(); subclasses should also run the superclass _pre_run.

        Receives the instance of the Tool that will be run, and its inputs
        values: input_files and input_metadata (see Tool).
        Returns input_files and input_metadata.
        """
        return input_files, input_metadata

    def _post_run(self, tool_instance, output_files, output_metadata):  # pylint: disable=no-self-use,unused-argument
        """
        Subclasses can specify here operations to be executed AFTER running
        Tool.run(); subclasses should also run the superclass _post_run.

        Receives the instance of the Tool that was run, and its return values:
        output_files and output_metadata (see Tool).
        Returns output_files and output_metadata.
        """
        return output_files, output_metadata
