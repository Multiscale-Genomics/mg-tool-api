from pycompss.api.parameter import FILE_IN, FILE_OUT
from pycompss.api.task import task
from basic_modules.metadata import Metadata
from basic_modules.tool import Tool


# -----------------------------------------------------------------------------
class Tool2(Tool):
    """
    Mockup Tool that defines a task with two FILE_IN inputs and one
    FILE_OUT output
    """

    # @constraint()
    @task(input_file=FILE_IN, output_file=FILE_OUT,
          returns=int, isModifier=False)
    def myTask2(self, input_file, output_file):
        """
        @param input_file Input file where the initial content is
        @param output_file Output file where the result is stored
        @return bool True if done successfully. False on the contrary.
        """
        # do something with input_file and output_file
        pass

        with open(output_file, 'w') as f:
            f.write("this is a test file")

        return 0

    def run(self, input_files, metadata, output_files):
        """
        Standard function to call a task
        """

        # Run the tool
        taskResult = self.myTask2(input_files[0], output_files[0])

        # handle error
        # [COMMENT] myTask is a task it will return a future object.
        # Consequently, the following condition will never be true.
        # Alternatively if output metadata is a parameter of the task, the
        # task could add something to it within it's execution, and check its
        # value when synchronized (usually done at the end of the workflow).
        '''
        if not taskResult:
            output_metadata.set_exception(Exception(
                "SimpleTool1: Could not process file {}.".format(input_file)))
            output_file = None
        '''
        return (output_files, metadata)

# -----------------------------------------------------------------------------
