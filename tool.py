from mug import datatypes as mug_datatypes
from . import Metadata

from pycompss.api.task import task
from pycompss.api.constraint import constraint
from pycompss.api.parameter import FILE_IN, FILE_OUT

#------------------------------------------------------------------------------
# Main Tool interface
#------------------------------------------------------------------------------
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
    be decorated using the "@task" decorator. Further, the execution
    environment in which each operation is run can be configured by decorating
    the appropriate method(s) using the "@constraint" decorator.

    See also Workflow.
    """
    input_data_type = None
    output_data_type = None
    configuration = {}
    
    def __init__(self, configuration = {}):
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
    @task(input_file = FILE_IN, output_file = FILE_OUT, isModifier = False)
    def _taskMethod(self, input_file):
        """
        This method performs the actions required to achieve the Tool's
        functionality. Note the use of the "@task" and "@constraint"
        decorators.
        """
        output_file = "/path/to/output_file"
        return output_file

    def run(self, input_files, metadata = None):
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
        input_file : list
        	List of valid file names (str) locally accessible to the Tool. 
        metadata : list
        	List of Metadata instances, one for each of the input_files.


        Returns
        -------
        list, list
        	 1. a list of output files (str), each a valid file name locally
             	accessible to the Tool
             2. a list of Metadata instances, one for each of the
             	output_files


        Example
        -------
        >>> import Tool
        >>> tool = Tool(configuration = {})
        >>> tool.run([<input_1>, <input_2>], [<in_data_1>, <in_data_2>])
        ([<output_1>, <output_2>], [<out_data_1>, <out_data_2>])
        """
        # 0: not required
        # 1:
        assert len(input_files) == 1
        # 2: not required
        # 3:
        output_file = self.action(input_files[0])
        # 4: not required
        # 5:
        output_format = "OUTPUT_FILE_FORMAT"
        output_metadata = Metadata(self.output_data_type, output_format)
        return ([output_file], [output_metadata])


#------------------------------------------------------------------------------
# Main Workflow interface
#------------------------------------------------------------------------------
class Workflow(Tool):
    """
    Abstract class describing a Workflow. 

    Workflows are similar to Tools in that they are defined as receiving a
    precise input data type to produce a precise output data type. The main
    difference is that, instead of performing the operations themselves, they
    instantiate other Tools and call their "run()" method to define a flow of
    operations. Workflows can be further nested, to provide easy access to very
    complex pipelines. Furthermore, Workflows automatically take advantage of
    the VRE's ability to optimise the data flow between operations: this is a
    powerful strategy to implement the most data intensive pipelines.

    The Workflow itself is executed by calling its "run()" method; as for
    Tools, "run()" should support multiple inputs and outputs, which are
    assumed to be valid file names locally accessible to the Workflow. This
    allows the Workflow to use the output of Tools as input for other Tools.

    The "run()" method of Workflows should keep track of these intermediate
    outputs by using the "add_intermediate()" method, to allow the wrapping App
    to unstage these (see App).

    As for Tools, Workflows are expected to generate metadata for each of the
    outputs (as well as for intermediate outputs); generally the metadata
    generated by the Tools called by the Workflow will be sufficient.

    """
    input_data_type = None
    output_data_type = None
    intermediate_outputs = []
    configuration = {}
    
    def add_intermediate(self, output_file, metadata):
        """
        Add an intermediate output file, complete with its metadata. It is the
        App's responsibility to look for these and unstage them: see also
        WorkflowApp. 


        Parameters
        ----------
        output_file : str
        	Valid file name locally accessible to the Tool.
        metadata : Metadata
        	Corresponding metadata instance.


        Returns
        -------
        bool
        	True upon success.
        """
        for fname, meta in zip(output_file, metadata):
            self.intermediate_outputs.append((fname, meta))
        return True

    def run(self, input_files, metadata = None):
        """
        Perform the required operations to achieve the functionality of the
        Workflow. This usually involves:
        0. Perform relevant checks on the input
        1. Instantiate a Tool and run it using some input data
        2. Add the Tool's output to the intermediates
        3. Repeat from 1 as many times as required
        4. Optionally edit the output metadata
        5. Return the output files and metadata

        See also help(Tool.run).
        """
        pass
