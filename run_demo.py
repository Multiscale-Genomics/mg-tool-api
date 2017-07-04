"""
Run a named demo by attempting to import it from the demos subpackage.

Usage:

python run_demo.py DEMO_NAME


A folder "demos/DEMO_NAME" should exist and contain an __init__.py file
that defines at least a "main()" method, which accepts no arguments and
takes care of initialising and running the demo (possibly generating
valid input files). 

Demos can be added to be executed automatically in "bin/launchDemos.sh".
Any input, intermediate and output files generated by demos should be
deleted in the "bin/cleanDemos.sh" script.

"""

import sys
import demos
import importlib
# import pycompss_mock

if __name__ == "__main__":
    demoname = sys.argv[1]
    try:
        demo = importlib.import_module("demos.{}".format(demoname))
    except ImportError:
        sys.stderr.write("ERROR: Couldn't run demo {}.".format(demoname))
        sys.exit(1)

    demo.main()
