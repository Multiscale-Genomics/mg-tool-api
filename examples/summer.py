"""
Simple example of Workflow using PyCOMPSs, called using an App.

- SimpleTool1: 
  reads an integer from a file, increments it, and writes it to file
- SimpleTool2: 
  reads two integers from two file and writes their sum to file

- SimpleWorkflow:
  implements the following workflow:

	  1           2
	  |			  |
     Tool1		 Tool1
	  |			  |
	  +-----.-----+
			|
		  Tool2
			|
			3

  Where 1 and 2 are inputs, 3 is the output, Tool1 and Tool2 are the SimpleTool1
  and SimpleTool2 defined above.

  The "main()" uses the WorkflowApp to launch SimpleWorkflow in order to unstage
  intermediate outputs.
"""

from .. import Tool, Workflow, Metadata
from pycompss.api.parameter import FILE_IN, FILE_OUT
from pycompss.api.task import task
from pycompss.api.constraint import constraint
import os

#------------------------------------------------------------------------------
class SimpleTool1(Tool):
    """
    Mockup Tool that defines a task with one FILE_IN input and one FILE_OUT output
    """

    input_data_type = "number file"
    output_data_type = "number file"
    
    #@constraint()
    @task(input_file=FILE_IN, output_file=FILE_OUT, returns=int, isModifier=False)
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
                    "SimpleTool1: Could not process file {}.".format(input_file)))
            output_file = None
        return ([output_file], [output_metadata])


#------------------------------------------------------------------------------
class SimpleTool2(Tool):
    """
    Mockup Tool that defines a task with two FILE_IN inputs and one FILE_OUT output.
    """

    input_data_type = ["number file", "number file"]
    output_data_type = "number file"
    
    #@constraint()
    @task(file1=FILE_IN, file2=FILE_IN, file3=FILE_OUT, returns=int, isModifier=False)
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
        output_metadata = Metadata.get_child(metadata)
        
        # handle error
        if not self.sumTwoFiles(input_files[0], input_files[1], output_file):
            output_metadata.set_exception(
                Exception(
                    "SimpleTool2: Could not process files {}, {}.".format(*input_files)))
            output_file = None
        return ([output_file], [output_metadata])


#------------------------------------------------------------------------------
class SimpleWorkflow(Workflow):
    """
    input1		input2
	  |			  |
     Tool1		 Tool1
	  |			  |
	  +-----.-----+
			|
		  Tool2
			|
		  result
    """

    input_data_type = ["number file", "number file"]
    output_data_type = "number file"
    
    def run(self, files, metadata):
        "0. perform checks"
        assert len(files) == 2
        assert len(metadata) == 2
        input1, input2 = files
        inmd1, inmd2 = metadata

        "1.a Instantiate Tool and run"
        simpleTool1 = SimpleTool1(self.configuration)
        output1, outmd1 = simpleTool1.run([input1], [inmd1])

        "2.a Add outputs to intermediates"
        self.add_intermediate(output1, outmd1)

        "1.b (Instantiate Tool) and run"
        output2, outmd2 = simpleTool1.run([input2], [inmd2])

        "2.b Add outputs to intermediates"
        self.add_intermediate(output2, outmd2)

        "1.c Instantiate Tool and run"
        simpleTool2 = SimpleTool2(self.configuration)
        output3, outmd3 = simpleTool2.run(
            (output1[0], output2[0]), (outmd1[0], outmd2[0]))

        "4. Optionally edit the output metadata"
        "5. Return"
        return (output3, outmd3)

#------------------------------------------------------------------------------
if __name__ == "__main__":
    # 1. Create some data: 2 input files
    with open("file1","w") as f:
        f.write("5")
    with open("file2","w") as f:
        f.write("9")

    # 2. Register the data with the DMP
    import os
    from dmp import dmp
    da = dmp()
    pwd = os.getcwd()
    opj = os.path.join
    id1 = da.set_file("user1", opj(pwd, "file1"), "plain text", "number file")
    id2 = da.set_file("user1", opj(pwd, "file2"), "plain text", "number file")
    print da.get_files_by_user("user1")
    
    # 3. Instantiate and launch the App
    from ..apps import WorkflowApp
    app = WorkflowApp()
    id3 = app.launch(SimpleWorkflow, [id1, id2], {})
    
    print da.get_files_by_user("user1")
