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
    pass
