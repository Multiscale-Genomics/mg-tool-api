#------------------------------------------------------------------------------
# Workflow App
#------------------------------------------------------------------------------
from . import PyCOMPSsApp, LocalApp
from .. import Workflow

class WorkflowApp(PyCOMPSsApp, LocalApp):
    """
    Workflow-aware App.

    Inherits from the LocalApp (see LocalApp) and the PyCOMPSsApp.
    """

    def _post_run(self, tool_instance, output_files, output_metadata):
        """
        Also unstage intermediate files.
        """
        output_files, output_metadata = super(WorkflowApp, self)._post_run(
            tool_instance, output_files, output_metadata)
        if issubclass(tool_instance.__class__, Workflow):
            self._unstage(*zip(*tool_instance.intermediate_outputs))
        return output_files, output_metadata
