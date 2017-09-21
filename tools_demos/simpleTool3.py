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
class SimpleTool3(Tool):
    """
    Mockup Tool that defines a task with two FILE_IN inputs and one
    FILE_OUT output. The Tool accepts multiple input files and cumulatively
    uses the task to sum them up, producing an output file at each step.
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
        Standard function to call tasks
        """

        # perform checks
        assert len(input_files["input"]) == len(metadata["input"])

        # prepare outputs
        output_pattern = output_files["output"]
        output_files["output"] = []
        output_metadata = {}
        output_metadata["output"] = []
        
        # Iteratively run the tool 3
        previous_input = input_files["input"][0]
        previous_metadata = metadata["input"][0]
        
        for i in range(len(input_files["input"]) - 1):
            next_input = input_files["input"][i+1]
            next_metadata = metadata["input"][i+1]
            file_out = output_pattern%i
            metadata_out = Metadata.get_child(
                (previous_metadata, next_metadata))
            success = self.sumTwoFiles(previous_input,
                                       next_input,
                                       file_out)
            if success:
                output_files["output"].append(file_out)
                # input and outputs share most metadata
                output_metadata["output"].append(metadata_out)
                previous_input = file_out
                previous_metadata = metadata_out

        return output_files, output_metadata

# ------------------------------------------------------------------------------
