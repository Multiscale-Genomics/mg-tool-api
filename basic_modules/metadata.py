#!/usr/bin/env python
"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from __future__ import print_function
import copy


class Metadata(object):  # pylint: disable=too-few-public-methods
    """
    Object containing all information pertaining to a specific data element.
    """
    def __init__(self, data_type=None, file_type=None, file_path=None,  # pylint: disable=too-many-arguments
                 sources=None, meta_data=None, taxon_id=None):
        """
        Initialise the Metadata; for more information see the documentation for
        the MuG DMP API.


        Parameters
        ----------
        data_type : str
            The type of information in the file
        file_type : str
            File format
        file_path : str
            Relative path of the file
        sources : list
            List of paths of files that were processed to generate this file
        meta_data : dict
            Dictionary object containing the extra data related to the
            generation of the file or describing the way it was processed
        """
        self.data_type = data_type
        self.file_type = file_type
        self.file_path = file_path
        self.taxon_id = taxon_id
        if sources is None:
            sources = []
        self.sources = sources
        if meta_data is None:
            meta_data = {}
        self.meta_data = meta_data

    def __repr__(self):
        return """<Metadata:
            data_type: {md.data_type}
            file_type: {md.file_type}
            file_path: {md.file_path}
            sources: {md.sources}
            taxon_id: {md.taxon_id}
            meta_data: {md.meta_data}>""".format(md=self)

    @classmethod
    def get_child(cls, parents, path):
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
        >>> 	Metadata.get_child([metadata1, metadata2], 'child_file')
        """
        if isinstance(parents, [list, tuple]) is False:
            parents = (parents,)
        meta_data = copy.deepcopy(parents[0].meta_data)

        for parent in parents[1:]:
            meta_data.update(parent.meta_data)

        return cls(parents[0].data_type,
                   parents[0].file_type,
                   path,
                   sources=[parent.file_path for parent in parents],
                   meta_data=meta_data,
                   taxon_id=parents[0].taxon_id)
