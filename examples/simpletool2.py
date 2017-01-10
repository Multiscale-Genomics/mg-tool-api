import os
from .. import Tool
from pycompss.api.parameter import FILE_IN, FILE_OUT
from pycompss.api.task import task
from pycompss.api.constraint import constraint


class SimpleTool2(Tool):
    """
    Mockup Tool that defines a task with two FILE_IN inputs and one FILE_OUT
    output.
    """

    input_data_type = ["number file", "number file"]
    output_data_type = "number file"

    # @constraint()
    @task(file1=FILE_IN, file2=FILE_IN, file3=FILE_OUT, returns=int,
          isModifier=False)
    def sumTwoFiles(self, file1, file2, file3):
        """
        Task that merges the contents of two files and returns the value
        @param file1
        @param file2
        @param file3
        @return int
        """
        result = 0
        try:
            with open(file1, 'r+') as f:
                result += int(f.read())
            with open(file2, 'r+') as f:
                result += int(f.read())
            with open(file3, 'w') as f:
                f.write(str(result))
            return True
        except:
            return False

    def run(self, input_files, metadata):
        """
        Standard function to call a task
        """
        output_file = os.path.join(
            os.path.dirname(input_files[0]),
            "summed.out")

        # input and output share most metadata
        output_metadata = dict(
            data_type=metadata[0]["data_type"],
            file_type=metadata[0]["file_type"],
            meta_data=metadata[0]["meta_data"])

        # handle error
        if not self.sumTwoFiles(input_files[0], input_files[1], output_file):
            output_metadata.set_exception(
                Exception(
                    "SimpleTool2: Could not process files {}, {}.".format(
                        *input_files)))
            output_file = None
        return ([output_file], [output_metadata])
