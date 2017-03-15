from .. import Tool, Metadata
from pycompss.api.parameter import FILE_IN, FILE_OUT
from pycompss.api.task import task
from pycompss.api.constraint import constraint


class SimpleTool1(Tool):
    """
    Mockup Tool that defines a task with one FILE_IN input and one FILE_OUT
    output.
    """

    input_data_type = "number file"
    output_data_type = "number file"

    # @constraint()
    @task(input_file=FILE_IN, output_file=FILE_OUT, returns=int,
          isModifier=False)
    def inputPlusOne(self, input_file, output_file):
        """
        Task that writes a file with the content from a file plus one
        @param input_file
        @param output_file
        @return bool
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

    def run(self, input_files, metadata):
        """
        Standard function to call a task
        """
        input_file = input_files[0]
        output_file = input_file+".out"

        # input and output share most metadata
        output_metadata = Metadata.get_child(metadata[0])

        # handle error
        if not self.inputPlusOne(input_file, output_file):
            output_metadata.set_exception(
                Exception(
                    "SimpleTool1: Could not process file {}.".format(
                        input_file)))
            output_file = None
        return ([output_file], [output_metadata])
