#------------------------------------------------------------------------------
# Main Resource interface
#------------------------------------------------------------------------------
class Resource(object):
    """
    Abstract class defining a generic resource.
    It must specify the data type, as defined in the DMP, which is defined at
    creation and is read-only.
    An exception can be attached to the resource to carry information about
    failure in the process generating the resource.
    Subclasses should implement the _retrieve() method according to the type of
    resource, as well as the various commodity staging methods (e.g. write,
    as_string, as_file). Other resource types might find it advantageous to
    define other staging methods for particular common usage scenarios
    (e.g. retrieving the ID of an entry in a database rather than the entry
    itself).
    
    """

    def __init__(self, data_type):
        self._data_type = data_type
        self.__data = None
        self._exception = None
    
    @property
    def data_type(self):
        """Enforce data type as read-only"""
        return self._data_type    

    @property
    def _resource(self):
        """Cache retrieved data"""
        if self.__data is None:
            self.__data = self._retrieve()
        return self.__data

    @_resource.setter
    def _resource(self, value):
        """Set the resource"""
        self.__data = value

    @property
    def exception(self):
        """Error information about failure to generate the resource"""
        return self._exception
        
    @exception.setter
    def exception(self, exception):
        """Attach error information"""
        self._exception = exception
    
    def _retrieve(self):
        """Retrieve data."""
        pass
        
    def write(self, name):
        """Write the resource to a named file"""
        pass
    
    def as_file(self):
        """Return the resource as an open file object"""
        pass
    
    def as_string(self):
        """Return the resource as a string"""
        pass

#------------------------------------------------------------------------------
# Example subclasses
#------------------------------------------------------------------------------
class FileResource(Resource):
    """A resource that is a Python file object."""

    def __init__(self, data_type, path, mode='r'):
        """
        Initialise this resource specifying, as well as the data_type, the
        path of the underlying file. The file will be opened with the specified
        mode (default 'r').
        """
        super(FileResource).__init__(data_type)
        self._file_path = path
        self._file_mode = mode
    
    def _retrieve(self):
        """Retrieving this resource amounts to opening the file."""
        self._resource = file(self._file_path, self._file_mode)

    def write(self, name):
        """Write the file to another location."""
        with file(name, 'w') as fout:
            fout.write(self.read())
            
    def as_file(self):
        return self
    
    def as_string(self):
        return self.read()
    
    def __getattr__(self,attr):
        """ Wrap file """
        if attr in self.__dict__:
            return getattr(self, attr)
        return getattr(self._resource, attr)

#------------------------------------------------------------------------------
class TextResource(Resource):
    """A resource that is a plain-text string."""

    def __init__(self, data_type, text):
        """
        Initialise this resource specifying, as well as the data_type, its full
        content as a string.
        """
        super(TextResource).__init__(data_type)
        self._resource = text
    
    def write(self, name):
        """Write the text to file"""
        with file(name, 'w') as fout:
            fout.write(self._resource)
            
    def as_file(self):
        """Use StringIO to provide file access to the text."""
        from StringIO import StringIO
        return StringIO(self._resource)
    
    def as_string(self):
        return self._resource
