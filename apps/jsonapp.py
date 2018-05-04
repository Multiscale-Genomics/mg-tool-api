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

# -----------------------------------------------------------------------------
# JSON-configured App
# -----------------------------------------------------------------------------
import json

from apps.workflowapp import WorkflowApp
from basic_modules.metadata import Metadata


class JSONApp(WorkflowApp):  # pylint: disable=too-few-public-methods
    """
    JSON-configured App.

    Redefines launch to the following signature (see launch for details)

    launch(tool_class, config_path, input_metadata_path, output_metadata_path)

    """

    # The arguments deffer between this function and the supeclass in
    # basic_modules.app to provide a common interface and so that the JSON
    # configuration files can be provided to generate the parameters required
    # by App.
    def launch(self, tool_class,  # pylint: disable=too-many-locals,arguments-differ
               config_path, input_metadata_path, output_metadata_path):
        """
        Run a Tool with the specified inputs and configuration.


        Parameters
        ----------
        tool_class : class
            the subclass of Tool to be run;
        config_path : str
            path to a valid JSON file containing information on how the tool
            should be executed. The schema for this JSON string is the
            "config.json".
        input_metadata_path : str
            path to a valid JSON file containing information on tool inputs.
            The schema for this JSON string is the "input_metadata.json".
        output_metadata_path : str
            path to write the JSON file containing information on tool outputs.
            The schema for this JSON string is the "output_metadata.json".


        Returns
        -------
        bool


        Example
        -------
        >>> import App, Tool
        >>> app = JSONApp()
        >>> # expects to find valid config.json and input_metadata.json
        >>> app.launch(
        ...     Tool, "/path/to/config.json",
        ...     "/path/to/input_metadata.json", "/path/to/results.json")
        >>> # writes /path/to/results.json
        """

        print "0) Unpack information from JSON"
        input_ids, arguments, output_files = self._read_config(
            config_path)

        input_metadata_ids = self._read_metadata(
            input_metadata_path)

        # arrange by role
        input_metadata = {}
        for role, input_id in input_ids.items():
            if isinstance(input_id, (list, tuple)):  # check allow_multiple?
                input_metadata[role] = [input_metadata_ids[el] for el in input_id]
            else:
                input_metadata[role] = input_metadata_ids[input_id]

        # get paths from IDs
        input_files = {}
        for role, metadata in input_metadata.items():
            if isinstance(metadata, (list, tuple)):  # check allow_multiple?
                input_files[role] = [el.file_path for el in metadata]
            else:
                input_files[role] = metadata.file_path

        # Run launch from the superclass
        output_files, output_metadata = super(JSONApp, self).launch(
            tool_class, input_files, input_metadata,
            output_files, arguments)

        print "4) Pack information to JSON"
        return self._write_results(
            input_files, input_metadata,
            output_files, output_metadata,
            output_metadata_path)

    def _read_config(self, json_path):  # pylint: disable=no-self-use
        """
        Read config.json to obtain:
        input_ids: dict containing IDs of tool input files
        arguments: dict containing tool arguments
        output_files: dict containing absolute paths of tool outputs

        Note that values of input_ids may be either str or list,
        according to whether "allow_multiple" is True for the role;
        in which case, the VRE will have accepted multiple input files
        for that role.

        For output files with "allow_multiple" True nothing changes
        here: it is up to the Tool developer to handle this.

        For more information see the schema for config.json.
        """
        configuration = json.load(file(json_path))
        input_ids = {}
        for input_config_id in configuration["input_files"]:
            role = input_config_id["name"]
            input_id = input_config_id["value"]
            if role in input_ids:
                if not isinstance(input_ids[role], list):
                    input_ids[role] = [input_ids[role]]
                input_ids[role].append(input_id)
            else:
                input_ids[role] = input_id

        output_files = {}
        for output_file in configuration["output_files"]:
            output_files[output_file["name"]] = output_file["file"].get("file_path", None)

        arguments = {}
        for argument in configuration["arguments"]:
            arguments[argument["name"]] = argument["value"]

        return input_ids, arguments, output_files

    def _read_metadata(self, json_path):  # pylint: disable=no-self-use
        """
        Read input_metadata.json to obtain input_metadata_ids, a dict
        containing metadata on each of the tool input files,
        arranged by their ID.

        For more information see the schema for input_metadata.json.
        """
        metadata = json.load(file(json_path))
        input_metadata = {}
        for input_file in metadata:
            input_id = input_file["_id"]
            input_metadata[input_id] = Metadata(
                data_type=input_file["data_type"],
                file_type=input_file["file_type"],
                file_path=input_file["file_path"],
                meta_data=input_file["meta_data"],
                taxon_id=input_file["taxon_id"],
                sources=input_file["sources"]
            )
        return input_metadata

    def _write_results(self,  # pylint: disable=no-self-use,too-many-arguments
                       input_files, input_metadata,  # pylint: disable=unused-argument
                       output_files, output_metadata, json_path):
        """
        Write results.json using information from input_files and output_files:
        input_files: dict containing absolute paths of input files
        input_metadata: dict containing metadata on input files
        output_files: dict containing absolute paths of output files
        output_metadata: dict containing metadata on output files

        Note that values of output_files may be either str or list,
        according to whether "allow_multiple" is True for the role;
        in which case, the Tool may have generated multiple output
        files for that role.

        Values of output_metadata for roles for which "allow_multiple"
        is True can be either a list of instances of Metadata, or a
        single instance. In the former case, the list is assumed to be
        the same length as that in output_files. In the latter, the same
        instance of Metadata is used for all outputs for that role.

        For more information see the schema for results.json.
        """
        results = []

        def _newresult(role, path, metadata):
            return {
                "name": role,
                "file_path": path,
                "data_type": metadata.data_type,
                "file_type": metadata.file_type,
                "sources": metadata.sources,
                "taxon_id": metadata.taxon_id,
                "meta_data": metadata.meta_data
            }

        for role, path in output_files.items():
            metadata = output_metadata[role]
            if isinstance(path, (list, tuple)):  # check allow_multiple?
                assert (
                    isinstance(metadata, (list, tuple)) and
                    len(metadata) == len(path)
                ) or isinstance(metadata, Metadata), \
                        """Wrong number of metadata entries for role {role}:
either 1 or {np}, not {nm}""".format(role=role, np=len(path), nm=len(metadata))

                if not isinstance(metadata, (list, tuple)):
                    metadata = [metadata] * len(path)

                results.extend(
                    [_newresult(role, pa, md) for pa, md in zip(path, metadata)])
            else:
                results.append(
                    _newresult(role, path, metadata))
        json.dump(
            {"output_files": results}, file(json_path, 'w'),
            indent=4, separators=(',', ': '))
        return True
