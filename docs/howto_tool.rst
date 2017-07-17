Creating a Tool
===============

This document provides a tutorial for the creation of a tool that can be used within a pipeline within the MuG VRE. All functions should be wrapped up as a tool, this then allows for the tools to be easily reused by other pipelines and also deployed onto the compute cluster.

The Tool is the core element when it comes to running a program of function within the COMPSs environment. It defines the procedures that need to happen to prepare the data along with the function that is parelised to run over the chunks of data provided. A function can be either a piece of code that is written in python or an external package that is run with given chunks of data or defined parameters. The results are then returned to the calling function for merging.

All functions contain at least a `run(self)` function which is called by the pipeline. The run function takes the input files (list), defined output files (list) and relevant metadata (dict). Returned by the run function is a list containing a list of the output files as the first object and a list of metadata dict objects as the second element.

Basic Tool
----------

This is a test tool that takes an input file, writes some text to it and then returns the file

.. code-block:: python
   :linenos:

   try:
       from pycompss.api.parameter import FILE_INOUT
       from pycompss.api.task import task
       from pycompss.api.api import compss_wait_on
   except ImportError:
       print("[Warning] Cannot import \"pycompss\" API packages.")
       print("          Using mock decorators.")

       from dummy_pycompss import FILE_INOUT
       from dummy_pycompss import task
       from dummy_pycompss import compss_wait_on

   from basic_modules.tool import Tool

   # ------------------------------------------------------------------------------

   class testTool(Tool):
       """
       Tool for writing to a file
       """

       def __init__(self):
           """
           Init function
           """
           print("Test writer")
           Tool.__init__(self)

      @task(file_loc=FILE_INOUT)
      def test_writer(self, file_loc):
          with open(file_loc, "w") as file_handle:
              file_handle.write("This is the test writer")

          return True

      def run(self, input_files, output_files, metadata=None):
          self.test_writer(input_files[0], output_files[0])

          return (output_files, {})

This is this simplest case of a Tool that will run a function within the COMPSS environment. The run function takes the input files, if the output files are defined it can use those as the output locations and any relevant metadata. The locations of the output files can also be defined within the run function as sometimes functions can generate a large number of files that are not always easy to define up front if the Tool is being run as part of the VRE or as part of a larger pipeline.

The run function then calls the `test_writer` function. This uses the python decorator syntax to highlight that it is a function that can be run in parallel to pyCOMPSs library. The `task` decorator is used to define the list of files and parameters that need to be passed to the function. It also requires a list of the files a that are to be returned. As such the most common types will be `FILE_IN`, `FILE_OUT`, `FILE_INOUT`.

Decorators can also be used to define the resources that are required by function. They can be used to define a set of machines that the task should be run on, required CPU capacity  or the amount of RAM that is required by the task. Defining these parameters helps the COMPSS infrastructure correctly allocate jobs so that they are able to run as soon as the resources allow and prevent the job failing by being run on a machine that does not have the correct resources.

Further details about COMPSS and pyCOMPSs can be found at the BSC website along with specific tutorials about how to write functions that can utilise the full power of COMPSS.


Practical Example
-----------------

Now that we know the basics it is possible to apply this to writing a tool that can run and perform a real operation within the cluster.

Here is a tool that uses BWA to index a genome sequence file that has been saved in FASTA format.

The run function takes the input FASTA file, from this is generates a list of the locations of the output files. The input file and output files are passed to the bwa_indexer function. The files do not need to be listed in the return call so True is fine. COMPSS handles the passing back of the files to the run function. The run function then returns the output files to the pipeline or the VRE.

.. code-block:: python
   :linenos:

   from __future__ import print_function

   try:
       from pycompss.api.parameter import FILE_IN, FILE_OUT
       from pycompss.api.task import task
       from pycompss.api.api import compss_wait_on
   except ImportError:
       print("[Warning] Cannot import \"pycompss\" API packages.")
       print("          Using mock decorators.")

       from dummy_pycompss import FILE_IN, FILE_OUT
       from dummy_pycompss import task
       from dummy_pycompss import compss_wait_on

   from basic_modules.tool import Tool

   # ------------------------------------------------------------------------------

   class bwaIndexerTool(Tool):
       """
       Tool for running indexers over a genome FASTA file
       """

       def __init__(self):
           """
           Init function
           """
           print("BWA Indexer")
           Tool.__init__(self)

       @task(file_loc=FILE_IN, amb_loc=FILE_OUT, ann_loc=FILE_OUT,
             bwt_loc=FILE_OUT, pac_loc=FILE_OUT, sa_loc=FILE_OUT)
       def bwa_indexer(self, file_loc, amb_loc, ann_loc, bwt_loc, pac_loc, sa_loc): # pylint: disable=unused-argument
           """
           BWA Indexer

           Parameters
           ----------
           file_loc : str
               Location of the genome assembly FASTA file
           amb_loc : str
               Location of the output file
           ann_loc : str
               Location of the output file
           bwt_loc : str
               Location of the output file
           pac_loc : str
               Location of the output file
           sa_loc : str
               Location of the output file
           """
           common_handler = common()
           amb_loc, ann_loc, bwt_loc, pac_loc, sa_loc = common_handler.bwa_index_genome(file_loc)
           return True

       def run(self, input_files, output_files, metadata=None):
           """
           Function to run the BWA over a genome assembly FASTA file to generate
           the matching index for use with the aligner

           Parameters
           ----------
           input_files : list
               List containing the location of the genome assembly FASTA file
           output_files : list
               List of output files generated
           meta_data : list

           Returns
           -------
           list
               amb_loc : str
                   Location of the output file
               ann_loc : str
                   Location of the output file
               bwt_loc : str
                   Location of the output file
               pac_loc : str
                   Location of the output file
               sa_loc : str
                   Location of the output file
           """
           output_metadata = {}

           # Define the names of the output files
           output_files = [
               input_files[0] + ".amb",
               input_files[0] + ".ann",
               input_files[0] + ".bwt",
               input_files[0] + ".pac",
               input_files[0] + ".sa"
           ]

           results = self.bwa_indexer(
               input_files[0],
               input_files[0] + ".amb",
               input_files[0] + ".ann",
               input_files[0] + ".bwt",
               input_files[0] + ".pac",
               input_files[0] + ".sa"
           )

           results = compss_wait_on(results)

           return (output_files, [output_metadata])

