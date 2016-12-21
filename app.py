from mug import datatypes as mug_datatypes
from .metadata import Metadata

# ------------------------------------------------------------------------------
# Main App Interface
# ------------------------------------------------------------------------------


class App(object):

    """
    The generic App interface.

    The App is the main entry point to the tools layer of the VRE. The App
    abstracts details of the particular local execution environment in order
    for Tools to run smoothly. For example, a subclass of App may exist that
    deals with execution of Tools in a Virtual Machine, without file-system
    access to the VRE, using COMPSs. Apps should be compatible with all Tools.

    In general, App deals with:

    1) retrieve and stage the inputs required by the Tool,
    3) instantiate and configure the Tool,
    3) call its "run" method,
    4) deal with errors, and
    5) finally unstage its outputs.

    The App.launch() method is called in order to run a Tool within the App,
    with each call wrapping a single Tool class. App.launch calls Tool.run();
    App._pre_run() and App._post_run() should be called to execute operations
    before and after, in order to facilitate the accumulation of features in
    App subclasses in a way similar to the mixin pattern (see for example
    WorkflowApp).

    The App must check for errors in Tool execution and take the necessary
    actions to report the errors to the caller. Since Tools may generally be
    executed on separate machines, the Exceptions are passed by the Tools in
    the Metadata (see Metadata.set_exception). App._error_report() should be
    called to report errors.

    As Apps need to be compatible with all Tools, it is unpractical to use Apps
    to combine Tools. Instead, Workflows can be implemented (see Workflow) in
    order to take advantage of the VRE's capabilities to optimise the data flow
    according to the specific requirements of the workflow, by ensuring that
    data is staged/unstaged only once.

    The following general interface outlines the App's workload, independent of
    the execution environment and runtime used (e.g. it does not rely on
    PyCOMPSs, see PyCOMPSsApp). Subclasses of App should implement operations
    specific to the local execution environment, such as staging/unstaging.
    """

    def launch(self, tool_class, input_ids, configuration):
        """
        Run a Tool with the specified inputs and configuration.


        Parameters
        ----------
        tool_class : class
            the subclass of Tool to be run;
        input_ids : list
            a list of unique IDs of the input data elements required by the
            Tool;
        configuration : dict
            a dictionary containing information on how the tool should be
            executed.


        Returns
        -------
        list
            A list of unique IDs for the Tool's output data elements.


        Example
        -------
        >>> import App, Tool
        >>> app = App()
        >>> app.launch(Tool, [<input_id>], {})
        """

        "1) Retrieve and stage inputs"
        input_files, input_metadata = self._stage(input_ids)

        "2) Instantiate and configure Tool"
        tool_instance = self._instantiate_tool(tool_class, configuration)

        "3) Run Tool"
        input_files, input_metadata = self._pre_run(
            tool_instance, input_files, input_metadata)

        output_files, output_metadata = tool_instance.run(
            input_files, metadata=input_metadata)

        output_files, output_metadata = self._post_run(
            tool_instance, output_files, output_metadata)

        "4) Check for errors"
        if any([outmd.error for outmd in output_metadata]):
            fatal = self._error(
                [outmd for outmd in output_metadata if outmd.error])
            if fatal:
                return None

        "5) Unstage outputs"
        output_ids = self._unstage(output_files, output_metadata)
        return output_ids

    def _instantiate_tool(self, tool_class, configuration):
        """
        Instantiate the Tool with its configuration.
        Returns instance of the specified Tool subclass.
        """
        return tool_class(configuration)

    def _stage(self, input_ids):
        """
        Retrieve and stage the specified inputs, as a list of unique data IDs.
        This generally involves calling the DMP's "get_file_by_id" method.
        Returns a list of file_names and a corresponding list of metadata.
        """
        pass

    def _pre_run(self, tool_instance, input_files, input_metadata):
        """
        Subclasses can specify here operations to be executed BEFORE running
        Tool.run(); subclasses should also run the superclass _pre_run.

        Receives the instance of the Tool that will be run, and its inputs
        values: input_files and input_metadata (see Tool).
        Returns input_files and input_metadata.
        """
        return input_files, input_metadata

    def _post_run(self, tool_instance, output_files, output_metadata):
        """
        Subclasses can specify here operations to be executed AFTER running
        Tool.run(); subclasses should also run the superclass _post_run.

        Receives the instance of the Tool that was run, and its return values:
        output_files and output_metadata (see Tool).
        Returns output_files and output_metadata.
        """
        return output_files, output_metadata

    def _error(self, error_metadata):
        """
        Subclasses can specify here operations to be executed to treat and
        report errors occurred in Tool.run(). The passed error_metadata should
        be only instances of Metadata that carry an Exception.

        Returns True if the error is FATAL and entails immediate arrest of App
        operations (i.e. unstaging will not occur).
        """
        for errmd in error_metadata:
            print errmd.exception
        return True

    def _unstage(self, output_files, output_metadata):
        """
        Unstage the specified outputs, as a list of file names and a
        corresponding list of metadata. This generally involves declaring each
        output data element to the DMP (via the "set_file" method) to obtain
        unique data IDs that are then returned as a list.
        """
        pass
