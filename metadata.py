#------------------------------------------------------------------------------
# Metadata class
#------------------------------------------------------------------------------
import copy
class Metadata(object):
    """
    Object containing all information pertaining to a specific data element.
    """
    def __init__(self, data_type, file_type,
                     source_id = None, meta_data = None, data_id = None):
        """
        Initialise the Metadata; for more information see the documentation for
        the MuG DMP API. The "data_id" parameter should only be specified when
        the Metadata instance refers to an existing element in the DMP
        database. 


        Parameters
        ----------
        data_type : str
        	The type of information in the file
        file_type : str
        	File format
        source_id : list
        	List of IDs of files that were processed to generate this file
        meta_data : dict
        	Dictionary object containing the extra data related to the 
            generation of the file or describing the way it was processed
        data_id : str
        	ID of the corresponding file in the DMP database
        """
        self.data_type = data_type
        self.file_type = file_type
        self.source_id = source_id
        self.meta_data = meta_data
        self.id = data_id
        self.exception = None
        self.error = False

    def __repr__(self):
        return """<Metadata: ({md.id})
    data_type: {md.data_type}
    file_type: {md.file_type}
    source_id: {md.source_id}
    meta_data: {md.meta_data}>""".format(md=self)
        
    def set_exception(self, exception):
        """
        Set an exception on this Metadata, in order to bubble up error
        information back to the App. 


        Parameters
        ----------
        exception : Exception
        	The exception to rise in the App
        """
        self.exception = exception
        self.error = True
        return True

    @classmethod
    def get_child(cls, parents):
        """
        Generate a stub for the metadata of a new data element generated
        from the data element described in the specified parents.

        Fields "data_type" and "file_type" are taken from the first parent; the
        "meta_data" fields are merged from all parents, in their respective
        order (i.e. values in the last parent prevail).
        
        While making a copy, ensure the copy is deep enough that changing the
        child instance will not affect the parents.


        Parameters
        ----------
        parents : list
        	List of Metadata instances


        Returns
        -------
        Metadata
        	An instance of Metadata generated as described above

        
        Example
        -------
        >>> import Metadata
        >>> metadata1 = Metadata(...)
        >>> metadata2 = Metadata(...)
        >>> child_metadata = 
        >>> 	Metadata.get_child([metadata1, metadata2])
        """
        if type(parents) not in [list, tuple]:
            parents = (parents,)
        meta_data = copy.deepcopy(parents[0].meta_data)
        [meta_data.update(parent.meta_data) for parent in parents[1:]]
            
        return cls(parents[0].data_type,
                      parents[0].file_type,
                      source_id = [parent.id for parent in parents],
                      meta_data = meta_data)

    
