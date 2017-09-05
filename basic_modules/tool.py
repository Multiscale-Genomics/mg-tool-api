# from mug import datatypes as mug_datatypes
from pycompss.api.parameter import FILE_IN, FILE_OUT
from pycompss.api.task import task
from basic_modules.metadata import Metadata


# -----------------------------------------------------------------------------
# Main Tool interface
# -----------------------------------------------------------------------------
class Tool(object):
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

    def __init__(self, configuration={}):
        """
        Initialise the tool with its configuration.


        Parameters
        ----------
        configuration : dict
            a dictionary containing parameters that define how the operation
            should be carried out, which are specific to each Tool.
        """
        self.configuration.update(configuration)

    # @constraint()
    @task(input_file=FILE_IN, output_file=FILE_OUT, isModifier=False)
    def _taskMethod(self, input_file, output_file):
        """
        This method performs the actions required to achieve the Tool's
        functionality. Note the use of the "@task" and "@constraint"
        decorators.
        """
        return True

    def run(self, input_files, output_files):
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

        Note that this method calls the actual task(s). Ideally, each task
        should have a unique name that identifies the operation: these will be
        used by the COMPSs runtime to build a graph and trace.


        Parameters
        ----------
        input_files : input_file_spec
            Structure containing information on Tool input files,
            in particular paths (input_files.get_path()) and
            corresponding metadata (input_files.get_metadata()).
        output_files : output_file_spec
            Structure containing information on Tool output files,
            in particular paths (output_files.get_path()) and
            default metadata (output_files.get_metadata()).


        Returns
        -------
        output_files : output_file_spec
            The output_files structure is returned, after appropriately
            calling output_files.confirm_output() for as many outputs
            that have been created by the tool.


        """
        # 0: not required
        # 1:
        assert input_files.nfiles > 1
        input_file = input_files.get_path()
        output_file = output_files.get_path()
        # 2: not required
        # 3:
        self._taskMethod(input_file, output_file)
        # 4: not required
        # 5:
        output_files.confirm_output(
            output_file,
            source_paths=[input_file],
            metadata=output_files.get_metadata())
        return output_files
