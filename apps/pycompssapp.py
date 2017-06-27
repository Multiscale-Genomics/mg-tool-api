# -----------------------------------------------------------------------------
# PyCOMPSs App
# -----------------------------------------------------------------------------
from pycompss.api.api import compss_wait_on
from basic_modules.app import App


class PyCOMPSsApp(App):
    """
    PyCOMPSsApp: uses PyCOMPSs.
    """

    def _post_run(self, tool_instance, output_files, output_metadata):
        """
        Adds a wait command to ensure asynchronous tasks are
        terminated before unstaging.
        """
        output_files = compss_wait_on(output_files)
        # Please note that the _post_run can not be done before waiting for
        # the output files.
        # The compss_wait_on performs a synchronization and retrieves the
        # content from output_files. Then it is possible to perform any
        # post operation like storing the results somewhere.
        output_files, output_metadata = super(PyCOMPSsApp, self)._post_run(
                                                            tool_instance,
                                                            output_files,
                                                            output_metadata)
        return output_files, output_metadata
