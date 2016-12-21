"""
Simple example of Workflow using PyCOMPSs, called using an App.

- SimpleTool1:
  reads an integer from a file, increments it, and writes it to file
- SimpleTool2:
  reads two integers from two file and writes their sum to file

- SimpleWorkflow:
  implements the following workflow:

      1           2
      |           |
     Tool1       Tool1
      |           |
      +-----.-----+
            |
          Tool2
            |
            3

  Where 1 and 2 are inputs, 3 is the output, Tool1 and Tool2 are the
  SimpleTool1 and SimpleTool2 defined above.

  The "main()" uses the WorkflowApp to launch SimpleWorkflow in order to
  unstage intermediate outputs.
"""

import os
from .. import Workflow
from simpletool1 import SimpleTool1
from simpletool2 import SimpleTool2


class SimpleWorkflow(Workflow):
    """
    input1      input2
      |           |
     Tool1       Tool1
      |           |
      +-----.-----+
            |
          Tool2
            |
          result
    """

    input_data_type = ["number file", "number file"]
    output_data_type = "number file"

    def run(self, files, metadata):
        # 0. perform checks
        assert len(files) == 2
        assert len(metadata) == 2
        input1, input2 = files
        inmd1, inmd2 = metadata

        # 1.a Instantiate Tool and run
        simpleTool1 = SimpleTool1(self.configuration)
        output1, outmd1 = simpleTool1.run([input1], [inmd1])

        # 2.a Add outputs to intermediates
        self.add_intermediate(output1, outmd1)

        # 1.b (Instantiate Tool) and run
        output2, outmd2 = simpleTool1.run([input2], [inmd2])

        # 2.b Add outputs to intermediates
        self.add_intermediate(output2, outmd2)

        # 1.c Instantiate Tool and run
        simpleTool2 = SimpleTool2(self.configuration)
        output3, outmd3 = simpleTool2.run(
            (output1[0], output2[0]), (outmd1[0], outmd2[0]))

        # 4. Optionally edit the output metadata
        # 5. Return
        return (output3, outmd3)


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # 1. Create some data: 2 input files
    with open("file1", "w") as f:
        f.write("5")
    with open("file2", "w") as f:
        f.write("9")

    # 2. Register the data with the DMP
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
