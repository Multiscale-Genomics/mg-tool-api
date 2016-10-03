"""
In this simple example, tools are implemented to:

a. Ab-initio predict the structure of a protein given its sequence;
b. Ab-initio predict the structure of a DNA oligomer given its sequence;
c. Rigid-body dock two molecules given their 3D structure.

These tools wrap external resources, Python libraries, binary executables or 
REST APIs, to perform their task; in this example these are not implemented,
but may be replaced with existing tools in the future. 

Finally, an example simple workflow is outlined to generate a protein-DNA 
complex given the sequence of the two partners using the tools defined above.
"""

from mug import datatypes as mug_datatypes
from mug import conversion as mug_conversion
from .tool import Tool
from .resource import Resource

from pycompss.api.task import task
from pycompss.api.constraint import constraint
from pycompss.api.parameter import IN, OUT


#------------------------------------------------------------------------------
# Example tools
#------------------------------------------------------------------------------
class ProteinAbInitioStructurePrediction(Tool):

    """
    An example tool that predicts the structure of a protein given its
    sequence in FASTA format. As an example, this tool uses a dummy Python
    library to perform the prediction, which requires numpy and scipy.
    """

    # mug_datatypes contains all accepted data types in MuG (see DMP)
    input_data_type = mug_datatypes.Sequence
    output_data_type = mug_datatypes.PDBStructure
    configuration = dict(output_format="PDB")

    @task(protein_sequence = IN, output_resource = OUT)
    @constraint(AppSoftware="numpy,scipy")
    def run(self, protein_sequence):
        
        # 0. Import the dummy structure prediction library
        import protein_abinit
        
        try:
            # 1. Stage resource locally as a file
            protein_sequence.write("tempfile.fasta")
            
            # 2. Convert from FASTA to just sequence (XXX: use mug_conversion)
            with file("tempfile2", 'w') as outfile:
                grep = subprocess.Popen(['grep', '-v', "'>' tempfile.fasta"],
                                        stdout=outfile, shell=False)
                grep.wait()
            
            # 3. Perform action (rate-limiting step)
            with file("tempfile2") as infile, \
              file("prediction.pdb", 'w') as outfile:
                protein_abinit.structure_from_sequence(
                    input_file = infile,
                    output_file = outfile,
                    **configuration)      # note: specifies output file format

            # 4. In this case, no output conversion is needed
            # 5. Return output resource
            output_resource = FileResource(output_data_type, "prediction.pdb")
        
        except Exception as e:
            # 6. Handle failure here.
            # If the tool fails, the output_resource carries error information
            output_resource = Resource(mug_datatypes.Error)
            output_resource.exception = e
            
        return output_resource

#------------------------------------------------------------------------------
class DNAAbInitioStructurePrediction(Tool):

    """
    An example tool that predicts the structure of a DNA oligomer given its
    sequence in FASTA format. As an example, this tool uses a dummy external
    executable binary to perform the prediction, which runs on Linux.
    """

    # mug_datatypes contains all accepted data types in MuG (see DMP)
    input_data_type = mug_datatypes.Sequence
    output_data_type = mug_datatypes.PDBStructure
    configuration = {}

    @task(dna_sequence = IN, output_resource = OUT)
    @constraint(ProcessorArch="x86_64", OperatingSystemType="Linux")
    def run(self, dna_sequence):

        # 0. Import the mug_conversion library, which provides
        #    routines to perform common conversion tasks
        import mug_conversion
        
        try:
            # 1. Stage resource locally as a file
            dna_sequence.write("tempfile.fasta")
            
            # 2. No conversion required
            # 3. Perform action (rate-limiting step)
            with file("out.log",'w') as stdout, \
                file("err.log",'w') as stderr:
                predict  = subprocess.Popen(['dna_predict_structure',
                                            '--infile=tempfile.fasta',
                                            '--informat="fasta"',
                                            '--outfile=tempfile2.mol'],
                                            stdout=stdout, stderr=stderr,
                                            shell=False)
                predict.wait()
                
            # 3b. Check output for errors
            #     assume the 'dna_predict_structure' writes an "ERROR" 
            #     message to stderr upon failure
            with file("err.log") as stderr:
                for line in stderr:
                    if line.startswith("ERROR"):
                        raise RuntimeError(line.strip())
            
            # 4. Conversion output from "mol" to "pdb"
            #    using a function from the "mug_conversion" library
            mug_conversion.mol_to_pdb("tempfile2.mol", "prediction.pdb")
            
            # 5. Return output resource
            output_resource = FileResource(output_data_type, "prediction.pdb")
        
        except Exception as e:
            # 6. Handle various exceptions here.
            # If the tool fails, the output_resource carries error information
            output_resource = Resource(mug_datatypes.Error)
            output_resource.exception = e
            
        return output_resource

