if __name__ == "__main__":

    ## Mock the MuG library
    class datatypes(object):
        Sequence = 0
        PDBStructure = 1

    class conversion(object):
        def mol_to_pdb(molfile, pdbfile):
            pass

    class mug(object):
        datatypes = datatypes
        conversion = conversion

    import sys
    sys.modules["mug"] = mug


    ## Mock pycompss
    class parameter(object):
        IN=0
        OUT=1
        #...

    class task(object):
        @staticmethod
        def task(**kwargs):
            return lambda x:x

    class constraint(object):
        @staticmethod
        def constraint(**kwargs):
            return lambda x:x

    import sys
    sys.modules["pycompss"] = object()
    sys.modules["pycompss.api"] = object()
    sys.modules["pycompss.api.task"] = task
    sys.modules["pycompss.api.constraint"] = constraint
    sys.modules["pycompss.api.parameter"] = parameter

    ## Import and execute workflow
    sys.path.append("/Users/marco/sci/MuG/src/D6.1")
    from MuGtoolAPI import tool, example_docking_workflow, resource

    protein_sequence = resource.Resource(mug.datatypes.Sequence)
    dna_sequence = resource.Resource(mug.datatypes.Sequence)
    example_docking_workflow.DockingWorkflow().run(
        protein_sequence, dna_sequence)
