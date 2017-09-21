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
            print "DATA: ", data
            with open(output_file, 'w') as f:
                f.write(str(int(data) + 1))
            return True
        except:
            return False

    def run(self, input_files, metadata, output_files):
        """
        Standard function to call a task
        """

        # input and output share most metadata
        output_metadata = Metadata.get_child(
            metadata["input"], output_files["output"])

        # Run the tool
        self.inputPlusOne(input_files["input"],
                          output_files["output"])

        return {"output": output_files["output"]}, {"output": output_metadata}

# -----------------------------------------------------------------------------
