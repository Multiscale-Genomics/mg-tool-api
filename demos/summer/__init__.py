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
from simpleTool1 import SimpleTool1
from simpleTool2 import SimpleTool2


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

    def run(self, input_files, metadata, output_files):

        print "\t0. perform checks"
        assert len(input_files) == 2
        assert len(metadata) == 2
        input1, input2 = input_files
        inmd1, inmd2 = metadata
        output = output_files[0]

        print "\t1.a Instantiate Tool 1 and run"
        simpleTool1 = SimpleTool1(self.configuration)
        output1, outmd1 = simpleTool1.run([input1], [inmd1], [input1 + '.out'])

        print "\t1.b (Instantiate Tool) and run"
        output2, outmd2 = simpleTool1.run([input2], [inmd2], [input2 + '.out'])

        print "\t2. Instantiate Tool and run"
        simpleTool2 = SimpleTool2(self.configuration)
        output3, outmd3 = simpleTool2.run([output1[0], output2[0]],
                                          [outmd1[0], outmd2[0]],
                                          [output])

        print "\t4. Optionally edit the output metadata"
        print "\t5. Return"
        return (output3, outmd3)


# -----------------------------------------------------------------------------

def summer(inputFiles, inputMetadata, outputFiles):
    """
    Main function
    -------------

    This function launches the app.
    """

    # import pprint  # Pretty print - module for dictionary fancy printing

    # 1. Instantiate and launch the App
    print "1. Instantiate and launch the App"
    from apps.workflowapp import WorkflowApp
    app = WorkflowApp()
    result = app.launch(SimpleWorkflow, inputFiles, inputMetadata,
                        outputFiles, {})

    # 2. The App has finished
    print "2. Execution finished"


# -----------------------------------------------------------------------------

def main():
    inputFile1 = "file1"
    inputFile2 = "file2"
    metadataFile = "metadataFile"
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

    summer([inputFile1, inputFile2], [inputMetadataF1, inputMetadataF2],
         [outputFile])
