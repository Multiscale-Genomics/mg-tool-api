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
from tools_demos.simpleTool3 import SimpleTool3
from utils import remap


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
        print input_files, input_metadata, output_files
        print "\t0. perform checks"
        assert len(input_files.keys()) == 1
        assert len(input_metadata.keys()) == 1
        assert len(input_files["number"]) == len(input_metadata["number"])
        
        outputs = []
        out_mds = []
        print "\t1.a Instantiate Tool1"
        simpleTool1 = SimpleTool1(self.configuration)
        for i, path in enumerate(input_files["number"]):
            metadata = input_metadata["number"][i]
            print "\t1.b run %d"%i
            output, outmd = simpleTool1.run(
                {"input": path},
                {"input": metadata},
                {"output": path + '.out'})
            outputs.append(output["output"])
            out_mds.append(outmd["output"])

        print "\t2. Instantiate Tool and run"
        simpleTool3 = SimpleTool3(self.configuration)
        output3, outmd3 = simpleTool3.run(
            {"input": outputs},
            {"input": out_mds},
            output_files)

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
                        "tools_demos/config2.json",
                        "tools_demos/input_metadata2.json")

    # 2. The App has finished
    print "2. Execution finished; see /tmp/results.json"
    

if __name__ == "__main__":

    inputFile1 = "/tmp/file1"
    inputFile2 = "/tmp/file2"
    inputFile3 = "/tmp/file3"
    outputFile = "/tmp/outputFile%d"  # allow_multiple = True

    # The VRE has to prepare the data to be processed.
    # In this example we create 2 files for testing purposes.
    print "1. Create some data: 2 input files"
    with open(inputFile1, "w") as f:
        f.write("5")
    with open(inputFile2, "w") as f:
        f.write("9")
    with open(inputFile3, "w") as f:
        f.write("13")
    print "\t* Files successfully created"

    # Read metadata file and build a dictionary with the metadata:
    from basic_modules.metadata import Metadata
    # Maybe it is necessary to prepare a metadata parser from json file
    # when building the Metadata objects.
    inputMetadataF1 = Metadata("Number", "plainText")
    inputMetadataF2 = Metadata("Number", "plainText")
    inputMetadataF3 = Metadata("Number", "plainText")

    main({"number": [inputFile1, inputFile2, inputFile3]},
         {"number": [inputMetadataF1, inputMetadataF2, inputMetadataF3]},
         {"output": outputFile})

    main_json()
