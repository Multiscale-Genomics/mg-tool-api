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

# -----------------------------------------------------------------------------
# PyCOMPSs App
# -----------------------------------------------------------------------------
import sys

try:
    if hasattr(sys, '_run_from_cmdl') is True:
        raise ImportError
    from pycompss.api.api import compss_wait_on
except ImportError:
    print("[Warning] Cannot import \"pycompss\" API packages.")
    print("          Using mock decorators.")

    from mg_tool_api.utils.dummy_pycompss import compss_wait_on

from mg_tool_api.basic_modules.app import App


class PyCOMPSsApp(App):  # pylint: disable=too-few-public-methods
    """
    PyCOMPSsApp: uses PyCOMPSs.
    """

    def _post_run(self, tool_instance, output_files, output_metadata):
        """
        Adds a wait command to ensure asynchronous tasks are
        terminated.
        """
        compss_wait_on(output_files.values())
        # Please note that the _post_run can not be done before waiting for
        # the output files.
        # The compss_wait_on performs a synchronization and retrieves the
        # content from output_files. Then it is possible to perform any
        # post operation like storing the results somewhere.
        output_files, output_metadata = super(PyCOMPSsApp, self)._post_run(
            tool_instance,
            output_files,
            output_metadata)
        return output_files, output_metadata
