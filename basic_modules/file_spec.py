from collections import defaultdict


class file_spec:
    """
    *file_spec* is a structure that contains information about file paths
    associated to their "role" in the tool execution (see the "name" property
    of input_files and output_files in Tool.json and config.json). It also
    serves to aggregate file path information together with the corresponding
    metadata.

    The aim of this structure is to hide all details of path handling from Tool
    developers. This information is accessed in Tools using the
    "get_path(role)" and "get_metadata(role)" methods.
    """
    def __init__(self):
        """"""
        self.path = defaultdict(list)
        self.metadata = defaultdict(list)
        self._role = dict()  # path->role backmap

    @property
    def nfiles(self):
        return len(self._role)

    def add_file(self, role, path, metadata):
        """
        Add a new path and metadata to the specified role.
        """
        self.path[role].append(path)
        self.metadata[role].append(path)
        self._role[path] = role
        return True

    def get_path(self, role=None):
        """
        Return the file path for the specified role.
        If the role is "allow_multiple", then return the CURRENT path.
        """
        self._check_role(role)
        return self.path[role][0]

    def get_next_path(self, role=None):
        """
        Return the next available file path for the specified role.
        If the role is "allow_multiple", then change the CURRENT path.
        """
        if len(self.path[role]) > 1:
            self.path[role].pop(0)
        return self.get_path(role)

    def get_metadata(self, role=None):
        """
        Return the default metadata for the specified role. This is specified
        in the config.json, once per role.
        """
        self._check_role(role)
        return self.metadata[role][0]

    def get_role(self, path):
        """
        Return the role of the specified file.
        """
        return self._role[path]

    def _check_role(self, role):
        if role is None and self.nfiles > 1:
            raise KeyError("Please select a role.")
        return True


class input_file_spec(file_spec):
    """
    *input_file_spec* has methods to deal with "allow_multiple=true" for
    input_files (see Tool.json and config.json).

    It contains a list of paths for each role, which may be of a single
    element if allow_multiple=False.
    """
    pass


class output_file_spec(file_spec):
    """
    *output_file_spec* has methods to deal with "allow_multiple=true" for
    output_files (see Tool.json and config.json).

    It contains a list of paths for each role, which may be either
    a valid path or a "pattern" when allow_multiple=True. Patterns are
    valid "format" strings, e.g. "output_file_{:02d}.fasta".

    This class also allows tools to specify which outputs have actually been
    created during a given run. In the following basic example, the single
    output file with role "sequence" is confirmed.

    class myTool(Tool):
        def run(input_files, output_files):
            input_sequence = input_files.get_path("sequence")
            output_sequence = output_file.get_path("sequence")
            file(output_sequence).write(input_sequence.replace("A","G"))
            output_file.confirm_output(
              output_sequence,
              source_paths=[input_sequence],
              metadata=output_file.get_metadata("sequence"))
            return output_file
    """

    def __init__(self):
        """
        Initialise structure that keeps track of confirmed output files.
        """
        file_spec.__init__(self)
        self.sources = dict()
        self.output_metadata = dict()

    def get_path(self, role=None, index=0):
        """
        Return the output file path for the specified role.
        If the role is "allow_multiple", then return the path with
        the specified index (default: first = 0).
        """
        self._check_role(role)
        path = self.path[role][0].format(index)
        self._role[path] = role
        return path

    def confirm_output(self, path, source_paths, metadata):
        """
        Confirm the output file *path* has been generated during the current
        run. Also, specify its *source_paths* and *metadata*.
        """
        self.sources[path] = source_paths
        self.output_metadata[path] = metadata
        return True

    def iterate_outputs(self):
        """
        Iterate through confirmed outputs: for each path, yield also its
        *source_paths* and *metadata*.
        """
        for path, sources in self.sources.items():
            yield path, sources, self.output_metadata[path]
