import sys

try:
    if hasattr(sys, '_run_from_cmdl') is True:
        raise ImportError
    from pycompss.api.parameter import FILE_IN, FILE_OUT
    from pycompss.api.task import task
except ImportError:
    print("[Warning] Cannot import \"pycompss\" API packages.")
    print("          Using mock decorators.")

    from dummy_pycompss import FILE_IN, FILE_OUT
    from dummy_pycompss import task

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
        output_metadata = Metadata.get_child(metadata["input1"])

        # Run the tool 2
        self.sumTwoFiles(input_files["input1"],
                         input_files["input2"],
                         output_files["output"])

        return {"output": output_files["output"]}, {"output": output_metadata}

# ------------------------------------------------------------------------------
