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
            input_metadata[role] = input_metadata_IDs[ID]

        # get paths from IDs
        input_files = {}
        for role, metadata in input_metadata.items():
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
            files[role] = os.path.join(root, path)
        return files

    def _read_config(self, json_path):
        """
        Read config.json to obtain:
        input_IDs: dict containing IDs of tool input files
        arguments: dict containing tool arguments
        output_files: dict containing absolute paths of tool outputs

        For more information see the schema for config.json.
        """
        configuration = json.load(file(json_path))
        input_IDs = {}
        for input_ID in configuration["input_files"]:
            input_IDs[input_ID["name"]] = input_ID["value"]

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
        for input_file in metadata:
            input_metadata[input_file["_id"]] = Metadata(
                data_type=input_file["data_type"],
                file_type=input_file["file_type"],
                file_path=input_file["file_path"],
                source_id=input_file["source_id"],
                meta_data=input_file["meta_data"],
                data_id=input_file["_id"])
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

        For more information see the schema for results.json.
        """
        results = []
        for role, path in output_files.items():
            results.append({
                "name": role,
                "file_path": path,
                "data_type": output_metadata[role].data_type,
                "file_type": output_metadata[role].file_type,
                "source_id": output_metadata[role].source_id,
                "meta_data": output_metadata[role].meta_data
            })
        json.dump({"output_files": results}, file(json_path, 'w'))
        return True
