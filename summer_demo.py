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
 SimpleTool1  SimpleTool1
      |			  |
      +-----.-----+
            |
       SimpleTool2
            |
            3

  Where 1 and 2 are inputs, 3 is the output, Tool1 and Tool2 are the
  SimpleTool1 and SimpleTool2 defined above.

  The "main()" uses the WorkflowApp to launch SimpleWorkflow in order to
  unstage intermediate outputs.
"""

from basic_modules.workflow import Workflow
from tools_demos.simpleTool1 import SimpleTool1
from tools_demos.simpleTool2 import SimpleTool2


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

    configuration = {}

    def __init__(self, configuration={}):
        """
        Initialise the tool with its configuration.


        Parameters
        ----------
        configuration : dict
            a dictionary containing parameters that define how the operation
            should be carried out, which are specific to each Tool.
        """
        self.configuration.update(configuration)

    def run(self, input_files, input_metadata, output_files):

        print "\t0. perform checks"
        assert len(input_files.keys()) == 2
        assert len(input_metadata.keys()) == 2
        input1 = input_files["number1"]
        input2 = input_files["number2"]
        inmd1 = input_metadata["number1"]
        inmd2 = input_metadata["number2"]
        output = output_files["output"]

        print "\t1.a Instantiate Tool 1 and run"
        simpleTool1 = SimpleTool1(self.configuration)
        output1, outmd1 = simpleTool1.run(
            {"input": input1},
            {"input": inmd1},
            {"output": input1 + '.out'})

        print "\t1.b (Instantiate Tool) and run"
        output2, outmd2 = simpleTool1.run(
            {"input": input2},
            {"input": inmd2},
            {"output": input2 + '.out'})

        print "\t2. Instantiate Tool and run"
        simpleTool2 = SimpleTool2(self.configuration)
        output3, outmd3 = simpleTool2.run(
            {"input1": output1["output"], "input2": output2["output"]},
            {"input1": outmd1["output"], "input2": outmd2["output"]},
            {"output": output})

        print "\t4. Optionally edit the output metadata"
        print "\t5. Return"
        return output3, outmd3


# -----------------------------------------------------------------------------

def main(inputFiles, inputMetadata, outputFiles):
    """
    Main function
    -------------

    This function launches the app.
    """

    # 1. Instantiate and launch the App
    print "1. Instantiate and launch the App"
    from apps.workflowapp import WorkflowApp
    app = WorkflowApp()
    result = app.launch(SimpleWorkflow, inputFiles, inputMetadata,
                        outputFiles, {})

    # 2. The App has finished
    print "2. Execution finished"


def main_json():
    """
    Alternative main function
    -------------

    This function launches the app using configuration written in
    two json files: config.json and input_metadata.json.
    """
    # 1. Instantiate and launch the App
    print "1. Instantiate and launch the App"
    from apps.jsonapp import JSONApp
    app = JSONApp()
    result = app.launch(SimpleWorkflow,
                        "/tmp/",
                        "tools_demos/config.json",
                        "tools_demos/input_metadata.json")

    # 2. The App has finished
    print "2. Execution finished; see /tmp/results.json"
    

if __name__ == "__main__":
    # Note that the code that was within this if condition has been moved
    # to a function called 'main'.
    # The reason for this change is to improve performance.

    inputFile1 = "file1"
    inputFile2 = "file2"
    outputFile = "outputFile"

    # The VRE has to prepare the data to be processed.
    # In this example we create 2 files for testing purposes.
    print "1. Create some data: 2 input files"
    with open(inputFile1, "w") as f:
        f.write("5")
    with open(inputFile2, "w") as f:
        f.write("9")
    print "\t* Files successfully created"

    # Read metadata file and build a dictionary with the metadata:
    from basic_modules.metadata import Metadata
    # Maybe it is necessary to prepare a metadata parser from json file
    # when building the Metadata objects.
    inputMetadataF1 = Metadata("Number", "plainText")
    inputMetadataF2 = Metadata("Number", "plainText")

    # main([inputFile1, inputFile2], [inputMetadataF1, inputMetadataF2],
    #      [outputFile])

    main_json()
