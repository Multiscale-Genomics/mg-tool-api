from mug import datatypes as mug_datatypes
from .resource import Resource

#------------------------------------------------------------------------------
# Main Tool interface
#------------------------------------------------------------------------------
class Tool:
    """
    Abstract class describing a specific operation on a precise input data type
    to produce a precise output data type. The tool should support multiple
    inputs and outputs. The execution environment in which the operation is run
    can be configured by decorating the "run()" method.
    """
    input_data_type = None
    output_data_type = None
    configuration = {}
    
    def __init__(self, configuration = {}):
        """
        Configuration contains parameters that define how the operation should
        be carried out, which are specific to each tool.
        """
        self.configuration.update(configuration)

    @task(input_resource = IN, output_resource = OUT)
    @constraints()
    def run(self, input_resource):
        """
        Perform the required operations to achieve the functionality of the
        tool. This usually involves:
        0. Importing tool-specific libraries
        1. Stage/retrieve data from the input_resource
        2. Optionally convert data to internal formats
        3. Performing tool-specific operations
        4. Optionally convert output data to the output_resource format
        5. Returning the output_resource
        6. Handling failure 
        """
        output_resource = Resource(self.output_data_type)
        return output_resource
