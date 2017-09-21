# -----------------------------------------------------------------------------
# JSON-configured App
# -----------------------------------------------------------------------------
from apps.workflowapp import WorkflowApp
from basic_modules.metadata import Metadata
import json
import os


class JSONApp(WorkflowApp):
    """
    JSON-configured App.

    Redefines launch to the following signature (see launch for details)

    launch(tool_class, config_json_path, input_metadata_json_path, root_dir)

    """

    def launch(self, tool_class, root_dir,
               config_json_path, input_metadata_json_path):
        """
        Run a Tool with the specified inputs and configuration.


        Parameters
        ----------
        tool_class : class
            the subclass of Tool to be run;
        root_dir : str
            The root directory where the Tool is expected to find input files
            and write outputs.
        config_json_path : str
            path to a valid JSON file containing information on how the tool
            should be executed. The schema for this JSON string is the
            "config.json".
        input_metadata_json_path : str
            path to a valid JSON file containing information on tool inputs.
            The schema for this JSON string is the "input_metadata.json".


        Returns
        -------
        bool


        Example
        -------
        >>> import App, Tool
        >>> app = JSONApp()
        >>> # expects to find valid config.json
        >>> app.launch(Tool, "/path/to/folder", "config.json", "input_metadata.json")
        >>> # writes results.json
        """

        print "0) Unpack information from JSON"
        input_IDs, arguments, output_files = self._read_config(
            config_json_path)

        output_files = self.make_absolute_path(output_files, root_dir)

        input_metadata_IDs = self._read_metadata(
            input_metadata_json_path)

        # arrange by role
        input_metadata = {}
        for role, ID in input_IDs.items():
            if isinstance(ID, (list, tuple)):  # check allow_multiple?
                input_metadata[role] = [input_metadata_IDs[el] for el in ID]
            else:
                input_metadata[role] = input_metadata_IDs[ID]

        # get paths from IDs
        input_files = {}
        for role, metadata in input_metadata.items():
            if isinstance(metadata, (list, tuple)):  # check allow_multiple?
                input_files[role] = [el.file_path for el in metadata]
            else:
                input_files[role] = metadata.file_path

        input_files = self.make_absolute_path(input_files, root_dir)

        # Run launch from the superclass
        output_files, output_metadata = WorkflowApp.launch(
            self, tool_class, input_files, input_metadata,
            output_files, arguments)

        print "4) Pack information to JSON"
        return self._write_json(
            input_files, input_metadata,
            output_files, output_metadata,
            os.path.join(root_dir, "results.json"))

    def make_absolute_path(self, files, root):
        """Make paths absolute."""
        for role, path in files.items():
            if isinstance(path, (list, tuple)):
                files[role] = [os.path.join(root, el) for el in path]
            else:
                files[role] = os.path.join(root, path)
        return files

    def _read_config(self, json_path):
        """
        Read config.json to obtain:
        input_IDs: dict containing IDs of tool input files
        arguments: dict containing tool arguments
        output_files: dict containing absolute paths of tool outputs

        Note that values of input_IDs may be either str or list,
        according to whether "allow_multiple" is True for the role;
        in which case, the VRE will have accepted multiple input files
        for that role.

        For output files with "allow_multiple" True nothing changes
        here: it is up to the Tool developer to handle this.

        For more information see the schema for config.json.
        """
        configuration = json.load(file(json_path))
        input_IDs = {}
        for input_ID in configuration["input_files"]:
            role = input_ID["name"]
            ID = input_ID["value"]
            if role in input_IDs:
                if not isinstance(input_IDs[role], list):
                    input_IDs[role] = [input_IDs[role]]
                input_IDs[role].append(ID)
            else:
                input_IDs[role] = ID

        output_files = {}
        for output_file in configuration["output_files"]:
            output_files[output_file["name"]] = output_file["file"]["file_path"]

        arguments = {}
        for argument in configuration["arguments"]:
            arguments[argument["name"]] = argument["value"]

        return input_IDs, arguments, output_files

    def _read_metadata(self, json_path):
        """
        Read input_metadata.json to obtain input_metadata_IDs, a dict
        containing metadata on each of the tool input files,
        arranged by their ID.

        For more information see the schema for input_metadata.json.
        """
        metadata = json.load(file(json_path))
        input_metadata = {}
        input_source_ids = {}
        for input_file in metadata:
            ID = input_file["_id"]
            input_metadata[ID] = Metadata(
                data_type=input_file["data_type"],
                file_type=input_file["file_type"],
                file_path=input_file["file_path"],
                meta_data=input_file["meta_data"])
            # Keep track of source_ids
            input_source_ids[ID] = input_file["source_id"]

        # Convert IDs to paths where available
        for ID, source_ids in input_source_ids.iteritems():
            input_metadata[ID].sources = [
                input_metadata[sID].file_path for sID in source_ids
                if sID in input_metadata]

        return input_metadata

    def _write_json(self,
                    input_files, input_metadata,
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
                "meta_data": metadata.meta_data
            }

        for role, path in output_files.items():
            metadata = output_metadata[role]
            if isinstance(path, (list, tuple)):  # check allow_multiple?
                assert (isinstance(metadata, (list, tuple)) and \
                        len(metadata) == len(path)) or \
                        isinstance(metadata, Metadata), \
                        """Wrong number of metadata entries for role {role}:
either 1 or {np}, not {nm}""".format(role=role, np=len(path), nm=len(metdata))

                if not isinstance(metadata, (list, tuple)):
                    metadata = [metadata] * len(path)

                results.extend(
                    [_newresult(role, pa, md) for pa, md in zip(path, metadata)])
            else:
                results.append(
                    _newresult(role, path, metadata))
        json.dump({"output_files": results}, file(json_path, 'w'))
        return True
