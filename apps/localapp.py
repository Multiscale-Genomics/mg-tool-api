#------------------------------------------------------------------------------
# Local Filesystem App
#------------------------------------------------------------------------------
from .. import App, Metadata
from dmp.dmp import dmp
da = dmp()

class LocalApp(App):
    """
    Local Filesystem App.

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

    def _stage(self, input_ids):
        """
        In this scenario, we just need to retrieve the "file_path"s from
        the DMP API.
        """
        file_names = []
        metadata = []
        for iid in input_ids:
            "Get the entry from the DMP database"
            file_obj = da.get_file_by_id('user1', iid)
            file_names.append(file_obj["file_path"])
            metadata.append(Metadata(
                file_obj["data_type"],
                file_obj["file_type"],
                file_obj["source_id"],
                file_obj["meta_data"],
                iid))
        return file_names, metadata

    def _unstage(self, output_files, output_metadata):
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
                source = metadata.source_id,
                meta = metadata.meta_data))
        return ids
