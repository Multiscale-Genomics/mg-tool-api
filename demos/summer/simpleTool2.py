from pycompss.api.parameter import FILE_IN, FILE_OUT
from pycompss.api.task import task
from basic_modules.metadata import Metadata
from basic_modules.tool import Tool


# -----------------------------------------------------------------------------
class SimpleTool2(Tool):
    """
    Mockup Tool that defines a task with two FILE_IN inputs and one
    FILE_OUT output.
    """

    # @constraint()
    @task(file1=FILE_IN, file2=FILE_IN, file3=FILE_OUT,
          returns=bool, isModifier=False)
    def sumTwoFiles(self, file1, file2, file3):
        """
        Task that merges the contents of two files and returns the value.
        @param file1 The first input file with initial content
        @param file2 The second input file with initial content
        @param file3 The file where the results will be
        @return bool True if done successfully. False on the contrary.
        """
        result = 0
        try:
            with open(file1, 'r+') as f:
                result += int(f.read())
                print result
            with open(file2, 'r+') as f:
                result += int(f.read())
            with open(file3, 'w') as f:
                f.write(str(result))
            return True
        except:
            return False

    def run(self, input_files, metadata, output_files):
        """
        Standard function to call a task
        """

        # input and output share most metadata
        output_metadata = Metadata.get_child(metadata[0])

        # Run the tool 2
        taskResult = self.sumTwoFiles(input_files[0],
                                      input_files[1],
                                      output_files[0])

        # handle error
        # [COMMENT] sumTwoFiles is a task it will return a future object.
        # Consequently, the following condition will never be true.
        # Alternatively if output metadata is a parameter of the task, the
        # task could add something to it within it's execution, and check its
        # value when synchronized (usually done at the end of the workflow).
        '''
        if not taskResult:
            print "not"
            output_metadata.set_exception(
                Exception(
                    "SimpleTool2: Could not process files {},
                    {}.".format(*input_files)))
            output_file = None
        '''
        return (output_files, [output_metadata])

# ------------------------------------------------------------------------------
