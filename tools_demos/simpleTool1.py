from __future__ import print_function

try:
    from pycompss.api.parameter import FILE_IN, FILE_OUT
    from pycompss.api.task import task
except ImportError:
    print ("[Warning] Cannot import \"pycompss\" API packages.")
    print ("          Using mock decorators.")

    from dummy_pycompss import FILE_IN, FILE_OUT

from basic_modules.metadata import Metadata
from basic_modules.tool import Tool


# -----------------------------------------------------------------------------
class SimpleTool1(Tool):
    """
    Mockup Tool that defines a task with one FILE_IN input and one
    FILE_OUT output
    """

    # @constraint()
    @task(input_file=FILE_IN, output_file=FILE_OUT,
          returns=int, isModifier=False)
    def inputPlusOne(self, input_file, output_file):
        """
        Task that writes a file with the content from a file plus one
        @param input_file Input file where the initial content is
        @param output_file Output file where the result is stored
        @return bool True if done successfully. False on the contrary.
        """
        try:
            data = None
            with open(input_file, 'r+') as f:
                data = f.readline()
            print("DATA: ", data)
            with open(output_file, 'w') as f:
                f.write(str(int(data) + 1))
            return True
        except IOError:
            return False

    def run(self, input_files, metadata, output_files):
        """
        Standard function to call a task
        """

        # input and output share most metadata
        output_metadata = Metadata.get_child(metadata[0])

        # Run the tool
        taskResult = self.inputPlusOne(input_files[0], output_files[0])

        # handle error
        # [COMMENT] inputPlusOne is a task it will return a future object.
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
        return (output_files, [output_metadata])

# -----------------------------------------------------------------------------
