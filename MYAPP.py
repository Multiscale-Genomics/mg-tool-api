"""
APPLICATION SKELETON

This file is intended to provide a brief overview of the structure of an
application implemented following the Application template developed for
the MUG project.

# Caution: since it is an skeleton, it is necessary to include some code in
order to make it work propperly.
"""

from basic_modules.workflow import Workflow
from tools.myTool1 import Tool1
from tools.myTool2 import Tool2


class myWorkflow(Workflow):
    """
    Define the workflow of the application.
    Brief overview of what it does.
    """

    # self variables
    configuration = {}
    # other user needed variables
    # ...

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
        """
        Workflow main code
        """

        print "\t0. perform checks"
        assert len(input_files) == 2
        assert len(metadata) == 1
        assert len(output_files) == 1

        output = output_files[0]

        print "\t1. Instantiate Tool 1 and run"
        tool1 = Tool1(self.configuration)
        output1, outmd1 = tool1.run(input_files, metadata, ['partial.out'])

        print "\t2. Instantiate Tool 2 and run"
        tool2 = Tool2(self.configuration)
        output2, outmd2 = tool2.run(output1, outmd1, [output])

        print "\t3. Optionally edit the output metadata"
        print "\t4. Return"

        return (output2, outmd2)


# -----------------------------------------------------------------------------

def main(inputFiles, inputMetadata, outputFiles, configuration):
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
    result = app.launch(myWorkflow, inputFiles, inputMetadata, outputFiles,
                        configuration)

    # 2. The App has finished
    print "2. Execution finished"


if __name__ == "__main__":
    # Note that the code that was within this if condition has been moved
    # to a function called 'main'.
    # The reason for this change is to improve performance.

    import sys
    inputFile1 = sys.argv[1]
    inputFile2 = sys.argv[2]
    metadataFile = sys.argv[3]
    outputFile = sys.argv[4]

    # other parameters
    configuration = {}

    # Read metadata file and build a dictionary with the metadata:
    from basic_modules.metadata import Metadata
    # Maybe it is necessary to prepare a metadata parser from json file
    # when building the Metadata objects.
    # Parse metadataFile and get data_type, file_type, source_id=None,
    # meta_data=None, data_id=None
    import json
    with open('metadata.json') as data_file:
        metadata = json.load(data_file)
    inputMetadata = Metadata(metadata['data_type'],
                             metadata["file_type"])

    main([inputFile1, inputFile2], [inputMetadata], [outputFile],
         configuration)
