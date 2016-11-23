
# NOTE (161123): Important, Please Read
#
# In the absence of a Python object wrapping data elements that could convey
# related information such as data type, file format and other type-specific
# metadata, in the following code all these information are stored in a
# Metadata instance, one per each data element. Metadata for input data
# elements is provided to Tools via the run() method, which itself returns
# metadata for output data elements. The Metadata class is described here for
# ease of reading, but will be moved elsewhere.

from mug import datatypes as mug_datatypes
from dmp import dmp
da = dmp()

#------------------------------------------------------------------------------
# Main App Interface
#------------------------------------------------------------------------------
class App(object):
    """
    The generic App interface.

    Apps are the main entry point to the tools layer of the VRE; they deal
    with: 

    1) retrieving and staging the inputs required by Tools,
    3) instantiate and configure the Tool,
    3) calling its "run" method, and 
    4) finally unstaging its outputs.

    Apps have a "launch" method, which is called in order to run a Tool within
    the App. Each call wraps a single Tool class; note that multiple Tools can
    be combined to produce workflows (see documentation for Tool). By doing
    this, tool developers can take advantage of the VRE's capabilities to
    optimise the data flow according to the specific requirements of the
    workflow, by ensuring that data is staged/unstaged only once.

    Subclasses of App should implement operations specific to the particular
    execution environment, such as staging/unstaging.
    """

    def launch(tool_class, input_ids, configuration):
        """ 
        Run a Tool with the specified inputs and configuration.

        Arguments:
        - tool_class:		the subclass of Tool to be run;
        - input_ids:		a list of unique IDs of the input data elements
        					required by the Tool;
        - configuration:	a dictionary containing information on how the tool
        					should be executed.

        Returns a list of unique IDs for the Tool's output data elements.
        """
        
        "1) Retrieve and stage inputs"
        input_files, input_metadata = self._stage(input_ids)
        "2) Instantiate and configure Tool"
        tool_instance = tool_class(configuration)
        "3) Run Tool"
        output_files, output_metadata = tool_instance.run(
            *input_files, metadata = input_metadata)
        "4) Unstage outputs"
        output_ids = self._unstage(output_files, output_metadata)
        return output_ids

    def _stage(input_ids):
        """ 
        Retrieve and stage inputs, from a list of unique data IDs.
        This will involve calling the DMP's "get_file_by_id" method.
        Returns a list of file_names and a corresponding list of metadata.
        """
        pass

    def _unstage(output_files, output_metadata):
        """ 
        Unstage the tool's outputs, specified as a list of file names and a
        corresponding list of metadata. This will involve declaring each output
        data element to the DMP (via the "set_file" method) to obtain unique
        data IDs that are then returned as a list.
        """
        pass


#------------------------------------------------------------------------------
# Example App
#------------------------------------------------------------------------------
class SimpleApp(App):
    """
    Example simple App.

    Uses the DMP API to retrieve inputs and register outputs.
    This simple App assumes the "file_path" values returned by the DMP API are
    valid file locations on the local file system.


    NOTE: As a reminder, the DMP API describes a data element using the
    following fields (taken from the DMP API's documentation): 

    <user_id> - Identifier to uniquely locate the users files. Can be set to
    			"common" if the files can be shared between users 
    <file_path> - Location of the file in the file system
    <file_type> - File format
    <data_type> - The type of information in the file (RNA-seq, ChIP-seq, etc)
    <source_id> - List of IDs of files processed to generate this file 
    <meta_data> - Dictionary object containing the extra data related to the
    			  generation of the file or describing the way it was processed
    """

    def launch(tool_class, input_ids, configuration):
        """ 
        Same as in super, but add the "source_id" information to the
        output_metadata. This could also be done in the Tool.
        """
        
        input_files, input_metadata = self._stage(input_ids)
        tool_instance = tool_class(configuration)
        output_files, output_metadata = tool_instance.run(
            *input_files, metadata = input_metadata)

        "Add source_id if it wasn't specified by the Tool (None)"
        for metadata in output_metadata:
            if not metadata.source_id:
                metadata.source_id = input_ids
        
        output_ids = self._unstage(output_files, output_metadata)
        return output_ids

    def _stage(input_ids):
        """
        In this scenario, we just need to retrieve the "file_path"s from
        the DMP API.
        """
        file_names = []
        metadata = []
        for iid in input_ids:
            "Get the entry from the DMP database"
            file_obj = da.get_file_by_id(iid)
            file_names.append(file_obj["file_path"])
            metadata.append(Metadata(
                file_obj["data_type"],
                file_obj["file_type"],
                file_obj["source_id"],
                file_obj["meta_data"]))
        return file_names, metadata

    def _unstage(output_files, output_metadata):
        """
        In this scenario, we just need to declare the output files to
        the DMP API.
        """
        ids = []
        for file_name, metadata in zip(output_files, output_metadata):
            "Register the file to the DMP database"
            ids.append(da.set_file(
                'user1',
                file_name, metadata.file_type, metadata.data_type,
                source_id = metadata.source_id,
                meta = metadata.meta_data))
        return ids


#------------------------------------------------------------------------------
# Metadata class (TODO: move elsewhere)
#------------------------------------------------------------------------------
class Metadata(object):
    """
    Object containing all information pertaining to a specific data element.
    """
    def __init__(self, data_type, file_type, source_id, meta_data):
        self.data_type = data_type
        self.file_type = file_type
        self.source_id = source_id
        self.meta_data = meta_data