#------------------------------------------------------------------------------
class RigidBodyDocking(Tool):

    """
    An example tool that rigid-body docks two molecules, given their PDB
    structures. As an example, this tool uses a dummy REST API to perform the
    prediction.
    """

    # mug_datatypes contains all accepted data types in MuG (see DMP)
    input_data_type = [mug_datatypes.PDBStructure, mug_datatypes.PDBStructure]
    output_data_type = mug_datatypes.PDBStructure
    configuration = {
        'optimise_backbone':False,
        'optimise_sidechains':False}

    @task(model1 = IN, model2 = IN, output_resource = OUT)
    @constraint()
    def run(self, model1, model2):

        # 0. Import the "requests" library to simplify REST API calls;
        #    ideally, the REST API should be wrapped in a Python client.
        import requests, json
        
        try:
            # 1. Retrieve input resources as a file object
            file1 = model1.as_file()
            file2 = model2.as_file()
            
            # 2. No conversion required
            # 3. Perform action (rate-limiting step)
            url   = "http://bestdockingever.com/submit"
            files = {'model1': file1,
                     'model2': file2}
            r = requests.post(url,
                              files=files,
                              data = json.dumps(self.configuration))
                
            # 3b. Check output for errors
            if r.status_code != requests.codes.ok:
                r.raise_for_status()
            
            # 4. No conversion required on output
            # 5. Return output resource
            #    assume the REST API returns a valid PDB string.
            output_resource = TextResource(output_data_type, r.text)
        
        except Exception as e:
            # 6. Handle various exceptions here.
            # If the tool fails, the output_resource carries error information
            output_resource = Resource(mug_datatypes.Error)
            output_resource.exception = e
            
        return output_resource

#------------------------------------------------------------------------------
# Example workflow
#
# Note that the workflow is implemented as a subclass of Tool, making it 
# possible to further combine workflows to construct more complex operations.
#------------------------------------------------------------------------------
class DockingWorkflow(Tool):
    
    """
    An example workflow to predict the structure of a protein-DNA complex by
    docking the two partners' ab-initio predicted structures given their
    sequence. The workflow doesn't perform any action itself, but just
    combines the actions of several other tools.
    """
    
    input_data_type = [mug_datatypes.Sequence, mug_datatypes.Sequence]
    output_data_type = mug_datatypes.PDBStructure
    configuration = {}
    # A simple naming convention could be defined in order to distinguish
    # configuration entries for the different steps in the workflow; for
    # example, entries could be prefixed (e.g. "output_format" may become
    # "docking_output_format"), and then automatically filtered to configure
    # each step.
    
    @task(protein_sequence = IN, dna_sequence = IN, output_resource = OUT)
    @constraint()
    def run(self, protein_sequence, dna_sequence):
        protein_structure = ProteinAbInitioStructurePrediction().run(
            protein_sequence)
        dna_structure = DNAAbInitioStructurePrediction().run(
            dna_sequence)
        output_resource = RigidBodyDocking().run(
            protein_structure,
            dna_structure)
        return output_resource
