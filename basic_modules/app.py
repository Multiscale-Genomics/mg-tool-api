# from mug import datatypes as mug_datatypes
from metadata import Metadata
from basic_modules.file_spec import input_file_spec, output_file_spec
import json


# -----------------------------------------------------------------------------
# Main App Interface
# -----------------------------------------------------------------------------
class App(object):
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

    As Apps need to be compatible with any Tool, it is impractical to use Apps
    to combine Tools. Instead, Workflows can be implemented (see Workflow) in
    order to take advantage of the VRE's capabilities to optimise the data flow
    according to the specific requirements of the workflow, by ensuring that
    data is staged/unstaged only once.

    This general interface outlines the App's workload, independent of the
    execution environment and runtime used (e.g. it does not rely on PyCOMPSs,
    see PyCOMPSsApp).
    """

    def launch(self, tool_class, config_json, results_json):
        """
        Run a Tool with the specified config_json and write
        result information to results_json.


        Parameters
        ----------
        tool_class : class
            the subclass of Tool to be run;
        config_json : string
            path to a valid JSON file containing information on how the tool
            should be executed. The schema for this JSON string is the
            "config.json".
        results_json : string
            path where to write the JSON file containing information on the
            results of the tool execution. The schema for this JSON string is
            the "results.json".

        Returns
        -------
        bool


        Example
        -------
        >>> import App, Tool
        >>> app = App()
        >>> # expects to find valid config.json
        >>> app.launch(Tool, "config.json", "results.json")
        >>> # writes results.json
        """

        print "0) Unpack information from JSON"
        input_files, output_files, arguments = self._read_json(config_json)

        print "1) Instantiate and configure Tool"
        tool_instance = self._instantiate_tool(tool_class, arguments)

        print "2) Run Tool"
        input_files, output_files = self._pre_run(tool_instance,
                                                  input_files, output_files)

        output_files = tool_instance.run(input_files, output_files)

        output_files = self._post_run(tool_instance, output_files)

        print "3) Pack information to JSON"
        return self._write_json(results_json)

    def _read_json(self, json_path):
        """
        Read config.json to obtain:
        input_files: input_file_spec containing information about tool inputs
        output_files: output_file_spec containing information about tool
                      outputs
        arguments: dictionary containing information about tool arguments

        For more information see the schema for config.json.
        """
        configuration = json.load(json_path)
        input_files = input_file_spec()
        for input_file in configuration["input_files"]:
            input_files.add_file(
                role=input_file["name"],
                path=input_file["path"],
                metadata=input_file["metadata"]
            )
        output_files = output_file_spec()
        for output_file in configuration["output_files"]:
            output_files.add_file(
                role=output_file["name"],
                path=output_file["path"],
                metadata=output_file["metadata"]
            )
        arguments = dict()
        for argument in configuration["arguments"]:
            arguments[argument["name"]] = argument["value"]

        return input_files, output_files, arguments

    def _instantiate_tool(self, tool_class, configuration):
        """
        Instantiate the Tool with its configuration.
        Returns instance of the specified Tool subclass.
        """
        return tool_class(configuration)

    def _pre_run(self, tool_instance, input_files, output_files):
        """
        Subclasses can specify here operations to be executed BEFORE running
        Tool.run(); subclasses should also run the superclass _pre_run.

        Receives the instance of the Tool that will be run, and its inputs
        values: input_files and output_files (see Tool).
        Returns input_files and output_files.
        """
        return input_files, output_files

    def _post_run(self, tool_instance, output_files):
        """
        Subclasses can specify here operations to be executed AFTER running
        Tool.run(); subclasses should also run the superclass _post_run.

        Receives the instance of the Tool that was run, and its return values:
        output_files (see Tool).
        Returns output_files
        """
        return output_files

    def _write_json(self, input_files, output_files, json_path):
        """
        Write results.json using information from input_file and output_files:
        input_files: input_file_spec containing information about tool inputs
        output_files: output_file_spec containing information about tool
                      outputs

        For more information see the schema for results.json.
        """
        output = {}
        for path, sources, metadata in output_files.iterate_outputs():
            output[path] = {
                "name": output_files.get_role(path),
                "file_path": path,
                "source_id": sources,
                "taxon_id": 9606,
                "meta_data": metadata
            }
        json.write(output, json_path)
        return True
