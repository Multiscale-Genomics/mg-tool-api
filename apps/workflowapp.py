# -----------------------------------------------------------------------------
# Workflow App
# -----------------------------------------------------------------------------
from apps.localapp import LocalApp
from apps.pycompssapp import PyCOMPSsApp
from basic_modules.workflow import Workflow


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
        return output_files, output_metadata
